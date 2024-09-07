import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_mv_rule import LLMMVRule
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.analysis.analysis_helper as analysis_helper
import src.helpers.loaders.model_loader as model_loader

from src.rules.rule_type import RuleType
from src.inference.gurobi_inference_model import GurobiInferenceModel
from typing import Dict


def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 2
    topk = 5
    temperature = 0.5
    prompt_batch_size = 8
    num_votes = 10
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
    role_prompts = moral_prompting.generate_one_pass_tf_moral_role_prompt_format(
        constants.MORAL_ROLE_IDENTIFICATION_ONE_PASS_TF,
        constants.MORAL_ROLE_PROMPT_EXAMPLE_FORMAT, 
        num_shots, 
        example_path
    )
    
    # load model
    model, tokenizer = model_loader.load_test_model(device_type)
    # define rules
    rule_one = LLMMVRule(
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
        foundation_prompts,
        num_votes,
        True
    )
    rule_two = LLMMVRule(
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
        role_prompts,
        num_votes,
        True
    )

    # get rule groundings:
    foundation_predictions = rule_one.get_rule_groundings(data)
    role_predictions = rule_two.get_rule_groundings(data)

    # save results
    results = {}
    # cluster by id
    foundation_instance_groupings = foundation_predictions.groupby(['Id'])
    for group_name, group in foundation_instance_groupings:
        max_row = group.iloc[group['Score'].argmax()]
        results[max_row['Id']] = {
            'MoralFrame': max_row['label']
        }

    role_instance_groupings = role_predictions.groupby(['Id', 'Entity'])
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

    analysis_helper.write_json_file(output_path, results)

if __name__ == "__main__":
    main()