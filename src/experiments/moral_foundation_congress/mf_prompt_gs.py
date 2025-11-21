import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_gs_rule import LLMGSRule
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict
import os
import time
from src.inference.gurobi_inference_model import GurobiInferenceModel
import src.helpers.scoring.mf_scoring as mf_scoring

def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 2
    foundations_per_shot = 1
    topk = 5
    temperature = 0.5
    num_votes = 10
    num_return_sequences = 2
    max_generate_tokens = 10
    prompt_batch_size = 8
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3]
    print('gs rule')
    #model, tokenizer = model_loader.load_mistral_instruct_model(device_type, eight_bit=True, flash_attention_2=True, return_dict=False)
    model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True, return_dict=False)
    # load data
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)
    data = data.iloc[1:4, :]

    # generate moral foundation prompt format strings
    foundation_prompts = moral_prompting.generate_gs_prompt(
        constants.MF_GS_SYSTEM_PROMPT, 
        constants.MF_GS_EXAMPLE_FORMAT,
        num_shots, 
        os.path.join(example_path, 'moral_foundation_examples.json'),
        tokenizer,
        foundations_per_shot
    )
    foundation_prompts_with_features = moral_prompting.generate_gs_prompt(
        constants.MF_GS_SYSTEM_PROMPT, 
        constants.MF_GS_EXAMPLE_FORMAT_WITH_FEATURES,
        num_shots,
        os.path.join(example_path, 'moral_foundation_examples.json'),
        tokenizer,
        foundations_per_shot
    )
    # generate moral role prompt format strings
    role_prompts = moral_prompting.generate_gs_prompt(
        constants.MR_GS_SYSTEM_PROMPT, 
        constants.MR_GS_EXAMPLE_FORMAT,
        num_shots,
        os.path.join(example_path, 'moral_role_examples.json'),
        tokenizer,
        foundations_per_shot
    )
    role_prompts_with_features = moral_prompting.generate_gs_prompt(
        constants.MR_GS_SYSTEM_PROMPT, 
        constants.MR_GS_EXAMPLE_FORMAT_WITH_FEATURES,
        num_shots,
        os.path.join(example_path, 'moral_role_examples.json'),
        tokenizer,
        foundations_per_shot
    )

    # load model
    #model, tokenizer = model_loader.load_test_model(device_type, return_dict=False)
    # define rules
    rule_one = LLMGSRule(
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
        max_generate_tokens,
        num_return_sequences
    )
    rule_two = LLMGSRule(
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
        max_generate_tokens,
        num_return_sequences
    )
    rule_three = LLMGSRule(
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
        foundation_prompts_with_features,
        num_votes,
        max_generate_tokens,
        num_return_sequences
    )
    rule_four = LLMGSRule(
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
        role_prompts_with_features,
        num_votes,
        max_generate_tokens,
        num_return_sequences
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
    scored_rule_groundings = mf_scoring.get_scored_groundings(rule_groundings, ['rule_one', 'rule_two', 'rule_three', 'rule_four'], 'gs')
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