import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_gz_rule import LLMGZRule
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict


def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 0
    num_variations = 10
    prompt_batch_size = 16
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3]
    # load data
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)
    # generate moral foundation prompt format strings
    foundation_prompts = moral_prompting.generate_one_pass_gz_moral_foundation_prompt_format(
        constants.GEN_Z_MF_LABEL_SENTENCES, 
        constants.GEN_Z_MF_EXAMPLE_FORMAT,
        num_shots,
        num_variations,
        example_path
    )
    foundation_prompts_with_features = moral_prompting.generate_one_pass_gz_moral_foundation_prompt_format(
        constants.GEN_Z_MF_LABEL_SENTENCES_WITH_CONTEXT, 
        constants.GEN_Z_MF_EXAMPLE_FORMAT, 
        num_shots,
        num_variations,
        example_path
    )
    # generate moral role prompt format strings
    role_prompts = moral_prompting.generate_one_pass_gz_moral_role_prompt_format(
        constants.GEN_Z_MF_ROLE_LABEL_SENTENCES, 
        constants.GEN_Z_MF_EXAMPLE_FORMAT, 
        num_shots,
        num_variations,
        example_path
    )
    role_prompts_with_features = moral_prompting.generate_one_pass_gz_moral_role_prompt_format(
        constants.GEN_Z_MF_ROLE_LABEL_SENTENCES_WITH_CONTEXT, 
        constants.GEN_Z_MF_EXAMPLE_FORMAT, 
        num_shots,
        num_variations,
        example_path
    )
    # load model
    model, tokenizer = model_loader.load_test_model(device_type)
    # define rules
    rule_one = LLMGZRule(
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
        constants.GEN_Z_MF_TWEET_FORMAT,
        num_variations
    )
    rule_two = LLMGZRule(
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
        constants.GEN_Z_MF_TWEET_FORMAT,
        num_variations
    )
    rule_three = LLMGZRule(
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
        constants.GEN_Z_MF_TWEET_FORMAT,
        num_variations
    )
    rule_four = LLMGZRule(
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
        constants.GEN_Z_MF_TWEET_FORMAT,
        num_variations
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
    prompt_data_loader.save_rule_groundings(rules, data, output_path)
    

if __name__ == "__main__":
    main()
