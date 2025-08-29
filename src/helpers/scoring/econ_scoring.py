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
    return [article_econ_type, article_econ_condition, article_econ_direction, quantity_type, quantity_indicator, quantity_polarity]

def model_eval(rules, constraints, inputs, outputs=None, softmax_enabled=True, inference_enabled=True):
    with torch.no_grad():
        average_f1 = 0
        exploded_groundings = {}
        # rule f1 before inference
        for rule_name, grounding in inputs.items():
            curr_grounding = grounding.copy()
            if outputs != None and not softmax_enabled:
                curr_grounding['Score'] = list(outputs[rule_name].detach().numpy())
            elif outputs != None and softmax_enabled:
                outputs[rule_name] = torch.nn.functional.softmax(outputs[rule_name], dim=1)
                curr_grounding['Score'] = list(outputs[rule_name].detach().numpy())
            ground_truth = curr_grounding['GroundTruth'].tolist()
            exploded_groundings[rule_name] = curr_grounding.explode(['HeadVariable', 'RuleVariable', 'Score', 'label'])
            preds = np.argmax(np.array(curr_grounding['Score'].tolist()), axis=1)
            macro_f1 = sk.f1_score(ground_truth, preds, average='macro')
            print(f'rule: {rule_name}')
            print(f'macro f1: {macro_f1}')
            average_f1 += macro_f1

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
                macro_f1 = sk.f1_score(inputs[rule_name]['GroundTruth'].tolist(), preds, average='macro')
                print(f'rule: {rule_name}')
                print(f'macro f1: {macro_f1}')
                average_f1 += macro_f1
    return average_f1/6

def get_scored_groundings(rule_groundings_path, rule_type):
    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path, ['rule_one', 'rule_two', 'rule_three', 'rule_four', 'rule_five', 'rule_six'])
    for rule_name, rule in rule_groundings:
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
    return rule_groundings

def get_hard_constraints():
    # consistency between quantity type and indicator (macro)
    def constr_one(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        for index, row in rule_groundings['rule_four'].iterrows():
            split_head_variable = row['HeadVariable'].split('_')
            if split_head_variable[3] == 'macro':
                macro_type_var = head_dict[row['HeadVariable']]
                macro_indicator_var = head_dict['_'.join(['QI'] + split_head_variable[1:3])]
                m.addConstr(macro_type_var == macro_indicator_var)

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

    return [constr_one, constr_two]

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