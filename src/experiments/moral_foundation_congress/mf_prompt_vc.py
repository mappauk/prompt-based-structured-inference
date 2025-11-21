import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_vc_rule import LLMVCRule
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict
import time
from src.inference.gurobi_inference_model import GurobiInferenceModel
import src.helpers.scoring.mf_scoring as mf_scoring

def main():
    # hyperparamaters
    device_type = 'cuda'
    topk = 5
    temperature = 0.5
    num_votes = 10
    num_return_sequences = 2
    prompt_batch_size = 8
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    print('vc rule')
    #model, tokenizer = model_loader.load_mistral_instruct_model(device_type, eight_bit=True, flash_attention_2=True, return_dict=False)
    model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True, return_dict=False)

    # load data
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)
    data = data.iloc[1:4, :]

    #data = data.head(10)

    # generate moral foundation prompt format strings
    foundation_prompt = moral_prompting.generate_vc_prompt(constants.MF_VERB_CONF_SELF_PROBING_SYSTEM_PROMPT, constants.MF_VERB_CONF_SELF_PROBING_PROMPT_FORMAT, tokenizer)
    foundation_prompt_with_features = moral_prompting.generate_vc_prompt(constants.MF_VERB_CONF_SELF_PROBING_SYSTEM_PROMPT, constants.MF_VERB_CONF_SELF_PROBING_PROMPT_FORMAT_WITH_CONTEXT, tokenizer)

    # generate moral role prompt format strings
    role_prompt = moral_prompting.generate_vc_prompt(constants.ROLE_VERB_CONF_SELF_PROBING_SYSTEM_PROMPT, constants.ROLE_VERB_CONF_SELF_PROBING_PROMPT_FORMAT, tokenizer)
    role_prompt_with_features = moral_prompting.generate_vc_prompt(constants.ROLE_VERB_CONF_SELF_PROBING_SYSTEM_PROMPT, constants.ROLE_VERB_CONF_SELF_PROBING_PROMPT_FORMAT_WITH_CONTEXT, tokenizer)
    # load model
    #model, tokenizer = model_loader.load_test_model(device_type, eight_bit=False, flash_attention_2=False, return_dict=False)

    # define rules
    rule_one = LLMVCRule(
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
        foundation_prompt,
        num_votes,
        num_return_sequences
    )

    rule_two = LLMVCRule(
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
        role_prompt,
        num_votes,
        num_return_sequences
    )
    rule_three = LLMVCRule(
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
        foundation_prompt_with_features,
        num_votes,
        num_return_sequences
    )
    rule_four = LLMVCRule(
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
        role_prompt_with_features,
        num_votes,
        True
    )
    rules = {
        rule_one.name: rule_one, 
        rule_two.name: rule_two, 
        rule_three.name: rule_three, 
        rule_four.name: rule_four
    }

    # get rule groundings:
    start = time.time() # Record the start time
    rule_groundings = {}
    for rule_name, rule in rules.items():
        rule_groundings[rule_name] = rule.get_rule_groundings(data)
    scored_rule_groundings = mf_scoring.get_scored_groundings(rule_groundings, ['rule_one', 'rule_two', 'rule_three', 'rule_four'], 'vc')
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