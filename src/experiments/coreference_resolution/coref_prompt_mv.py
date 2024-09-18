import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_mv_rule import LLMMVRule
import src.helpers.loaders.model_loader as model_loader
import src.helpers.prompting.coref_prompting as coref_prompting
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict


def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 2
    topk = 5
    num_votes = 5
    temperature = 0.5
    prompt_batch_size = 4
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3] 
    # load data
    #data = ontonotes_dataset_loader.preprocess_ontonotes_coref(input_path)
    data = genia_dataset_loader.preprocess_genia_coref(input_path)

    # generate moral foundation prompt format strings
    coref_prompts = coref_prompting.generate_one_pass_tf_coref_prompt_format(
        num_shots, 
        example_path
    )
    # load model
    model, tokenizer = model_loader.load_mistral_model(device_type)
    # define rules
    rule_one = LLMMVRule(
        'rule_one',
        ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
        [],
        'CF_{doc_id}_{entity1_id}_{entity2_id}',
        'RuleOne_{doc_id}_{entity1_id}_{entity2_id}',
        RuleType.BINARY,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        coref_prompts,
        num_votes,
        True
    )
    rules = {
        rule_one.name: rule_one, 
    }
    prompt_data_loader.save_rule_groundings(rules, data, output_path)


if __name__ == "__main__":
    main()
