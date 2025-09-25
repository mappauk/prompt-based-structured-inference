import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.analysis.analysis_helper as analysis_helper
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
from src.inference.gurobi_inference_model import GurobiInferenceModel
from typing import Dict
import src.helpers.scoring.mf_scoring as mf_scoring


def main():
    # hyperparamaters
    input_path = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    output_path = sys.argv[3]
    rule_type = sys.argv[4]
    # load data
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)
    entity_group_map = dataset_loader.get_entity_group_mappings(data, input_path)

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

    rule_names = ['rule_one', 'rule_two', 'rule_three', 'rule_four']
    # get rule groundings:
    rule_groundings = mf_scoring.get_scored_groundings(rule_groundings_path, rule_names, rule_type)
    print(rule_groundings)
    raise Exception()
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
    # perform inference
    inference_model = GurobiInferenceModel(rules, rule_groundings,  custom_rule_constraints)
    solutions = inference_model.inference()
    # save results
    variable_assignments = solutions[0]
    results = {}
    for varName, value in variable_assignments.items():
        parsedVarName = varName.split('_')
        parsedId = parsedVarName[1]
        id_result = {}
        if parsedId in results:
            id_result = results[parsedId]
        if parsedVarName[0] == 'MF' and parsedVarName[len(parsedVarName) - 1] != 'n' and value == 1:
            if 'MoralFrame' in id_result and value == 1:
                raise(RuntimeError('Multiclass Constraint Violation'))
            id_result['MoralFrame'] = parsedVarName[2]
        if parsedVarName[0] == 'Role' and value == 1 and parsedVarName[len(parsedVarName) - 1] != 'n':
            entity_result = {
                'Entity': parsedVarName[2],
                'Label': parsedVarName[3]
            }
            if 'EntityRoles' in id_result:
                id_result['EntityRoles'].append(entity_result)
            else:
                id_result['EntityRoles'] = [entity_result]
        results[parsedId] = id_result
    analysis_helper.write_json_file(output_path, results)

if __name__ == "__main__":
    main()
