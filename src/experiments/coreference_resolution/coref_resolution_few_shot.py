import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
import src.analysis.analysis_helper as analysis_helper
import src.helpers.scoring.coref_scoring as coref_scoring
from typing import Dict


def main():
    rule_groundings_path = sys.argv[1]
    rule_type = sys.argv[2]
    output_path = sys.argv[3]

    rule_groundings = coref_scoring.get_scored_groundings(rule_groundings_path, ['rule_one'], rule_type)
    # save results
    results = {}
    for index, row in rule_groundings['rule_one'].iterrows():
        parsedVarName = row['HeadVariable'].split('_')
        parsedId = parsedVarName[1]
        id_result = []
        if parsedId in results:
            id_result = results[parsedId]
        if parsedVarName[0] == 'CF' and parsedVarName[len(parsedVarName) - 1] != 'distinct':
            id_result.append({
                'Entity_1': parsedVarName[2],
                'Entity_2': parsedVarName[3],
                'Value': round(row['Score'])
            })
        results[parsedId] = id_result
    analysis_helper.write_json_file(output_path, results)

if __name__ == "__main__":
    main()