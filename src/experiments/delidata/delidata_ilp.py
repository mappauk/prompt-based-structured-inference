import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
import src.helpers.prompting.delidata_prompt_constants as constants
import src.helpers.scoring.delidata_scoring as delidata_scoring
import src.helpers.loaders.delidata_dataset_loader as dataset_loader
import src.analysis.analysis_helper as analysis_helper
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
from src.inference.gurobi_inference_model import GurobiInferenceModel
from typing import Dict

def main():
    # hyperparamaters
    rule_groundings_path = sys.argv[1]
    rule_type = sys.argv[2]
    # load data
    data = dataset_loader.load_delidata()
    # define rules
    rule_one = RuleTemplate(
        'rule_one',
        ['message_id', 'original_text'],
        constants.LEVEL_1_LABELS,
        'LevelOne_{message_id}_{label}',
        'RuleOne_{message_id}_{label}',
        RuleType.MULTI_CLASS,
    )
    rule_two = RuleTemplate(
        'rule_two',
        ['message_id', 'original_text'],
        constants.LEVEL_2_LABELS,
        'LevelTwo_{message_id}_{label}',
        'RuleTwo_{message_id}_{label}',
        RuleType.MULTI_CLASS,
    )
    rule_three = RuleTemplate(
        'rule_three',
        ['message_id', 'previous_message_id','original_text', 'previous_original_text', 'previous_annotation_type'],
        constants.LEVEL_1_LABELS,
        'LevelOnePrior_{message_id}_{previous_message_id}_{previous_annotation_type}_{label}',
        'RuleThree_{message_id}_{previous_message_id}_{previous_annotation_type}_{label}',
        RuleType.MULTI_CLASS,
    )
    rule_four = RuleTemplate(
        'rule_four',
        ['message_id', 'previous_message_id','original_text', 'previous_original_text', 'previous_annotation_target'],
        constants.LEVEL_2_LABELS,
        'LevelTwoPrior_{message_id}_{previous_message_id}_{previous_annotation_target}_{label}',
        'RuleFour_{message_id}_{previous_message_id}_{previous_annotation_target}_{label}',
        RuleType.MULTI_CLASS,
    )
    rules = {
        rule_one.name: rule_one, 
        rule_two.name: rule_two,
        rule_three.name: rule_three,
        rule_four.name: rule_four
    }

    custom_groupby_exclusions = {
        'rule_three': ['previous_annotation_type'],
        'rule_four': ['previous_annotation_target']
    }
    rule_names = ['rule_one', 'rule_two', 'rule_three', 'rule_four']
    # get rule groundings:
    rule_groundings = delidata_scoring.get_scored_groundings(rule_groundings_path, rule_names, rule_type)

    # define custom constraints
    def constr_one(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        for index, row in rule_groundings['rule_one'].iterrows():
            level_one_head = head_dict[row['HeadVariable']]
            level_one_head_split = row['HeadVariable'].split('_')
            level_two_list = constants.LEVEL_1_TO_LEVEL_2[level_one_head_split[2]]
            message_id = level_one_head_split[1]
            rhs = 0
            for level_two_label in level_two_list:
                rhs += head_dict[f'LevelTwo_{message_id}_{level_two_label}']
            m.addConstr(level_one_head <= rhs)
    def constr_two(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        for index, row in rule_groundings['rule_three'].iterrows():
            level_one_transition_head_split = row['HeadVariable'].split('_')
            message_id = level_one_transition_head_split[1]
            message_label = level_one_transition_head_split[4]
            previous_message_id = level_one_transition_head_split[2]
            previous_message_label = level_one_transition_head_split[3]
            level_one_transition_head = head_dict[row['HeadVariable']]
            level_one_previous = head_dict[f'LevelOne_{previous_message_id}_{previous_message_label}']
            level_one_current = head_dict[f'LevelOne_{message_id}_{message_label}']
            m.addConstr(level_one_transition_head == level_one_previous*level_one_current)
    def constr_three(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        for index, row in rule_groundings['rule_four'].iterrows():
            level_two_transition_head_split = row['HeadVariable'].split('_')
            message_id = level_two_transition_head_split[1]
            message_label = level_two_transition_head_split[4]
            previous_message_id = level_two_transition_head_split[2]
            previous_message_label = level_two_transition_head_split[3]
            level_two_transition_head = head_dict[row['HeadVariable']]
            level_two_previous = head_dict[f'LevelTwo_{previous_message_id}_{previous_message_label}']
            level_two_current = head_dict[f'LevelTwo_{message_id}_{message_label}']
            m.addConstr(level_two_transition_head == level_two_previous*level_two_current)
    custom_rule_constraints = [constr_one, constr_two, constr_three]
    #custom_rule_constraints = [constr_one, constr_two, constr_three]
    # perform inference
    inference_model = GurobiInferenceModel(rules, rule_groundings,  custom_rule_constraints, custom_grounding_grouping_exclusions=custom_groupby_exclusions)
    solutions = inference_model.inference()

    # extract few shot predictions
    level_1_argmax = {}
    level_2_argmax = {}
    message_id_groupings = rule_groundings['rule_one'].groupby(['message_id'])
    for group_name, group in message_id_groupings:
        max_label = None
        max_score = -1
        id = None
        for index, row in group.iterrows():    
            id = row['message_id']
            if row['Score'] > max_score:
                max_score = row['Score']
                max_label = row['label']
        level_1_argmax[id] = constants.LEVEL_1_LABEL_TO_INDEX[max_label]

    message_id_groupings = rule_groundings['rule_two'].groupby(['message_id'])
    for group_name, group in message_id_groupings:
        max_label = None
        max_score = -1
        id = None
        for index, row in group.iterrows():    
            id = row['message_id']
            if row['Score'] > max_score:
                max_score = row['Score']
                max_label = row['label']
        level_2_argmax[id] = constants.LEVEL_2_LABEL_TO_INDEX[max_label]

    # extract ilp predictions
    level_1_assignments = {}
    level_2_assignments = {}
    variable_assignments = solutions[0]
    for varName, value in variable_assignments.items():
        parsedVarName = varName.split('_')
        parsedId = parsedVarName[1]
        parsedLabel = parsedVarName[2]
        if parsedVarName[0] == 'LevelOne' and parsedVarName[len(parsedVarName) - 1] != 'n' and value == 1:
            if parsedId in level_1_assignments:
                raise(RuntimeError('Multiclass Constraint Violation'))
            level_1_assignments[parsedId] = constants.LEVEL_1_LABEL_TO_INDEX[parsedLabel]
        elif parsedVarName[0] == 'LevelTwo' and value == 1 and parsedVarName[len(parsedVarName) - 1] != 'n':
            if parsedId in level_2_assignments:
                raise(RuntimeError('Multiclass Constraint Violation'))
            level_2_assignments[parsedId] = constants.LEVEL_2_LABEL_TO_INDEX[parsedLabel]

    # Eval
    level_1_labels = []
    level_2_labels = []
    ilp_level_1_preds = []
    ilp_level_2_preds = []
    few_shot_level_1_preds = []
    few_shot_level_2_preds = []
    for index, row in data.iterrows():
        message_id = row['message_id']

        level_1_labels.append(constants.LEVEL_1_LABEL_TO_INDEX[row['annotation_type']])
        level_2_labels.append(constants.LEVEL_2_LABEL_TO_INDEX[row['annotation_target']])

        ilp_level_1_label = level_1_assignments[message_id]
        ilp_level_2_label = level_2_assignments[message_id]
        ilp_level_1_preds.append(ilp_level_1_label)
        ilp_level_2_preds.append(ilp_level_2_label)

        few_shot_level_1_label = level_1_argmax[message_id]
        few_shot_level_2_label = level_2_argmax[message_id]
        few_shot_level_1_preds.append(few_shot_level_1_label)
        few_shot_level_2_preds.append(few_shot_level_2_label)

    print('Few Shot Results')
    delidata_scoring.eval(few_shot_level_1_preds, few_shot_level_2_preds, level_1_labels, level_2_labels)
    print('ILP Results')
    delidata_scoring.eval(ilp_level_1_preds, ilp_level_2_preds, level_1_labels, level_2_labels)



if __name__ == "__main__":
    main()