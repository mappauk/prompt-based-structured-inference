import sys
import numpy as np
import pandas as pd
from src.rules.llm_tf_rule import LLMTFRule
import src.helpers.loaders.model_loader as model_loader
import src.helpers.prompting.coref_prompting as coref_prompting
import src.helpers.loaders.ontonotes_dataset_loader as ontonotes_dataset_loader
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict
import time
from src.inference.gurobi_inference_model import GurobiInferenceModel
import src.helpers.scoring.coref_scoring as coref_scoring

def main():
    # hyperparamaters
    device_type = 'cuda'
    prompt_batch_size = 8
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3] 
    num_shots = 0

    print('tf rule')
    # load data
    data = genia_dataset_loader.preprocess_genia_coref(input_path)
    data = data.iloc[0:153, :]

    #model, tokenizer = model_loader.load_flan_model(device_type)
    model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True)

    # generate moral foundation prompt format strings
    coref_prompts = coref_prompting.generate_tf_prompts(
        num_shots,
        example_path,
        tokenizer
    )

    #model, tokenizer = model_loader.load_test_model(device_type)

    # define rules
    rule_one = LLMTFRule(
        'rule_one',
        ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
        ['coreferent', 'distinct'],
        'CF_{doc_id}_{entity1_id}_{entity2_id}_{label}',
        'RuleOne_{doc_id}_{entity1_id}_{entity2_id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        device_type,
        coref_prompts
    )
    rules = {
        rule_one.name: rule_one, 
    }
    start = time.time() # Record the start time
    rule_groundings = {}
    for rule_name, rule in rules.items():
        rule_groundings[rule_name] = rule.get_rule_groundings(data)
    scored_rule_groundings = coref_scoring.get_scored_groundings(rule_groundings, ['rule_one'], 'tf')
    elapsed = time.time() - start # Calculate elapsed time
    print(f"Prompt Elapsed time: {elapsed:.2f} seconds")
    rule_constraints = coref_scoring.get_constraints()
    inference_model = GurobiInferenceModel(rules, scored_rule_groundings,  rule_constraints)
    start = time.time() # Record the start time
    inference_model.inference()
    elapsed = time.time() - start # Calculate elapsed time
    print(f"Inference Elapsed time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
