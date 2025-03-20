import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_gc_rule import LLMGCRule
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict
import os


def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 0
    num_variations = 10
    foundations_per_shot = 1
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3]
    # load data
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)

    #model, tokenizer = model_loader.load_mistral_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)

    # generate moral foundation prompt format strings
    foundation_prompts = moral_prompting.generate_gc_prompt(
        constants.MF_GC_SYSTEM_PROMPT,
        constants.MF_GC_LABEL_SENTENCES,
        constants.MF_GC_EXAMPLE_FORMAT,
        num_shots,
        num_variations,
        os.path.join(example_path, 'moral_foundation_examples.json'),
        tokenizer,
        foundations_per_shot
    )
    foundation_prompts_with_features = moral_prompting.generate_gc_prompt(
        constants.MF_GC_SYSTEM_PROMPT,
        constants.MF_GC_LABEL_SENTENCES_WITH_FEATURES,
        constants.MF_GC_EXAMPLE_FORMAT,
        num_shots,
        num_variations,
        os.path.join(example_path, 'moral_foundation_examples.json'),
        tokenizer,
        foundations_per_shot
    )
    # generate moral role prompt format strings
    role_prompts = moral_prompting.generate_gc_prompt(
        constants.MR_GC_SYSTEM_PROMPT,
        constants.MR_GC_LABEL_SENTENCES,
        constants.MF_GC_EXAMPLE_FORMAT,
        num_shots,
        num_variations,
        os.path.join(example_path, 'moral_role_examples.json'),
        tokenizer,
        foundations_per_shot
    )
    role_prompts_with_features = moral_prompting.generate_gc_prompt(
        constants.MR_GC_SYSTEM_PROMPT,
        constants.MR_GC_LABEL_SENTENCES_WITH_FEATURES,
        constants.MF_GC_EXAMPLE_FORMAT,
        num_shots,
        num_variations,
        os.path.join(example_path, 'moral_role_examples.json'),
        tokenizer,
        foundations_per_shot
    )
    generation_format = constants.MF_GC_GENERATION_FORMAT
    # load model
    #model, tokenizer = model_loader.load_test_model(device_type)
    # define rules
    rule_one = LLMGCRule(
        'rule_one',
        ['Id', 'Tweet'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleOne_{Id}_{label}',
        RuleType.MULTI_CLASS,
        model, 
        tokenizer, 
        device_type,
        foundation_prompts,
        generation_format,
        num_variations
    )
    rule_two = LLMGCRule(
        'rule_two',
        ['Id', 'Tweet', 'Entity'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleTwo_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS,
        model, 
        tokenizer, 
        device_type,
        role_prompts,
        generation_format,
        num_variations
    )
    rule_three = LLMGCRule(
        'rule_three',
        ['Id', 'Tweet', 'Topic', 'Ideology'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleThree_{Id}_{label}',
        RuleType.MULTI_CLASS,
        model, 
        tokenizer, 
        device_type,
        foundation_prompts_with_features,
        generation_format,
        num_variations
    )
    rule_four = LLMGCRule(
        'rule_four',
        ['Id', 'Tweet', 'Entity', 'Ideology', 'Topic'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleFour_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS,
        model, 
        tokenizer, 
        device_type,
        role_prompts_with_features,
        generation_format,
        num_variations
    )
    rules = {
        rule_one.name: rule_one, 
        rule_two.name: rule_two, 
        rule_three.name: rule_three, 
        rule_four.name: rule_four
    }
    prompt_data_loader.save_rule_groundings(rules, data, output_path)

if __name__ == "__main__":
    main()
