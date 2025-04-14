
import src.helpers.scoring.scoring as scoring
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import pandas as pd
import src.helpers.loaders.mf_dataset_loader as dataset_loader
from typing import Dict
import pandas as pd
import gurobipy as gp
import torch
from src.inference.gurobi_inference_model import GurobiInferenceModel
import sklearn.metrics as sk
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
import math
from src.rules.rule_template import RuleTemplate
from src.rules.rule_type import RuleType


def get_scored_groundings(rule_groundings_path, rule_names, rule_type):
    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path, rule_names)

    if rule_type == 'tf':
        rule_groundings['rule_one'] = scoring.tf_scoring(rule_groundings['rule_one'], ['Id'])
        rule_groundings['rule_two'] = scoring.tf_scoring(rule_groundings['rule_two'], ['Id', 'Entity'])
        rule_groundings['rule_three'] = scoring.tf_scoring(rule_groundings['rule_three'], ['Id'])
        rule_groundings['rule_four'] = scoring.tf_scoring(rule_groundings['rule_four'], ['Id', 'Entity'])
    elif rule_type == 'mc':
        rule_groundings['rule_one'] = scoring.mc_scoring(rule_groundings['rule_one'], ['Id'], constants.MF_MC_LABEL_TO_CHOICE_INDEX)
        rule_groundings['rule_two'] = scoring.mc_scoring(rule_groundings['rule_two'], ['Id', 'Entity'], constants.MR_MC_LABEL_TO_CHOICE_INDEX)
        rule_groundings['rule_three'] = scoring.mc_scoring(rule_groundings['rule_three'], ['Id'], constants.MF_MC_LABEL_TO_CHOICE_INDEX )
        rule_groundings['rule_four'] = scoring.mc_scoring(rule_groundings['rule_four'], ['Id', 'Entity'], constants.MR_MC_LABEL_TO_CHOICE_INDEX)
    elif rule_type == 'gc':
        rule_groundings['rule_one'] = scoring.gc_scoring(rule_groundings['rule_one'], ['Id'])
        rule_groundings['rule_two'] = scoring.gc_scoring(rule_groundings['rule_two'], ['Id', 'Entity'])
        rule_groundings['rule_three'] = scoring.gc_scoring(rule_groundings['rule_three'], ['Id'])
        rule_groundings['rule_four'] = scoring.gc_scoring(rule_groundings['rule_four'], ['Id', 'Entity'])
    elif rule_type == 'gs':
        rule_groundings['rule_one'] = scoring.gs_scoring(rule_groundings['rule_one'])
        rule_groundings['rule_two'] = scoring.gs_scoring(rule_groundings['rule_two'])
        rule_groundings['rule_three'] = scoring.gs_scoring(rule_groundings['rule_three'])
        rule_groundings['rule_four'] = scoring.gs_scoring(rule_groundings['rule_four'])
    elif rule_type == 'vc':
        rule_groundings['rule_one'] = scoring.vc_scoring(rule_groundings['rule_one'], ['Id'])
        rule_groundings['rule_two'] = scoring.vc_scoring(rule_groundings['rule_two'], ['Id', 'Entity'])
        rule_groundings['rule_three'] = scoring.vc_scoring(rule_groundings['rule_three'], ['Id'])
        rule_groundings['rule_four'] = scoring.vc_scoring(rule_groundings['rule_four'], ['Id', 'Entity'])
    else:
        raise Exception('Invalid Rule Type')
    
    # drop duplicates: duplicates happen due to the splitting of the dataframe and duplicate id rows for examples with multiple entities to predict
    rule_groundings['rule_one'].drop_duplicates(['Id', 'Tweet', 'label'], inplace=True)
    rule_groundings['rule_two'].drop_duplicates(['Id', 'Tweet', 'Entity', 'label'], inplace=True)
    rule_groundings['rule_three'].drop_duplicates(['Id', 'Tweet', 'label'], inplace=True)
    rule_groundings['rule_four'].drop_duplicates(['Id', 'Tweet', 'Entity', 'label'], inplace=True)

    return rule_groundings

def get_mf_constraints(data_input_path):
    # get entity groups for entity constraint
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(data_input_path)
    entity_group_map = dataset_loader.get_entity_group_mappings(data, data_input_path)

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
    #custom_rule_constraints = [constr_one, constr_two, constr_three]
    return custom_rule_constraints

def model_eval(rules, constraints, inputs, outputs=None):
    with torch.no_grad():
        exploded_groundings = {}
        # rule f1 before inference
        for rule_name, grounding in inputs.items():
            curr_grounding = grounding.copy()
            if outputs != None:
                outputs[rule_name] = torch.nn.functional.softmax(outputs[rule_name], dim=1)
                curr_grounding['Score'] = list(outputs[rule_name].detach().numpy())
            ground_truth = curr_grounding['GroundTruth'].tolist()
            exploded_groundings[rule_name] = curr_grounding.explode(['HeadVariable', 'RuleVariable', 'Score', 'label'])
            preds = np.argmax(np.array(curr_grounding['Score'].tolist()), axis=1)
            micro_f1 = sk.f1_score(ground_truth, preds, average='micro')
            macro_f1 = sk.f1_score(ground_truth, preds, average='macro')
            print(f'rule: {rule_name}')
            print(f'micro f1: {micro_f1}')
            print(f'macro f1: {macro_f1}')
        # inference
        inference_model = GurobiInferenceModel(rules, exploded_groundings, constraints, num_solutions=1)
        solution = inference_model.inference()[0]
        mf_preds = []
        role_preds = []
        for index, row in inputs['rule_one'].iterrows():
            for i in range(len(row['HeadVariable'])):
                if solution[row['HeadVariable'][i]] == 1:
                    mf_preds.append(i)
                    break
        for index, row in inputs['rule_two'].iterrows():
            for i in range(len(row['HeadVariable'])):
                if solution[row['HeadVariable'][i]] == 1:
                    role_preds.append(i)
                    break

        # f1 after inference
        print(f'Moral Foundation Results')
        mf_micro_f1 = sk.f1_score(inputs['rule_one']['GroundTruth'].tolist(), mf_preds, average='micro')
        mf_macro_f1 = sk.f1_score(inputs['rule_one']['GroundTruth'].tolist(), mf_preds, average='macro')
        print(f'micro f1: {mf_micro_f1}')
        print(f'macro f1: {mf_macro_f1}')
        print(f'Moral Role Results')
        mr_micro_f1 = sk.f1_score(inputs['rule_two']['GroundTruth'].tolist(), role_preds, average='micro')
        mr_macro_f1 = sk.f1_score(inputs['rule_two']['GroundTruth'].tolist(), role_preds, average='macro')
        print(f'micro f1: {mr_micro_f1}')
        print(f'macro f1: {mr_macro_f1}')
    return mf_macro_f1, mf_micro_f1, mr_macro_f1, mr_micro_f1

def get_training_groundings(rule_groundings, data_input_path):
    # load labels
    mf_labels = dataset_loader.load_frame_labels(data_input_path)
    role_labels = dataset_loader.load_role_labels(data_input_path)
    mf_labels.rename(columns={'Label': 'GroundTruth'}, inplace=True)
    role_labels.rename(columns={'EntityLabel': 'GroundTruth'}, inplace=True)

    # exclude few shot example ids from evaluation
    mf_labels = mf_labels[~mf_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
    role_labels = role_labels[~role_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_one'] = rule_groundings['rule_one'][~rule_groundings['rule_one']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_two'] = rule_groundings['rule_two'][~rule_groundings['rule_two']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_three'] = rule_groundings['rule_three'][~rule_groundings['rule_three']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_four'] = rule_groundings['rule_four'][~rule_groundings['rule_four']['Id'].isin(constants.IDS_TO_EXCLUDE)]

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

        # split groundings into train/val/test data
    k = 5
    selection_data = rule_groundings['rule_one'][['Id', 'GroundTruth']]
    batch_size = 400
    batched_train_groundings = []
    k_fold_groundings = []
    # cross validation method
    skf = StratifiedKFold(k, shuffle=True, random_state=92)
    skf_split = skf.split(selection_data['Id'], selection_data['GroundTruth'])
    for train_indicies, test_indicies in skf_split:
        train_selection_data = selection_data.iloc[train_indicies]
        test_ids = selection_data.iloc[test_indicies]['Id']
        train, dev = train_test_split(train_selection_data, test_size=0.2, random_state=92, stratify=train_selection_data['GroundTruth'])
        batch_count = math.ceil(train.shape[0]/batch_size)
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
            test_groundings[rule_name] = grounding[grounding['Id'].isin(test_ids)]
            val_groundings[rule_name] = grounding[grounding['Id'].isin(dev['Id'])]
        k_fold_groundings.append(
            {
                'train': batched_train_groundings,
                'val': val_groundings,
                'test': test_groundings
            }
        )
    return k_fold_groundings

def get_rule_info():
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
    return rules