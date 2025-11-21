import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_tf_rule import LLMTFRule
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
from src.rules.rule_type import RuleType
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from typing import Dict
import os
import time
from src.inference.gurobi_inference_model import GurobiInferenceModel
import src.helpers.scoring.mf_scoring as mf_scoring

def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 2
    prompt_batch_size = 8
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3]
    print('tf rule')
    #model, tokenizer = model_loader.load_mistral_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    # load data
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)
    data = data.iloc[1:4, :]

    # generate moral foundation prompt format strings
    foundation_prompts = moral_prompting.generate_tf_prompts(
        constants.MF_TF_SYSTEM_PROMPT, 
        constants.MORAL_FOUNDATION_PROMPT_EXAMPLE_FORMAT,
        num_shots, 
        os.path.join(example_path, 'moral_foundation_examples.json'),
        tokenizer
    )
    foundation_prompts_with_features = moral_prompting.generate_tf_prompts(
        constants.MF_TF_SYSTEM_PROMPT, 
        constants.MORAL_FOUNDATION_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
        num_shots,
        os.path.join(example_path, 'moral_foundation_examples.json'),
        tokenizer
    )
    # generate moral role prompt format strings
    role_prompts = moral_prompting.generate_tf_prompts(
        constants.MR_TF_SYSTEM_PROMPT, 
        constants.MORAL_ROLE_PROMPT_EXAMPLE_FORMAT,
        num_shots,
        os.path.join(example_path, 'moral_role_examples.json'),
        tokenizer
    )
    role_prompts_with_features = moral_prompting.generate_tf_prompts(
        constants.MR_TF_SYSTEM_PROMPT, 
        constants.MORAL_ROLE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
        num_shots,
        os.path.join(example_path, 'moral_role_examples.json'),
        tokenizer
    )
    # load model
    #model, tokenizer = model_loader.load_test_model(device_type)

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
        device_type,
        foundation_prompts,
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
        device_type,
        role_prompts,
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
        device_type,
        foundation_prompts_with_features,
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
        device_type,
        role_prompts_with_features,
    )
    rules = {
        rule_one.name: rule_one, 
        rule_two.name: rule_two, 
        rule_three.name: rule_three, 
        rule_four.name: rule_four
    }
    start = time.time() # Record the start time
    rule_groundings = {}
    for rule_name, rule in rules.items():
        rule_groundings[rule_name] = rule.get_rule_groundings(data)
    scored_rule_groundings = mf_scoring.get_scored_groundings(rule_groundings, ['rule_one', 'rule_two', 'rule_three', 'rule_four'], 'tf')
    elapsed = time.time() - start # Calculate elapsed time
    print(f"Prompt Elapsed time: {elapsed:.2f} seconds")
    rule_constraints = mf_scoring.get_mf_constraints(input_path)
    inference_model = GurobiInferenceModel(rules, scored_rule_groundings,  rule_constraints)
    start = time.time() # Record the start time
    inference_model.inference()
    elapsed = time.time() - start # Calculate elapsed time
    print(f"Inference Elapsed time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
