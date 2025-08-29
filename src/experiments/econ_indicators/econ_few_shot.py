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
    rule_groundings_path = sys.argv[1]
    rule_type = sys.argv[2]
    output_path = sys.argv[3]

    rules = econ_scoring.get_rule_info()
    rule_groundings = econ_scoring.get_scored_groundings(rule_groundings_path, rule_type)
    constraints = econ_scoring.get_hard_constraints()

    econ_scoring.model_eval(rules, constraints, rule_groundings, outputs=None, softmax_enabled=False, inference_enabled=True)
    # save results


if __name__ == "__main__":
    main()