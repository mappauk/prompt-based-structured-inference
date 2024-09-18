import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
import src.analysis.analysis_helper as analysis_helper
import src.helpers.loaders.prompt_data_loader as prompt_data_loader

from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
from src.inference.gurobi_inference_model import GurobiInferenceModel
from typing import Dict


def main():
    input_path = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    output_path = sys.argv[3]

    data = genia_dataset_loader.preprocess_genia_coref(input_path)
    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path)
    rule_one = RuleTemplate(
        'rule_one',
        ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
        [],
        'CF_{doc_id}_{entity1_id}_{entity2_id}',
        'RuleOne_{doc_id}_{entity1_id}_{entity2_id}',
        RuleType.BINARY
    )
    rules = [rule_one]
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
    inference_model = GurobiInferenceModel(rules, rule_groundings, data, custom_rule_constraints)
    variable_assignments = inference_model.inference()
    # save results
    results = {}
    for varName, value in variable_assignments.items():
        parsedVarName = varName.split('_')
        print(parsedVarName)
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
        results[parsedId] = id_result
    analysis_helper.write_json_file(output_path, results)

if __name__ == "__main__":
    main()