import sys
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import src.helpers.scoring.scoring as scoring
from src.learning.models.logistic_regression import LogisticRegression
from src.learning.loss.structured_hinge_loss import StructuredHingeLoss
from src.learning.loss.joint_cross_entropy_loss import JointCrossEntropyLoss
from src.learning.loss.early_stopping import EarlyStopping
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import torch
import src.helpers.prompting.mf_prompt_constants as constants
from typing import Dict
import pandas as pd
import gurobipy as gp
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
from sklearn.model_selection import train_test_split, StratifiedKFold
import sklearn.metrics as sk
import numpy as np
import math
from src.inference.gurobi_inference_model import GurobiInferenceModel


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
        # loss computation
    return mf_macro_f1, mf_micro_f1, mr_macro_f1, mr_micro_f1

def checkpoint(models, folder):
    for i in range(len(models)):
        torch.save(models[i].state_dict(), folder + f'model_{i}.pth')

def load_checkpoint(models, folder):
    for i in range(len(models)):
        models[i].load_state_dict(torch.load(folder + f'model_{i}.pth'))    

def training_loop(
        rules, 
        custom_rule_constraints, 
        foundation_model, 
        foundation_model_w_context, role_model, 
        role_model_w_context, 
        learning_rate,
        batched_train_groundings,
        val_groundings,
        output_path,
        hot_start,
        hot_start_epochs,
        optimized_hot_start,
        only_ce_loss):
    # hyper params
    epochs = 10000
    num_solutions = 10
    best_val_loss = 1000000000000000
    
    # optimizers
    foundation_model_optimizer = torch.optim.Adam(foundation_model.parameters(), lr=learning_rate)
    foundation_model_w_context_optimizer = torch.optim.Adam(foundation_model_w_context.parameters(), lr=learning_rate)
    role_model_optimizer = torch.optim.Adam(role_model.parameters(), lr=learning_rate)
    role_model_w_context_optimizer = torch.optim.Adam(role_model_w_context.parameters(), lr=learning_rate)

    # loss functions and early stopping definitions
    joint_ce_loss = JointCrossEntropyLoss()
    structured_hinge_loss = StructuredHingeLoss(rules, custom_rule_constraints, num_solutions)
    ce_only_early_stopping = EarlyStopping(3, 0.001)
    structured_hinge_early_stopping = EarlyStopping(20, 0)


    for epoch in range(epochs):
        batch_losses = []
        # set models to train
        foundation_model.train()
        foundation_model_w_context.train()
        role_model.train()
        role_model_w_context.train()

        use_structured_loss = (
            (hot_start and epoch > hot_start_epochs) or
            (hot_start and optimized_hot_start and  not ce_only_early_stopping.training_flag)
        )

        for i in range(len(batched_train_groundings)):
            print(f"############ epoch {epoch}, batch: {i} ############")
            batch = batched_train_groundings[i]

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

            loss = None
            if use_structured_loss:
                loss = structured_hinge_loss(batch, outputs)
            else:
                loss = joint_ce_loss(batch, outputs)
            loss.backward()
            # update weights
            foundation_model_optimizer.step()
            foundation_model_w_context_optimizer.step()
            role_model_optimizer.step()
            role_model_w_context_optimizer.step()
            batch_losses.append(loss.item())

        # Estimate the f1 score for the development set
        print(f"Training Loss: {sum(batch_losses)/len(batch_losses)}")
        print(f'####################### Model Performance (Val) epoch: {epoch} #######################')

        # set models to eval
        foundation_model.eval()
        foundation_model_w_context.eval()
        role_model.eval()
        role_model_w_context.eval()

        # evaluate on validation set
        with torch.no_grad():
            val_outputs = {
                'rule_one': foundation_model(torch.tensor(val_groundings['rule_one']['Score'].tolist())),
                'rule_two': role_model(torch.tensor(val_groundings['rule_two']['Score'].tolist())),
                'rule_three': foundation_model_w_context(torch.tensor(val_groundings['rule_three']['Score'].tolist())),
                'rule_four': role_model_w_context(torch.tensor(val_groundings['rule_four']['Score'].tolist()))
            }
            val_loss = None
            if use_structured_loss:
                val_loss = structured_hinge_loss(val_groundings, val_outputs)
                structured_hinge_early_stopping.check_early_stopping(val_groundings, val_outputs)
            else:
                val_loss = joint_ce_loss(val_groundings, val_outputs)
                ce_only_early_stopping.check_early_stopping(val_loss, epoch)
            print(f'Validation Loss: {val_loss}')

            model_eval(rules, custom_rule_constraints, val_groundings, val_outputs)
            print('\n\n\n')

            should_update_best_loss = (
                only_ce_loss or 
                (optimized_hot_start and not ce_only_early_stopping.training_flag) or
                (hot_start and epochs > hot_start_epochs) 
            )

            if best_val_loss > val_loss and should_update_best_loss:
                checkpoint([foundation_model, foundation_model_w_context, role_model, role_model_w_context], output_path)
                best_val_loss = val_loss

            if (not ce_only_early_stopping.training_flag and only_ce_loss) or not structured_hinge_early_stopping.training_flag:
                break



def main():
    data_input_path = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    rule_type = sys.argv[3]
    model_checkpoint_path = sys.argv[4]
    mode = sys.argv[5]
    hot_start = sys.argv[6] == 'true'
    hot_start_epochs = int(sys.argv[7])
    optimized_hot_start = sys.argv[8] == 'true'
    only_ce_loss = sys.argv[9] == 'true'
    learning_rate = float(sys.argv[10])

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

    # drop duplicates: (TODO investigate why there are duplicates see: 746841997575520256)
    rule_groundings['rule_one'].drop_duplicates(['Id', 'Tweet', 'label'], inplace=True)
    rule_groundings['rule_two'].drop_duplicates(['Id', 'Tweet', 'Entity', 'label'], inplace=True)
    rule_groundings['rule_three'].drop_duplicates(['Id', 'Tweet', 'label'], inplace=True)
    rule_groundings['rule_four'].drop_duplicates(['Id', 'Tweet', 'Entity', 'label'], inplace=True)

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

    # models
    foundation_model = LogisticRegression(5, 5)
    foundation_model_w_context = LogisticRegression(5, 5)
    role_model = LogisticRegression(16, 16)
    role_model_w_context = LogisticRegression(16, 16)

    # split groundings into train/val/test data
    k = 5
    selection_data = rule_groundings['rule_one'][['Id', 'GroundTruth']]
    batch_size = 400
    batched_train_groundings = []

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
        if mode == 'eval':
            # load checkpoints
            load_checkpoint([foundation_model, foundation_model_w_context, role_model, role_model_w_context], model_checkpoint_path)
            # set models to eval
            foundation_model.eval()
            foundation_model_w_context.eval()
            role_model.eval()
            role_model_w_context.eval()
            # evaluate on test set
            with torch.no_grad():
                test_outputs = {
                    'rule_one': foundation_model(torch.tensor(test_groundings['rule_one']['Score'].tolist())),
                    'rule_two': role_model(torch.tensor(test_groundings['rule_two']['Score'].tolist())),
                    'rule_three': foundation_model_w_context(torch.tensor(test_groundings['rule_three']['Score'].tolist())),
                    'rule_four': role_model_w_context(torch.tensor(test_groundings['rule_four']['Score'].tolist()))
                }
                print(f'####################### Model Performance Test (pre-training) #######################')
                model_eval(rules, custom_rule_constraints, test_groundings)
                print('\n\n\n')
                print(f'####################### Model Performance Test (calibrated) #######################')
                model_eval(rules, custom_rule_constraints, test_groundings, test_outputs)
        else:
            training_loop(
                rules,
                custom_rule_constraints,
                foundation_model,
                foundation_model_w_context,
                role_model,
                role_model_w_context,
                learning_rate,
                batched_train_groundings,
                val_groundings,
                model_checkpoint_path,
                hot_start,
                hot_start_epochs,
                optimized_hot_start,
                only_ce_loss
            )


if __name__ == "__main__":
    main()