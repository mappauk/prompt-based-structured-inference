import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_tf_rule import LLMTFRule
import src.helpers.model_loader as model_loader
import src.helpers.coref_prompting as coref_prompting
import src.helpers.mf_prompt_constants as constants
#import src.helpers.genia_dataset_loader as dataset_loader
import src.helpers.ontonotes_dataset_loader as dataset_loader

from src.rules.rule_type import RuleType
from src.inference.gurobi_inference_model import GurobiInferenceModel
from typing import Dict


def main():
    # hyperparamaters
    device_type = 'cuda'
    num_shots = 2
    topk = 5
    temperature = 0.5
    prompt_batch_size = 16
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    example_path = sys.argv[3] 
    # load data
    data = dataset_loader.preprocess_ontonotes_coref(input_path)
    print(data)

'''
    # generate moral foundation prompt format strings
    coref_prompts = coref_prompting.generate_one_pass_tf_coref_prompt_format(
        num_shots, 
        example_path
    )
    # load model
    model, tokenizer = model_loader.load_test_model(device_type)
    # define rules
    rule_one = LLMTFRule(
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
    def constr_one(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        coref_groupings = rule_groundings['rule_one'].groupby(['doc_id'])
        for group_name, group in coref_groupings:
            for i, main_row in group.iterrows():
                for j, sec_row in group.iloc[i:].iterrows():
                    tr_ent_one = None
                    tr_ent_two = None
                    if main_row['entity1_id'] == sec_row['entity1_id']:
                        tr_ent_one = main_row['entity2_id']
                        tr_ent_two = sec_row['entity2_id']
                    elif main_row['entity1_id'] == sec_row['entity2_id']:
                        tr_ent_one = main_row['entity2_id']
                        tr_ent_two = sec_row['entity1_id']
                    elif main_row['entity2_id'] == sec_row['entity1_id']:
                        tr_ent_one = main_row['entity1_id']
                        tr_ent_two = sec_row['entity2_id']
                    elif main_row['entity2_id'] == sec_row['entity2_id']:
                        tr_ent_one = main_row['entity1_id']
                        tr_ent_two = sec_row['entity1_id']     
                    tr_var_one = 'CF_{0}_{1}'.format(tr_ent_one, tr_ent_two)
                    tr_var_two = 'CF_{0}_{1}'.format(tr_ent_two, tr_ent_one)
                    if tr_ent_one != None and tr_var_one in head_dict:
                        m.addConstr(head_dict[main_row['HeadVariable']] * head_dict[sec_row['HeadVariable']] <= head_dict[tr_var_one])
                    elif tr_ent_one != None and tr_var_two in head_dict:
                        m.addConstr(head_dict[main_row['HeadVariable']] * head_dict[sec_row['HeadVariable']] <= head_dict[tr_var_two])

    custom_rule_constraints = [constr_one]
    # perform inference
    inference_model = GurobiInferenceModel(rules, rule_groundings, data,  custom_rule_constraints)
    variable_assignments = inference_model.inference()
    # save results
    results = {}
    for varName, value in variable_assignments.items():
        parsedVarName = varName.split('_')
        parsedId = parsedVarName[1]
        id_result = []
        if parsedId in results:
            id_result = results[parsedId]
        if parsedVarName[0] == 'CF' and parsedVarName[len(parsedVarName) - 1] != 'n':
            id_result.append({
                'Entity_1': parsedVarName[2],
                'Entity_2': parsedVarName[3],
                'Value': value
            })
    dataset_loader.write_json_file(output_path, results)
    '''

if __name__ == "__main__":
    main()
