import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_mv_rule import LLMMVRule
import src.helpers.loaders.model_loader as model_loader
import src.helpers.prompting.coref_prompting as coref_prompting
import src.helpers.prompting.coref_prompt_constants as constants
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
import src.helpers.loaders.ontonotes_dataset_loader as ontonotes_dataset_loader
import src.analysis.analysis_helper as analysis_helper

from src.rules.rule_type import RuleType
from src.inference.gurobi_inference_model import GurobiInferenceModel
from typing import Dict


def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 2
    topk = 5
    num_votes = 5
    temperature = 0.5
    prompt_batch_size = 16
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3] 
    # load data
    data = ontonotes_dataset_loader.preprocess_ontonotes_coref(input_path)
    #data = genia_dataset_loader.preprocess_genia_coref(input_path)

    # generate moral foundation prompt format strings
    coref_prompts = coref_prompting.generate_one_pass_tf_coref_prompt_format(
        num_shots, 
        example_path
    )
    # load model
    model, tokenizer = model_loader.load_test_model(device_type)
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
    # get rule groundings:
    rule_groundings = {}
    for rule_name, rule in rules.items():
        rule_groundings[rule_name] = rule.get_rule_groundings(data)
    # define custom constraints

    # save results
    results = {}
    for index, row in rule_groundings['rule_one'].iterrows():
        parsedVarName = row['HeadVariable'].split('_')
        parsedId = parsedVarName[1]
        id_result = []
        if parsedId in results:
            id_result = results[parsedId]
        if parsedVarName[0] == 'CF' and parsedVarName[len(parsedVarName) - 1] != 'n':
            id_result.append({
                'Entity_1': parsedVarName[2],
                'Entity_2': parsedVarName[3],
                'Value': round(row['score'])
            })
        results[parsedId] = id_result
    analysis_helper.write_json_file(output_path, results)

if __name__ == "__main__":
    main()