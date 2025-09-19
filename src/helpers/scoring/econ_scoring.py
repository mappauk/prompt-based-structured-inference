import src.helpers.scoring.scoring as scoring
import src.helpers.prompting.econ_prompt_constants as constants
import pandas as pd
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
import src.analysis.analysis_helper as analysis_helper
import json
from gurobipy import GRB
from src.helpers.scoring import scoring
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import src.helpers.loaders.econ_indicators_dataset_loader as dataset_loader


def get_rule_info():
    # define rules
    article_econ_type = RuleTemplate(
        'rule_one',
        ['Id', 'Text'],
        constants.ARTICLE_ECONOMIC_TYPE_LABELS,
        'AT_{Id}_{label}',
        'RuleOne_{Id}_{label}',
        RuleType.MULTI_CLASS
    )

    article_econ_condition = RuleTemplate(
        'rule_two',
        ['Id', 'Text'],
        constants.ARTICLE_ECONOMIC_CONDITIONS_LABELS,
        'AC_{Id}_{label}',
        'RuleTwo_{Id}_{label}',
        RuleType.MULTI_CLASS
    )

    article_econ_direction = RuleTemplate(
        'rule_three',
        ['Id', 'Text'],
        constants.ARTICLE_ECONOMIC_DIRECTION_LABELS,
        'AD_{Id}_{label}',
        'RuleThree_{Id}_{label}',
        RuleType.MULTI_CLASS
    )

    quantity_type = RuleTemplate(
        'rule_four',
        ['Id', 'IndicatorText', 'Context'],
        constants.QUANTITY_TYPE_LABELS,
        'QT_{Id}_{label}',
        'RuleFour_{Id}_{label}',
        RuleType.MULTI_CLASS
    )

    quantity_indicator = RuleTemplate(
        'rule_four',
        ['Id', 'IndicatorText', 'Context'],
        constants.QUANTITY_INDICATOR_LABELS,
        'QI_{Id}_{label}',
        'RuleFive_{Id}_{label}',
        RuleType.MULTI_CLASS
    )

    quantity_polarity = RuleTemplate(
        'rule_four',
        ['Id', 'IndicatorText', 'Context'],
        constants.QUANTITY_POLARITY_LABELS,
        'QP_{Id}_{label}',
        'RuleSix_{Id}_{label}',
        RuleType.MULTI_CLASS
    )
    return {
        'rule_one': article_econ_type, 
        'rule_two': article_econ_condition, 
        'rule_three': article_econ_direction, 
        'rule_four': quantity_type, 
        'rule_five': quantity_indicator, 
        'rule_six': quantity_polarity
    }

def model_eval(rules, constraints, inputs, outputs=None, softmax_enabled=True, inference_enabled=True):
    with torch.no_grad():
        average_f1 = 0
        exploded_groundings = {}
        rule_preds = {}
        # rule f1 before inference
        for rule_name, grounding in inputs.items():
            curr_grounding = grounding.copy()
            #print(curr_grounding)
            if outputs != None and not softmax_enabled:
                curr_grounding['Score'] = list(outputs[rule_name].detach().numpy())
            elif outputs != None and softmax_enabled:
                outputs[rule_name] = torch.nn.functional.softmax(outputs[rule_name], dim=1)
                curr_grounding['Score'] = list(outputs[rule_name].detach().numpy())
            #print(curr_grounding)
            exploded_groundings[rule_name] = curr_grounding.explode(['HeadVariable', 'RuleVariable', 'Score', 'label'])
            filtered_groundings = curr_grounding[curr_grounding['GroundTruth'] != -1]
            preds = np.argmax(np.array(filtered_groundings['Score'].tolist()), axis=1)
            rule_preds[rule_name] = pd.DataFrame({
                'Id': curr_grounding['Id'],
                'Prediction': np.argmax(np.array(curr_grounding['Score'].tolist()), axis=1),
            })
            ground_truth = filtered_groundings['GroundTruth'].tolist()
            #print(preds)
            #print(ground_truth)
            macro_f1 = sk.f1_score(ground_truth, preds, average='macro')
            print(f'rule: {rule_name}')
            print(f'macro f1: {macro_f1}')
            average_f1 += macro_f1
        get_constraint_violations(rule_preds)

        rule_preds = {}
        # inference
        if inference_enabled:
            average_f1 = 0
            inference_model = GurobiInferenceModel(rules, exploded_groundings, constraints, num_solutions=1)
            solution = inference_model.inference()[0]
            for rule_name, grounding in inputs.items():
                preds = []
                for index, row in inputs[rule_name].iterrows():
                    for i in range(len(row['HeadVariable'])):
                        if solution[row['HeadVariable'][i]] == 1:
                            preds.append(i)
                            break
                rule_preds[rule_name] = pd.DataFrame({
                    'Id': inputs[rule_name]['Id'],
                    'Prediction': preds,
                })
                ground_truth = inputs[rule_name]['GroundTruth'].tolist()
                clean_ground_truth = []
                clean_preds = []
                for i in range(len(ground_truth)):
                    if ground_truth[i] != -1:
                        clean_ground_truth.append(ground_truth[i])
                        clean_preds.append(preds[i])
                macro_f1 = sk.f1_score(clean_ground_truth, clean_preds, average='macro')
                print(f'rule: {rule_name}')
                print(f'macro f1: {macro_f1}')
                average_f1 += macro_f1
            get_constraint_violations(rule_preds)
    return average_f1/6

def get_scored_groundings(input_path, rule_groundings_path, rule_type):
    qual_data = dataset_loader.load_econ_indicators_qual(input_path + 'agreed_qual_dict.pkl', input_path + 'full_data_backup_sep5.db')
    quant_data = dataset_loader.load_econ_indicators_quant(input_path + 'agreed_quant_dict.pkl')
    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path, ['rule_one', 'rule_two', 'rule_three', 'rule_four', 'rule_five', 'rule_six'])
    qual_rules = {'rule_one', 'rule_two', 'rule_three'}
    quant_rules = {'rule_four', 'rule_five', 'rule_six'}
    for rule_name, rule in rule_groundings.items():
        if rule_type == 'tf':
            rule_groundings[rule_name] = scoring.tf_scoring(rule_groundings[rule_name], ['Id'])
        elif rule_type == 'mc':
            rule_groundings[rule_name] = scoring.mc_scoring(rule_groundings[rule_name], ['Id'], constants.MC_TASK_TO_CHOICE_MAP[rule_name])
        elif rule_type == 'gc':
            rule_groundings[rule_name] = scoring.gc_scoring(rule_groundings[rule_name], ['Id'])
        elif rule_type == 'gs':
            rule_groundings[rule_name] = scoring.gs_scoring(rule_groundings[rule_name])
        elif rule_type == 'vc':
            rule_groundings[rule_name] = scoring.vc_scoring(rule_groundings[rule_name], ['Id'])
        else:
            raise Exception('Invalid Rule Type')
        gold_column = constants.ECON_RULE_TO_LABEL_COLUMN_NAME[rule_name]
        if rule_name in qual_rules:
            rule_groundings[rule_name] = rule_groundings[rule_name].groupby(['Id', 'Text']).agg(lambda x: list(x)).reset_index()
            rule_groundings[rule_name] = pd.merge(rule_groundings[rule_name], qual_data[['Id'] + [gold_column]], on='Id')
        elif rule_name in quant_rules:
            rule_groundings[rule_name] = rule_groundings[rule_name].groupby(['Id', 'IndicatorText', 'Context']).agg(lambda x: list(x)).reset_index()
            rule_groundings[rule_name] = pd.merge(rule_groundings[rule_name], quant_data[['Id'] + [gold_column]], on='Id')
        rule_groundings[rule_name].rename(columns={gold_column: 'GroundTruth'}, inplace=True)

    rule_groundings['rule_one']['GroundTruth'] = rule_groundings['rule_one']['GroundTruth'].apply(lambda x: constants.ARTICLE_ECONOMIC_TYPE_TO_LABEL_INDEX[x])
    rule_groundings['rule_two']['GroundTruth'] = rule_groundings['rule_two']['GroundTruth'].apply(lambda x: constants.ARTICLE_ECONOMIC_CONDITIONS_TO_LABEL_INDEX[x])
    rule_groundings['rule_three']['GroundTruth'] = rule_groundings['rule_three']['GroundTruth'].apply(lambda x: constants.ARTICLE_ECONOMIC_DIRECTION_TO_LABEL_INDEX[x])
    rule_groundings['rule_four']['GroundTruth'] = rule_groundings['rule_four']['GroundTruth'].apply(lambda x: constants.QUANTITY_TYPE_TO_LABEL_INDEX[x])
    rule_groundings['rule_five']['GroundTruth'] = rule_groundings['rule_five']['GroundTruth'].apply(lambda x: constants.QUANTITY_INDICATOR_TO_LABEL_INDEX[x])
    rule_groundings['rule_six']['GroundTruth'] = rule_groundings['rule_six']['GroundTruth'].apply(lambda x: constants.QUANTITY_POLARITY_TO_LABEL_INDEX[x])
    rule_groundings['rule_six']['DocId'] = rule_groundings['rule_six']['Id'].apply(lambda x: str.split(x, '_')[0])

    return rule_groundings

def get_constraint_violations(predictions):
    constraint_one_merges = pd.merge(predictions['rule_four'], predictions['rule_five'], on='Id')
    constraint_one_violations = 0
    for index, row in constraint_one_merges.iterrows():
        if (row['Prediction_x'] == 0 and row['Prediction_y'] == 11):
            constraint_one_violations += 1
    
    constraint_two_merges = pd.merge(predictions['rule_one'], predictions['rule_two'], on='Id')
    constraint_two_merges = pd.merge(constraint_two_merges, predictions['rule_three'], on='Id')
    constraint_two_violations = 0
    for index, row in constraint_two_merges.iterrows():
        if (row['Prediction_x'] == 0 and row['Prediction_y'] == 0) or (row['Prediction_x'] == 0 and row['Prediction'] == 4):
            constraint_two_violations += 1
    
    predictions['rule_six']['DocId'] = predictions['rule_six']['Id'].apply(lambda x: str.split(x, '_')[0])
    article_groupings = predictions['rule_six'].groupby(['DocId'])
    constraint_three_violations = 0
    constraint_four_violations = 0
    for group_name, group in article_groupings:
        positive_polarity_count = 0
        negative_polarity_count = 0
        doc_id = None
        count = group.shape[0]
        for index, row in group.iterrows():
            if row['Prediction'] == 0:
                positive_polarity_count += 1
            elif row['Prediction'] == 1:
                negative_polarity_count += 1
            doc_id = row['DocId']
        article_condition = predictions['rule_two'].query(f'Id == {doc_id}')['Prediction'].iloc[0]
        article_direction = predictions['rule_three'].query(f'Id == {doc_id}')['Prediction'].iloc[0]
        if (article_condition == 1 and negative_polarity_count > count/2) or (article_condition == 2 and positive_polarity_count > count/2):
            constraint_three_violations += 1
        if (article_direction == 1 and positive_polarity_count > count/2) or (article_direction == 2 and negative_polarity_count > count/2):
            constraint_four_violations += 1

    print(f'Constraint 1 Violations: {constraint_one_violations}')
    print(f'Constraint 2 Violations: {constraint_two_violations}')
    print(f'Constraint 3 Violations: {constraint_three_violations}')
    print(f'Constraint 4 Violations: {constraint_four_violations}')

def get_hard_constraints():
    # consistency between quantity type and indicator (macro)
    def constr_one(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        for index, row in rule_groundings['rule_four'].iterrows():
            split_head_variable = row['HeadVariable'].split('_')
            if split_head_variable[3] == 'macro':
                macro_type_var = head_dict[row['HeadVariable']]
                none_var = head_dict['_'.join(['QI'] + split_head_variable[1:3] + ['none'])]
                m.addConstr(macro_type_var <= 1 - none_var)
                m.addConstr(none_var <= 1 - macro_type_var)

    # if article type is macro then conditions and direction must be predicted
    def constr_two(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        for index, row in rule_groundings['rule_one'].iterrows():
            split_head_variable = row['HeadVariable'].split('_')
            if split_head_variable[2] == 'macro':
                article_macro_var = head_dict[row['HeadVariable']]
                article_conditions_var = head_dict['_'.join(['AC', split_head_variable[1], 'irrelevant'])]
                article_directions_var = head_dict['_'.join(['AD', split_head_variable[1], 'irrelevant'])]
                m.addConstr(article_macro_var*article_conditions_var <= 0)
                m.addConstr(article_macro_var*article_directions_var <= 0)

    def constr_three(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        article_groupings = rule_groundings['rule_six'].groupby(['DocId'])
        for group_name, group in article_groupings:
            positive_constr = 0
            negative_constr = 0
            count = group.shape[0]
            for index, row in group.iterrows():
                if row['label'] == 'negative':
                    positive_constr += head_dict[row['HeadVariable']]
                    negative_constr -= head_dict[row['HeadVariable']]
                elif row['label'] == 'positive':
                    positive_constr -= head_dict[row['HeadVariable']]
                    negative_constr += head_dict[row['HeadVariable']]
                else:
                    positive_constr += head_dict[row['HeadVariable']]
                    negative_constr += head_dict[row['HeadVariable']]
            
            article_negative_var = head_dict['_'.join(['AC', row['DocId'], constants.QUANTITY_POLARITY_TO_ARTICLE_CONDITIONS['negative']])]
            article_positive_var = head_dict['_'.join(['AC', row['DocId'], constants.QUANTITY_POLARITY_TO_ARTICLE_CONDITIONS['positive']])]
            m.addConstr(negative_constr <=  count - article_negative_var*count)
            m.addConstr(positive_constr <=  count - article_positive_var*count)
    
    def constr_four(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        article_groupings = rule_groundings['rule_six'].groupby(['DocId'])
        for group_name, group in article_groupings:
            positive_constr = 0
            negative_constr = 0
            count = group.shape[0]
            for index, row in group.iterrows():
                if row['label'] == 'negative':
                    positive_constr += head_dict[row['HeadVariable']]
                    negative_constr -= head_dict[row['HeadVariable']]
                elif row['label'] == 'positive':
                    positive_constr -= head_dict[row['HeadVariable']]
                    negative_constr += head_dict[row['HeadVariable']]
                else:
                    positive_constr += head_dict[row['HeadVariable']]
                    negative_constr += head_dict[row['HeadVariable']]
            
            article_negative_var = head_dict['_'.join(['AD', row['DocId'], constants.QUANTITY_POLARITY_TO_ARTICLE_DIRECTION['negative']])]
            article_positive_var = head_dict['_'.join(['AD', row['DocId'], constants.QUANTITY_POLARITY_TO_ARTICLE_DIRECTION['positive']])]
            m.addConstr(negative_constr <=  count - article_negative_var*count)
            m.addConstr(positive_constr <=  count - article_positive_var*count)

    return [constr_one, constr_two]#, constr_three, constr_four]

def get_soft_constraints(penalties):
    # negative/positive polarity of a quantity indicates negative/positive economic conditions in article
    def constr_three(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        constraint_objective_penalty = 0
        for index, row in rule_groundings['rule_six'].iterrows():
            if row['label'] != 'neutral':
                quantity_var = head_dict[row['HeadVariable']]
                article_var = head_dict['_'.join(['AC', row['DocId'], constants.QUANTITY_POLARITY_TO_ARTICLE_CONDITIONS[row['label']]])]
                id = row['Id']
                slack_var = m.addVar(vtype=GRB.BINARY, name='Slack_C3_{id}')
                m.addConstr(quantity_var - 1 - slack_var <= article_var)
                constraint_objective_penalty -= slack_var*penalties[0]
        return constraint_objective_penalty

    # negative/positive polarity of a quantity indicates negative/positive economic direction in article
    def constr_four(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        constraint_objective_penalty = 0
        for index, row in rule_groundings['rule_six'].iterrows():
                if row['label'] != 'neutral':
                    quantity_var = head_dict[row['HeadVariable']]
                    article_var = head_dict['_'.join(['AD', row['DocId'], constants.QUANTITY_POLARITY_TO_ARTICLE_DIRECTION[row['label']]])]
                    id = row['Id']
                    slack_var = m.addVar(vtype=GRB.BINARY, name='Slack_C4_{id}')
                    m.addConstr(quantity_var - 1 - slack_var <= article_var)
                    constraint_objective_penalty -= slack_var*penalties[1]
        return constraint_objective_penalty

    # consecutive quantities have 
    def constr_five(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        for index, row in rule_groundings['rule_one'].iterrows():
            split_head_variable = row['HeadVariable'].split('_')
            if split_head_variable[2] == 'macro':
                article_macro_var = head_dict[row['HeadVariable']]
                article_conditions_var = head_dict['_'.join(['AC', split_head_variable[1], 'irrelevant'])]
                article_directions_var = head_dict['_'.join(['AD', split_head_variable[1], 'irrelevant'])]
                m.addConstr(article_macro_var*article_conditions_var <= 0)
                m.addConstr(article_macro_var*article_directions_var <= 0)

    return [constr_three, constr_four, constr_five]