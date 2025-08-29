import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_tf_rule import LLMTFRule
import src.helpers.prompting.econ_prompting as econ_prompting
import src.helpers.prompting.econ_prompt_constants as constants
import src.helpers.loaders.econ_indicators_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
from src.rules.rule_type import RuleType
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from typing import Dict
import os


def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 2
    prompt_batch_size = 8
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3]

    #model, tokenizer = model_loader.load_mistral_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    #model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)
    # load data
    qual_data = dataset_loader.load_econ_indicators_qual(input_path + 'agreed_qual_dict.pkl', input_path + 'full_data_backup_sep5.db')
    quant_data = dataset_loader.load_econ_indicators_quant(input_path + 'agreed_quant_dict.pkl')
    qual_data = qual_data.head(10)
    quant_data = quant_data.head(10)

    # generate article level prompt format strings
    article_type_prompts = econ_prompting.generate_tf_prompts(constants.TF_ARTICLE_TYPE_SYSTEM_PROMPT, constants.TF_ARTICLE_TYPE_EXAMPLE_PROMPT, num_shots, example_path, tokenizer, "article_type")
    article_condition_prompts = econ_prompting.generate_tf_prompts(constants.TF_ARTICLE_CONDITIONS_SYSTEM_PROMPT, constants.TF_ARTICLE_CONDITIONS_USER_PROMPT, num_shots, example_path, tokenizer, "article_cond")
    article_direction_prompts = econ_prompting.generate_tf_prompts(constants.TF_ARTICLE_DIRECTION_SYSTEM_PROMPT, constants.TF_ARTICLE_DIRECTION_USER_PROMPT, num_shots, example_path, tokenizer, "article_dir")

    # generate quantity level prompt format strings
    quantity_type_prompts = econ_prompting.generate_tf_prompts(constants.TF_QUANTITY_TYPE_SYSTEM_PROMPT, constants.TF_QUANTITY_TYPE_USER_PROMPT, num_shots, example_path, tokenizer, "quantity_type")
    quantity_indicator_prompts = econ_prompting.generate_tf_prompts(constants.TF_QUANTITY_INDICATOR_SYSTEM_PROMPT, constants.TF_QUANTITY_INDICATOR_USER_PROMPT, num_shots, example_path, tokenizer, "quantity_ind")
    quantity_polarity_prompts = econ_prompting.generate_tf_prompts(constants.TF_QUANTITY_POLARITY_SYSTEM_PROMPT, constants.TF_QUANTITY_POLARITY_USER_PROMPT, num_shots, example_path, tokenizer, "quantity_pol")



    # load model
    model, tokenizer = model_loader.load_test_model(device_type)

    # define rules
    article_econ_type = LLMTFRule(
        'rule_one',
        ['Id', 'Text'],
        constants.ARTICLE_ECONOMIC_TYPE_LABELS,
        'AT_{Id}_{label}',
        'RuleOne_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        article_type_prompts,
    )

    article_econ_condition = LLMTFRule(
        'rule_two',
        ['Id', 'Text'],
        constants.ARTICLE_ECONOMIC_CONDITIONS_LABELS,
        'AC_{Id}_{label}',
        'RuleTwo_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        article_condition_prompts,
    )

    article_econ_direction = LLMTFRule(
        'rule_three',
        ['Id', 'Text'],
        constants.ARTICLE_ECONOMIC_DIRECTION_LABELS,
        'AD_{Id}_{label}',
        'RuleThree_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        article_direction_prompts,
    )

    quantity_type = LLMTFRule(
        'rule_four',
        ['Id', 'IndicatorText', 'Context'],
        constants.QUANTITY_TYPE_LABELS,
        'QT_{Id}_{label}',
        'RuleFour_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        quantity_type_prompts,
    )

    quantity_indicator = LLMTFRule(
        'rule_four',
        ['Id', 'IndicatorText', 'Context'],
        constants.QUANTITY_INDICATOR_LABELS,
        'QI_{Id}_{label}',
        'RuleFive_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        quantity_indicator_prompts,
    )

    quantity_polarity = LLMTFRule(
        'rule_four',
        ['Id', 'IndicatorText', 'Context'],
        constants.QUANTITY_POLARITY_LABELS,
        'QP_{Id}_{label}',
        'RuleSix_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        quantity_polarity_prompts,
    )


    qual_rules = {
        article_econ_type.name: article_econ_type,
        article_econ_condition.name: article_econ_condition,
        article_econ_direction.name: article_econ_direction,
    }

    quant_rules = {
        quantity_type.name: quantity_type,
        quantity_indicator.name: quantity_indicator,
        quantity_polarity.name: quantity_polarity
    }

    # get rule groundings:
    prompt_data_loader.save_rule_groundings(qual_rules, qual_data, output_path)
    prompt_data_loader.save_rule_groundings(quant_rules, quant_data, output_path)

if __name__ == "__main__":
    main()