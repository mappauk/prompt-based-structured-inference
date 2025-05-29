import sys
import numpy as np
import pandas as pd
from src.rules.llm_gs_rule import LLMGSRule
import src.helpers.loaders.model_loader as model_loader
import src.helpers.prompting.coref_prompting as coref_prompting
import src.helpers.loaders.ontonotes_dataset_loader as ontonotes_dataset_loader
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict
import src.helpers.prompting.coref_prompt_constants as constants

def main():
    # hyperparamaters
    device_type = 'cuda'
    prompt_batch_size = 8
    topk = 5
    temperature = 0.5
    num_return_sequences = 2
    max_generate_tokens = 3
    num_votes = 2
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
    coref_prompts = coref_prompting.generate_gs_prompts(
        num_shots,
        example_path,
        tokenizer,
        both_per_shot=False
    )

    model, tokenizer = model_loader.load_test_model(device_type)

    # define rules
    rule_one = LLMGSRule(
        'rule_one',
        ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
        ['coreferent', 'distinct'],
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
        num_votes,
        max_generate_tokens,
        num_return_sequences
    )
    rules = {
        rule_one.name: rule_one, 
    }
    prompt_data_loader.save_rule_groundings(rules, data, output_path)

if __name__ == "__main__":

    main()
