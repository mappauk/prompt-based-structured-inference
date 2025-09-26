import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.rule_template import RuleTemplate
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict
import os
import src.helpers.scoring.mf_scoring as mf_scoring
import src.analysis.analysis_helper as analysis_helper
from src.inference.gurobi_inference_model import GurobiInferenceModel


def transform_openai_response(rule_groundings, responses):
    for rule_name, response_data in responses.items():
        print(len(response_data))
        rule_groundings[rule_name].drop(columns='Score', inplace=True)
        labels = None
        if rule_name == 'rule_one' or rule_name == 'rule_three':
            ids = []
            labels = []
            for response in response_data:
                id = response['custom_id'].split('_')[1]
                response_choices = response['response']['body']['choices']
                choices = []
                for i in range(len(response_choices)):
                    choices.append(response_choices[i]['message']['content'])
                ids.append(id)
                labels.append(choices)
            response_dataframe = pd.DataFrame({
                'Id': ids,
                'Score': labels
            })
            response_dataframe = response_dataframe.groupby(['Id'], sort=False).agg(sum).reset_index()
            rule_groundings[rule_name] = rule_groundings[rule_name].merge(response_dataframe, on='Id', how='left')
            rule_groundings[rule_name]['Score'] = rule_groundings[rule_name]['Score'].apply(lambda x: x if isinstance(x, list) else ['CARE/HARM', 'CARE/HARM'])
            '''
            for index, row in rule_groundings[rule_name].iterrows():
                if not isinstance(row['Score'], list):
                    print(row)
            print(response_dataframe.shape)
            print(response_dataframe)
            print(rule_groundings[rule_name].shape)
            raise Exception()
            '''
        else:
            print(len(response_data))
            ids = []
            entities = []
            labels = []
            for response in response_data:
                id_split = response['custom_id'].split('_', 2)
                id = id_split[1]
                entity = id_split[2]
                response_choices = response['response']['body']['choices']
                choices = []
                for i in range(len(response_choices)):
                    choices.append(response_choices[i]['message']['content'])
                ids.append(id)
                entities.append(entity)
                labels.append(choices)
            print(len(ids))
            response_dataframe = pd.DataFrame({
                'Id': ids,
                'Entity': entities,
                'Score': labels
            })
            response_dataframe = response_dataframe.groupby(['Id', 'Entity'], sort=False).agg(sum).reset_index()
            rule_groundings[rule_name] = rule_groundings[rule_name].merge(response_dataframe, on=['Id', 'Entity'], how='left')
            rule_groundings[rule_name]['Score'] = rule_groundings[rule_name]['Score'].apply(lambda x: x if isinstance(x, list) else ['Target of care/harm', 'Target of care/harm'])
            '''
            print(response_dataframe.shape)
            print(response_dataframe)
            print(rule_groundings[rule_name].shape)
            counter = 0
            for index, row in rule_groundings[rule_name].iterrows():
                if not isinstance(row['Score'], list):
                    counter += 1
                    #print(row)
            print(counter)
            raise Exception()
            '''
    #raise Exception()
    return rule_groundings


def main():
    data_input_path = sys.argv[1]
    rule_grounding_path = sys.argv[2]
    openai_response_input_path = sys.argv[3]
    output_path = sys.argv[4]
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
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(data_input_path)
    template_rule_groundings = prompt_data_loader.load_rule_groundings(rule_grounding_path, rules.keys())
    responses = prompt_data_loader.load_rule_grounding_batches(rules, openai_response_input_path)
    rule_groundings = transform_openai_response(template_rule_groundings, responses)
    scored_rule_groundings = mf_scoring.get_scored_groundings(rule_groundings, rules.keys(), 'gs')
    constraints = mf_scoring.get_mf_constraints(data_input_path)

    # few shot results
    results = {}
    foundation_instance_groupings = scored_rule_groundings['rule_one'].groupby(['Id'])
    for group_name, group in foundation_instance_groupings:
        max_row = group.iloc[group['Score'].argmax()]
        results[max_row['Id']] = {
            'MoralFrame': max_row['label']
        }
    role_instance_groupings = scored_rule_groundings['rule_two'].groupby(['Id', 'Entity'])
    for group_name, group in role_instance_groupings:
        max_row = group.iloc[group['Score'].argmax()]
        foundation_id_result = results[max_row['Id']]
        entity_result = {
            'Entity': max_row['Entity'],
            'Label': max_row['label']
        }
        if 'EntityRoles' in foundation_id_result:
            foundation_id_result['EntityRoles'].append(entity_result)
        else:
            foundation_id_result['EntityRoles'] = [entity_result]
        results[max_row['Id']] = foundation_id_result
    analysis_helper.write_json_file(output_path + '_few_shot.json', results)

    inference_model =  GurobiInferenceModel(rules, scored_rule_groundings, constraints)
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
    analysis_helper.write_json_file(output_path + '_ilp.json', results)

if __name__ == "__main__":
    main()
