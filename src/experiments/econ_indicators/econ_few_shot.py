import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
import src.analysis.analysis_helper as analysis_helper
import src.helpers.scoring.econ_scoring as econ_scoring
from typing import Dict


def main():
    data_path = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    rule_type = sys.argv[3]

    rules = econ_scoring.get_rule_info()
    rule_groundings = econ_scoring.get_scored_groundings(data_path, rule_groundings_path, rule_type)
    constraints = econ_scoring.get_hard_constraints()
    #print(rule_groundings['rule_one'])
    econ_scoring.model_eval(rules, constraints, rule_groundings, outputs=None, softmax_enabled=False, inference_enabled=True)


if __name__ == "__main__":
    main()