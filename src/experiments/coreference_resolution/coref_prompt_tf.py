import sys
import numpy as np
import pandas as pd
from src.rules.llm_tf_rule import LLMTFRule
import src.helpers.loaders.model_loader as model_loader
import src.helpers.prompting.coref_prompting as coref_prompting
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict


def main():
    # hyperparamaters
    device_type = 'cpu'
    topk = 5
    temperature = 0.5
    prompt_batch_size = 2
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3] 
    num_shots = int(sys.argv[4])
    seq2seq = sys.argv[5] == "true"
    # load data
    data = genia_dataset_loader.preprocess_genia_coref(input_path)

    # generate moral foundation prompt format strings
    coref_prompts = coref_prompting.generate_one_pass_tf_coref_prompt_format(
        num_shots,
        example_path
    )

    # load model
    if seq2seq: 
        model, tokenizer = model_loader.load_flan_model(device_type)
    else:
        model, tokenizer = model_loader.load_mistral_model(device_type)
    # define rules
    rule_one = LLMTFRule(
        'rule_one',
        ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
        ['coref', 'nocoref'],
        'CF_{doc_id}_{entity1_id}_{entity2_id}_{label}',
        'RuleOne_{doc_id}_{entity1_id}_{entity2_id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        coref_prompts,
        True,
        seq2seq
    )
    rules = {
        rule_one.name: rule_one, 
    }
    prompt_data_loader.save_rule_groundings(rules, data, output_path)

if __name__ == "__main__":
    main()
