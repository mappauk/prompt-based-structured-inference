import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_tf_rule import LLMTFRule
import src.helpers.moral_prompting as moral_prompting
import src.helpers.prompt_constants as constants
import src.helpers.dataset_loader as dataset_loader
from src.rules.rule_type import RuleType
from src.inference.gurobi_inference_model import GurobiInferenceModel
from typing import Dict


def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 2
    topk = 5
    temperature = 0.5
    prompt_batch_size = 2
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3]
    # load data
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)
    # generate moral foundation prompt format strings
    foundation_prompts = moral_prompting.generate_one_pass_tf_moral_foundation_prompt_format(
        constants.MORAL_FOUNDATION_IDENTIFICATION_ONE_PASS_TF, 
        constants.MORAL_FOUNDATION_PROMPT_EXAMPLE_FORMAT, 
        num_shots, 
        example_path
    )
    foundation_prompts_with_features = moral_prompting.generate_one_pass_tf_moral_foundation_prompt_format(
        constants.MORAL_FOUNDATION_IDENTIFICATION_ONE_PASS_WITH_FEATURES_TF, 
        constants.MORAL_FOUNDATION_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT, 
        num_shots, 
        example_path
    )
    # generate moral role prompt format strings
    role_prompts = moral_prompting.generate_one_pass_tf_moral_role_prompt_format(
        constants.MORAL_ROLE_IDENTIFICATION_ONE_PASS_TF,
        constants.MORAL_ROLE_PROMPT_EXAMPLE_FORMAT, 
        num_shots, 
        example_path
    )
    role_prompts_with_features = moral_prompting.generate_one_pass_tf_moral_role_prompt_format(
        constants.MORAL_ROLE_IDENTIFICATION_ONE_PASS_WITH_FEATURES_TF,
        constants.MORAL_ROLE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT, 
        num_shots, 
        example_path
    )
    # load model
    model, tokenizer = moral_prompting.load_test_model()
    # define rules
    rule_one = LLMTFRule(
        'rule_one',
        ['Id', 'Tweet'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleOne_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        foundation_prompts
    )
    rule_two = LLMTFRule(
        'rule_two',
        ['Id', 'Tweet', 'Entity'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleTwo_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        role_prompts
    )
    rule_three = LLMTFRule(
        'rule_three',
        ['Id', 'Tweet', 'Topic', 'Ideology'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleThree_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        foundation_prompts_with_features
    )
    rule_four = LLMTFRule(
        'rule_four',
        ['Id', 'Tweet', 'Entity', 'Ideology', 'Topic'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleFour_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        role_prompts_with_features
    )
    rules = {
        rule_one.name: rule_one, 
        rule_two.name: rule_two, 
        rule_three.name: rule_three, 
        rule_four.name: rule_four
    }
    # get rule groundings:
    rule_groundings = {}
    for rule_name, rule in rules.items():
        rule_groundings[rule_name] = rule.get_rule_groundings(data)
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
        role_groupings = rule_groundings['rule_four'].groupby(['Ideology', 'Topic', 'Entity'])
        for group_name, group in role_groupings:
            if group.shape[0] > 1:
                start_index = 1
                for index, row in group.iterrows():
                    entity_one = head_dict[row['HeadVariable']]
                    polarity = constants.POLARITY_MAP.get(row['label'], -1)
                    tweet_id = row['Id']
                    if polarity != -1:
                        counter = 0
                        for index, row in group.iterrows():
                            if counter >= start_index:
                                polarity_two = constants.POLARITY_MAP.get(row['label'], -1)
                                if tweet_id != row['Id'] and polarity_two != -1 and polarity_two != polarity:
                                    entity_two = head_dict[row['HeadVariable']]
                                    m.addConstr(entity_one + entity_two <= 1)
                            counter += 1
                    start_index += 1
    custom_rule_constraints = [ constr_one, constr_two, constr_three]
    # perform inference
    inference_model = GurobiInferenceModel(rules, rule_groundings, data,  custom_rule_constraints)
    variable_assignments = inference_model.inference()
    # save results
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
    dataset_loader.write_json_file(output_path, results)

if __name__ == "__main__":
    main()