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
    prompt_batch_size = 8
    output_path = sys.argv[1]
    example_path = sys.argv[2]
    num_shots = int(sys.argv[3])
    cosine_similarity = sys.argv[4] == 'true'
    include_transcript = sys.argv[5] == 'true'
    prompt_map_key = None
    model, tokenizer = model_loader.load_mistral_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    #model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    # load data
    data = dataset_loader.load_delidata(include_transcript)
    #print(data.shape)
    #print(data)
    #data = data.head(60)
    
    # define prompting constants
    if not include_transcript:
        level_one_system_prompt =  constants.LEVEL_ONE_SYSTEM_PROMPT
        level_two_system_prompt = constants.LEVEL_TWO_SYSTEM_PROMPT
        level_one_example_format = constants.LEVEL_ONE_EXAMPLE_FORMAT
        level_two_example_format = constants.LEVEL_TWO_EXAMPLE_FORMAT
        level_one_prior_system_prompt = constants.LEVEL_ONE_PRIOR_SYSTEM_PROMPT
        level_two_prior_system_prompt = constants.LEVEL_TWO_PRIOR_SYSTEM_PROMPT
        level_one_prior_example_prompt = constants.LEVEL_ONE_PRIOR_EXAMPLE_FORMAT
        level_two_prior_example_prompt = constants.LEVEL_TWO_PRIOR_EXAMPLE_FORMAT
        level_one_prior_gold_example_prompt = constants.LEVEL_ONE_PRIOR_GOLD_EXAMPLE_FORMAT
        level_two_prior_gold_example_prompt = constants.LEVEL_TWO_PRIOR_GOLD_EXAMPLE_FORMAT
    else:
        level_one_system_prompt =  constants.LEVEL_ONE_SYSTEM_PROMPT_W_TRANSCRIPT
        level_two_system_prompt = constants.LEVEL_TWO_SYSTEM_PROMPT_W_TRANSCRIPT
        level_one_example_format = constants.LEVEL_ONE_EXAMPLE_FORMAT_W_TRANSCRIPT
        level_two_example_format = constants.LEVEL_TWO_EXAMPLE_FORMAT_W_TRANSCRIPT
        level_one_prior_system_prompt = constants.LEVEL_ONE_PRIOR_SYSTEM_PROMPT_W_TRANSCRIPT
        level_two_prior_system_prompt = constants.LEVEL_TWO_PRIOR_SYSTEM_PROMPT_W_TRANSCRIPT
        level_one_prior_example_prompt = constants.LEVEL_ONE_PRIOR_EXAMPLE_FORMAT_W_TRANSCRIPT
        level_two_prior_example_prompt = constants.LEVEL_TWO_PRIOR_EXAMPLE_FORMAT_W_TRANSCRIPT
        level_one_prior_gold_example_prompt = constants.LEVEL_ONE_PRIOR_GOLD_EXAMPLE_FORMAT_W_TRANSCRIPT
        level_two_prior_gold_example_prompt = constants.LEVEL_TWO_PRIOR_GOLD_EXAMPLE_FORMAT_W_TRANSCRIPT
    # load model
    if cosine_similarity:
        level_one_prompts, level_two_prompts = delidata_prompting.delidata_prompting_cosine_similarity(
            tokenizer, 
            num_shots, 
            data, 
            level_one_system_prompt,
            level_two_system_prompt,
            ['message_id', 'original_text', 'annotation_type', 'annotation_target'] + ([] if not include_transcript else ['transcript']),
            level_one_example_format,
            level_two_example_format,
            level_one_example_format,
            level_two_example_format)
        level_one_prior_prompts, level_two_prior_prompts = delidata_prompting.delidata_prompting_cosine_similarity(
            tokenizer,
            num_shots, 
            data, 
            level_one_prior_system_prompt,
            level_two_prior_system_prompt,
            ['message_id', 'original_text', 'annotation_type', 'annotation_target', 'previous_original_text', 'previous_annotation_gold_type', 'previous_annotation_gold_target'] + ([] if not include_transcript else ['transcript']),
            level_one_prior_gold_example_prompt,
            level_two_prior_gold_example_prompt,
            level_one_prior_example_prompt,
            level_two_prior_example_prompt)
        prompt_map_key="message_id"
    else:
        level_one_prompts = delidata_prompting.delidata_prompting(
            tokenizer,
            level_one_system_prompt,
            level_one_example_format,
            num_shots,
            example_path + 'delidata_level_one_examples.json',
            constants.LEVEL_1_TO_CHOICE_MAP
        )
        level_two_prompts = delidata_prompting.delidata_prompting(
            tokenizer,
            level_two_system_prompt,
            level_two_example_format,
            num_shots,
            example_path + 'delidata_level_two_examples.json',
            constants.LEVEL_2_TO_CHOICE_MAP
        )
        level_one_prior_prompts = delidata_prompting.delidata_prompting(
            tokenizer,
            level_one_prior_system_prompt,
            level_one_prior_example_prompt,
            num_shots,
            example_path + 'delidata_level_one_examples.json',
            constants.LEVEL_1_TO_CHOICE_MAP
        )

        level_two_prior_prompts = delidata_prompting.delidata_prompting(
            tokenizer,
            level_two_prior_system_prompt,
            level_two_prior_example_prompt,
            num_shots,
            example_path + 'delidata_level_two_examples.json',
            constants.LEVEL_2_TO_CHOICE_MAP
        )
    
    #model, tokenizer = model_loader.load_test_model(device_type)

    # define rules
    rule_one = LLMMCRule(
        'rule_one',
        ['message_id', 'original_text'] + ([] if not include_transcript else ['transcript']),
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
        ['message_id', 'original_text'] + ([] if not include_transcript else ['transcript']),
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
        ['message_id', 'previous_message_id','original_text', 'previous_original_text', 'previous_annotation_type'] + ([] if not include_transcript else ['transcript']),
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
        ['message_id', 'previous_message_id', 'original_text', 'previous_original_text', 'previous_annotation_target'] + ([] if not include_transcript else ['transcript']),
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
