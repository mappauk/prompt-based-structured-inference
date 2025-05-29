import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_gc_rule import LLMGCRule
import src.helpers.loaders.model_loader as model_loader
import src.helpers.prompting.coref_prompting as coref_prompting
import src.helpers.prompting.coref_prompt_constants as constants
import src.helpers.loaders.ontonotes_dataset_loader as ontonotes_dataset_loader
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict


def main():
    # hyperparamaters
    device_type = 'cuda'
    num_variations = 1
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3]
    num_shots = int(sys.argv[4])

    # load data
    data = ontonotes_dataset_loader.preprocess_ontonotes_coref(input_path)
    #data = genia_dataset_loader.preprocess_genia_coref(input_path)
    data = data.head(10)
    print(data)
    #model, tokenizer = model_loader.load_flan_model(device_type)
    model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)

    # generate moral foundation prompt format strings
    coref_prompts = coref_prompting.generate_gc_prompt(num_shots, num_variations, example_path, tokenizer)

    # load model
    model, tokenizer = model_loader.load_test_model(device_type)

    # define rules
    rule_one = LLMGCRule(
        'rule_one',
        ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
        ['coreferent', 'distinct'],
        'CF_{doc_id}_{entity1_id}_{entity2_id}_{label}',
        'RuleOne_{doc_id}_{entity1_id}_{entity2_id}_{label}',
        RuleType.MULTI_CLASS,
        model,
        tokenizer,
        device_type,
        coref_prompts,
        constants.COREF_GENERATION_FORMAT,
        num_variations
    )
    rules = {
        rule_one.name: rule_one, 
    }
    prompt_data_loader.save_rule_groundings(rules, data, output_path)

if __name__ == "__main__":
    main()
