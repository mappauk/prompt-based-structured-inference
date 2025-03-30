import sys
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import src.helpers.scoring.scoring as scoring
from src.learning.models.logistic_regression import LogisticRegression
from src.learning.loss.structured_hinge_loss import StructuredHingeLoss
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import torch
import src.helpers.prompting.mf_prompt_constants as constants
from typing import Dict
import pandas as pd
import gurobipy as gp
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
from sklearn.model_selection import train_test_split, StratifiedKFold
import numpy as np
import math

def get_model_performance(inputs, outputs):
    # f1 before inference

    # inference

    # f1 after inference
    return None

def main():
    data_input_path = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    rule_type = sys.argv[3]
    rule_names = ['rule_one', 'rule_two', 'rule_three', 'rule_four']

    # load data, rule groundings, and labels
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(data_input_path)
    entity_group_map = dataset_loader.get_entity_group_mappings(data, data_input_path)
    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path, rule_names)
    mf_labels = dataset_loader.load_frame_labels(data_input_path)
    role_labels = dataset_loader.load_role_labels(data_input_path)
    mf_labels.rename(columns={'Label': 'GroundTruth'}, inplace=True)
    role_labels.rename(columns={'EntityLabel': 'GroundTruth'}, inplace=True)
    # exclude few shot ids from evaluation
    mf_labels = mf_labels[~mf_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
    role_labels = role_labels[~role_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
    data = data[~data['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_one'] = rule_groundings['rule_one'][~rule_groundings['rule_one']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_two'] = rule_groundings['rule_two'][~rule_groundings['rule_two']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_three'] = rule_groundings['rule_three'][~rule_groundings['rule_three']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_four'] = rule_groundings['rule_four'][~rule_groundings['rule_four']['Id'].isin(constants.IDS_TO_EXCLUDE)]

    # transform raw scores into score distribution
    if rule_type == 'tf':
        rule_groundings['rule_one'] = scoring.tf_scoring(rule_groundings['rule_one'], ['Id'])
        rule_groundings['rule_two'] = scoring.tf_scoring(rule_groundings['rule_two'], ['Id', 'Entity'])
        rule_groundings['rule_three'] = scoring.tf_scoring(rule_groundings['rule_three'], ['Id'])
        rule_groundings['rule_four'] = scoring.tf_scoring(rule_groundings['rule_four'], ['Id', 'Entity'])
    # collapse rule groundings
    rule_groundings['rule_one'] = rule_groundings['rule_one'].groupby(['Id', 'Tweet'], sort=False).agg(lambda x: list(x)).reset_index()
    rule_groundings['rule_two'] = rule_groundings['rule_two'].groupby(['Id', 'Tweet', 'Entity'], sort=False).agg(lambda x: list(x)).reset_index()
    rule_groundings['rule_three'] = rule_groundings['rule_three'].groupby(['Id', 'Tweet', 'Topic', 'Ideology'], sort=False).agg(lambda x: list(x)).reset_index()
    rule_groundings['rule_four'] = rule_groundings['rule_four'].groupby(['Id', 'Tweet', 'Topic', 'Ideology', 'Entity'], sort=False).agg(lambda x: list(x)).reset_index()
    # transform label names into indicies
    mf_labels['GroundTruth'] = mf_labels['GroundTruth'].apply(lambda x: constants.MF_MC_LABEL_TO_CHOICE_INDEX[x])
    role_labels['GroundTruth'] = role_labels['GroundTruth'].apply(lambda x: constants.MR_MC_LABEL_TO_CHOICE_INDEX[x])
    # join labels
    rule_groundings['rule_one'] = rule_groundings['rule_one'].merge(mf_labels, on=['Id'], how='inner')
    rule_groundings['rule_two'] = rule_groundings['rule_two'].merge(role_labels, on=['Id', 'Entity'], how='inner')
    rule_groundings['rule_three'] = rule_groundings['rule_three'].merge(mf_labels, on=['Id'], how='inner')
    rule_groundings['rule_four'] = rule_groundings['rule_four'].merge(role_labels, on=['Id', 'Entity'], how='inner')

    # define rules
    rule_one = RuleTemplate(
        'rule_one',
        ['Id', 'Tweet'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleOne_{Id}_{label}',
        RuleType.MULTI_CLASS
    )
    rule_two = RuleTemplate(
        'rule_two',
        ['Id', 'Tweet', 'Entity'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleTwo_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS
    )
    rule_three = RuleTemplate(
        'rule_three',
        ['Id', 'Tweet', 'Topic', 'Ideology'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleThree_{Id}_{label}',
        RuleType.MULTI_CLASS
    )
    rule_four = RuleTemplate(
        'rule_four',
        ['Id', 'Tweet', 'Entity', 'Ideology', 'Topic'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleFour_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS
    )
    rules = {
        rule_one.name: rule_one, 
        rule_two.name: rule_two, 
        rule_three.name: rule_three, 
        rule_four.name: rule_four
    }
    
    # define custom constraints
    def constr_one(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        rule_groundings['rule_two'].insert(0, 'MoralFrameLabel', rule_groundings['rule_two']['label'].apply(lambda x: constants.MORAL_FOUNDATION_ROLE_TO_MF[x]))
        merged_frame = rule_groundings['rule_two'].merge(rule_groundings['rule_one'], how='left', left_on=['Id', 'MoralFrameLabel'], right_on=['Id', 'label'])
        for index, row in merged_frame.iterrows():
            role_head = head_dict[row['HeadVariable_x']]
            frame_head = head_dict[row['HeadVariable_y']]
            m.addConstr(role_head <= frame_head) 
    def constr_two(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        instance_groupings = rule_groundings['rule_two'].groupby(['Id', 'label'])
        for group_name, group in instance_groupings:
            if group.shape[0] > 1:
                start_index = 1
                for index, row in group.iterrows():
                    left_hand = head_dict[row['HeadVariable']]
                    counter = 0
                    for index, row in group.iterrows():
                        if counter >= start_index:
                            right_hand = head_dict[row['HeadVariable']]
                            m.addConstr(left_hand <= 1 - right_hand)
                        counter += 1
                    start_index += 1
    def constr_three(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        role_groupings = rule_groundings['rule_four'].groupby(['Ideology', 'Topic'])
        for group_name, group in role_groupings:
            if group.shape[0] > 1:
                start_index = 1
                for index, main_row in group.iterrows():
                    entity_one_var = head_dict[main_row['HeadVariable']]
                    entity_one = main_row['Entity']
                    if entity_one == None or pd.isnull(entity_one):
                        continue
                    entity_one = entity_one.strip()
                    polarity = constants.POLARITY_MAP.get(main_row['label'], -1)
                    tweet_id = main_row['Id']
                    if polarity != -1:
                        counter = 0
                        for sec_index, sec_row in group.iterrows():
                            if counter >= start_index:
                                entity_two = sec_row['Entity']
                                if entity_two == None or pd.isnull(entity_two):
                                    continue
                                entity_two = entity_two.strip()
                                polarity_two = constants.POLARITY_MAP.get(sec_row['label'], -1)
                                entity_one_group_list = entity_group_map[entity_one]
                                entity_two_group_list = entity_group_map[entity_two]
                                entities_equal = entity_one == entity_two and entity_one not in constants.ENTITIES_TO_EXCLUDE
                                for entity_one_group in entity_one_group_list:
                                    if entity_one_group in entity_two_group_list:
                                        entities_equal = True
                                if tweet_id != sec_row['Id'] and polarity_two != -1 and polarity_two != polarity and entities_equal:
                                    entity_two_var = head_dict[sec_row['HeadVariable']]
                                    m.addConstr(entity_one_var + entity_two_var <= 1)
                            counter += 1
                    start_index += 1
    custom_rule_constraints = [constr_one, constr_two]
    
    # hyperparamaters
    learning_rate = 0.001
    num_solutions = 10

    # models
    foundation_model = LogisticRegression(5, 5)
    foundation_model_w_context = LogisticRegression(5, 5)
    role_model = LogisticRegression(16, 16)
    role_model_w_context = LogisticRegression(16, 16)
    
    # optimizers
    foundation_model_optimizer = torch.optim.Adam(foundation_model.parameters(), lr=learning_rate)
    foundation_model_w_context_optimizer = torch.optim.Adam(foundation_model_w_context.parameters(), lr=learning_rate)
    role_model_optimizer = torch.optim.Adam(role_model.parameters(), lr=learning_rate)
    role_model_w_context_optimizer = torch.optim.Adam(role_model_w_context.parameters(), lr=learning_rate)

    loss_func = StructuredHingeLoss(rules, custom_rule_constraints, num_solutions)

    # split groundings into train/val/test data
    k = 5
    selection_data = rule_groundings['rule_one'][['Id', 'GroundTruth']]
    train, test = train_test_split(selection_data, test_size=0.2, random_state=92, stratify=selection_data['GroundTruth'])
    train, val = train_test_split(train, test_size=0.1, random_state=92, stratify=train['GroundTruth'])
    training_percentage = 0.1
    #train = train.sample(frac=training_percentage, random_state=92)
    batch_size = 200
    batch_count = math.ceil(train.shape[0]/200)
    batched_train_groundings = []
    for i in range(batch_count):
        batched_train_groundings.append({})
    test_groundings = {}
    val_groundings = {}
    for rule_name, grounding in rule_groundings.items():
        for i in range(batch_count):
            batch_start = i*batch_size
            batch_end = min((i+1)*batch_size, train.shape[0])
            batched_train_groundings[i][rule_name] = grounding[grounding['Id'].isin(train.iloc[batch_start:batch_end]['Id'])]
        test_groundings[rule_name] = grounding[grounding['Id'].isin(test['Id'])]
        val_groundings[rule_name] = grounding[grounding['Id'].isin(val['Id'])]
    epochs = 10
    loss_history = []
    for epoch in range(epochs):
        for batch in batched_train_groundings:
            # zero gradients
            foundation_model_optimizer.zero_grad()
            foundation_model_w_context_optimizer.zero_grad()
            role_model_optimizer.zero_grad()
            role_model_w_context_optimizer.zero_grad()

            # get predictions
            foundation_model_logits = foundation_model(torch.tensor(batch['rule_one']['Score'].tolist()))
            foundation_model_w_context_logits = foundation_model_w_context(torch.tensor(batch['rule_three']['Score'].tolist()))
            role_model_logits = role_model(torch.tensor(batch['rule_two']['Score'].tolist()))
            role_model_w_context_logits = role_model_w_context(torch.tensor(batch['rule_four']['Score'].tolist()))

            outputs = {
                'rule_one': foundation_model_logits,
                'rule_two': role_model_logits,
                'rule_three': foundation_model_w_context_logits,
                'rule_four': role_model_w_context_logits
            }
            loss = loss_func(batch, outputs)
            loss.backward()
            # update weights
            foundation_model_optimizer.step()
            foundation_model_w_context_optimizer.step()
            role_model_optimizer.step()
            role_model_w_context_optimizer.step()
            loss_history.append(loss.item())
            break
            # Estimate the f1 score for the development set
        print(f"epoch {epoch}, loss: {sum(loss_history)/len(loss_history)}")
        get_model_performance()
        break



    


if __name__ == "__main__":
    main()