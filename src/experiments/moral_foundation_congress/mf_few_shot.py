import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
import src.analysis.analysis_helper as analysis_helper
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from typing import Dict


def main():
    rule_groundings_path = sys.argv[1]
    output_path = sys.argv[2]

    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path)
    # save results
    results = {}
    # cluster by id
    foundation_instance_groupings = rule_groundings['rule_one'].groupby(['Id'])
    for group_name, group in foundation_instance_groupings:
        max_row = group.iloc[group['Score'].argmax()]
        results[max_row['Id']] = {
            'MoralFrame': max_row['label']
        }

    role_instance_groupings = rule_groundings['rule_two'].groupby(['Id', 'Entity'])
    for group_name, group in role_instance_groupings:
        max_row = group.iloc[group['Score'].argmax()]
        foundation_id_result = results[max_row['Id']]
        entity_result = {
            'Entity': max_row['Entity'],
            'Label': max_row['label']
        }
        if 'EntityRoles' in foundation_id_result:
            foundation_id_result['EntityRoles'].append(entity_result)
        else:
            foundation_id_result['EntityRoles'] = [entity_result]
        results[max_row['Id']] = foundation_id_result

    analysis_helper.write_json_file(output_path, results)

if __name__ == "__main__":
    main()
