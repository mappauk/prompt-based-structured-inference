import sys
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_mc_rule import LLMMCRule
import src.helpers.prompting.delidata_prompt_constants as constants
import src.helpers.loaders.delidata_dataset_loader as dataset_loader
import src.helpers.prompting.delidata_prompting as delidata_prompting
import src.helpers.loaders.model_loader as model_loader
from src.rules.rule_type import RuleType
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from typing import Dict
import os

def main():
    # hyperparamaters
    device_type = 'cuda'
    cosine_similarity_examples = True
    num_shots = 0
    prompt_batch_size = 2
    output_path = sys.argv[1]
    example_path = sys.argv[2]
    prompt_map_key = None
    model, tokenizer = model_loader.load_mistral_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    #model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    # load data
    data = dataset_loader.load_delidata()
    #print(data.shape)
    #print(data)
    #data = data.head(2)

    # load model
    if cosine_similarity_examples:
        level_one_prompts, level_two_prompts = delidata_prompting.delidata_prompting_cosine_similarity(
            tokenizer, 
            num_shots, 
            data, 
            constants.LEVEL_ONE_SYSTEM_PROMPT,
            constants.LEVEL_TWO_SYSTEM_PROMPT,
            ['message_id', 'original_text', 'annotation_type', 'annotation_target'],
            constants.LEVEL_ONE_EXAMPLE_FORMAT,
            constants.LEVEL_TWO_EXAMPLE_FORMAT)
        level_one_prior_prompts, level_two_prior_prompts = delidata_prompting.delidata_prompting_cosine_similarity(
            tokenizer, 
            num_shots, 
            data, 
            constants.LEVEL_ONE_PRIOR_SYSTEM_PROMPT,
            constants.LEVEL_TWO_PRIOR_SYSTEM_PROMPT,
            ['message_id', 'original_text', 'annotation_type', 'annotation_target', 'previous_original_text', 'previous_annotation_gold_type', 'previous_annotation_gold_target'],
            constants.LEVEL_ONE_PRIOR_GOLD_EXAMPLE_FORMAT,
            constants.LEVEL_TWO_PRIOR_GOLD_EXAMPLE_FORMAT)
        prompt_map_key="message_id"
    else:
        level_one_prompts = delidata_prompting.delidata_prompting(
            tokenizer,
            constants.LEVEL_ONE_SYSTEM_PROMPT,
            constants.LEVEL_ONE_EXAMPLE_FORMAT,
            num_shots,
            example_path + 'delidata_level_one_examples.json',
            constants.LEVEL_1_TO_CHOICE_MAP
        )
        level_two_prompts = delidata_prompting.delidata_prompting(
            tokenizer,
            constants.LEVEL_TWO_SYSTEM_PROMPT,
            constants.LEVEL_TWO_EXAMPLE_FORMAT,
            num_shots,
            example_path + 'delidata_level_two_examples.json',
            constants.LEVEL_2_TO_CHOICE_MAP
        )
        level_one_prior_prompts = delidata_prompting.delidata_prompting(
            tokenizer,
            constants.LEVEL_ONE_PRIOR_SYSTEM_PROMPT,
            constants.LEVEL_ONE_PRIOR_EXAMPLE_FORMAT,
            num_shots,
            example_path + 'delidata_level_one_examples.json',
            constants.LEVEL_1_TO_CHOICE_MAP
        )

        level_two_prior_prompts = delidata_prompting.delidata_prompting(
            tokenizer,
            constants.LEVEL_TWO_PRIOR_SYSTEM_PROMPT,
            constants.LEVEL_TWO_PRIOR_EXAMPLE_FORMAT,
            num_shots,
            example_path + 'delidata_level_two_examples.json',
            constants.LEVEL_2_TO_CHOICE_MAP
        )
    
    model, tokenizer = model_loader.load_test_model(device_type)

    # define rules
    rule_one = LLMMCRule(
        'rule_one',
        ['message_id', 'original_text'],
        constants.LEVEL_1_LABELS,
        'LevelOne_{message_id}_{label}',
        'RuleOne_{message_id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        level_one_prompts,
        constants.LEVEL_1_CHOICES,
        prompt_map_key=prompt_map_key
    )
    rule_two = LLMMCRule(
        'rule_two',
        ['message_id', 'original_text'],
        constants.LEVEL_2_LABELS,
        'LevelTwo_{message_id}_{label}',
        'RuleTwo_{message_id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        level_two_prompts,
        constants.LEVEL_2_CHOICES,
        prompt_map_key=prompt_map_key
    )

    rule_three = LLMMCRule(
        'rule_three',
        ['message_id', 'previous_message_id','original_text', 'previous_original_text', 'previous_annotation_type'],
        constants.LEVEL_1_LABELS,
        'LevelOnePrior_{message_id}_{previous_message_id}_{previous_annotation_type}_{label}',
        'RuleThree_{message_id}_{previous_message_id}_{previous_annotation_type}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        level_one_prior_prompts,
        constants.LEVEL_1_CHOICES,
        prompt_map_key=prompt_map_key
    )
    rule_four = LLMMCRule(
        'rule_four',
        ['message_id', 'original_text', 'previous_original_text', 'previous_annotation_target'],
        constants.LEVEL_2_LABELS,
        'LevelTwoPrior_{message_id}_{previous_message_id}_{previous_annotation_target}_{label}',
        'RuleFour_{message_id}_{previous_message_id}_{previous_annotation_target}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer,
        device_type,
        level_two_prior_prompts,
        constants.LEVEL_2_CHOICES,
        prompt_map_key=prompt_map_key
    )
    rules = {
        rule_one.name: rule_one,
        rule_two.name: rule_two,
        rule_three.name: rule_three,
        rule_four.name: rule_four
    }
    # get rule groundings:
    prompt_data_loader.save_rule_groundings(rules, data, output_path)

if __name__ == "__main__":
    main()
