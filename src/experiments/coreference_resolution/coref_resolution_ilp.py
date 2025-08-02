import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
import src.helpers.loaders.ontonotes_dataset_loader as ontonotes_dataset_loader

import src.analysis.analysis_helper as analysis_helper
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import src.helpers.scoring.coref_scoring as coref_scoring

from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
from src.inference.gurobi_inference_model import GurobiInferenceModel
from typing import Dict

def main():
    rule_groundings_path = sys.argv[1]
    rule_type = sys.argv[2]
    output_path = sys.argv[3]

    rule_groundings = coref_scoring.get_scored_groundings(rule_groundings_path, ['rule_one'], rule_type)
    rule_one = RuleTemplate(
        'rule_one',
        ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
        [],
        'CF_{doc_id}_{entity1_id}_{entity2_id}',
        'RuleOne_{doc_id}_{entity1_id}_{entity2_id}',
        RuleType.BINARY
    )
    rules = {
        rule_one.name: rule_one
    }

    # filter out multi class rule variables
    rule_groundings['rule_one'] = rule_groundings['rule_one'][~rule_groundings['rule_one']['HeadVariable'].str.endswith('distinct')]
    rule_groundings['rule_one']['HeadVariable'] = rule_groundings['rule_one']['HeadVariable'].map(lambda h: h[:-11])
    rule_groundings['rule_one']['RuleVariable'] = rule_groundings['rule_one']['RuleVariable'].map(lambda h: h[:-11])


    custom_rule_constraints = coref_scoring.get_constraints()
    # perform inference
    inference_model = GurobiInferenceModel(rules, rule_groundings, custom_rule_constraints, num_solutions=1)
    solutions = inference_model.inference()
    # save results

    variable_assignments = solutions[0]
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
        results[parsedId] = id_result
    analysis_helper.write_json_file(output_path, results)

if __name__ == "__main__":
    main()