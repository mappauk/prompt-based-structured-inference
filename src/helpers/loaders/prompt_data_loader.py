import os
import pandas as pd
from typing import List
from src.rules.rule_template import RuleTemplate
import numpy as np
import torch



def load_rule_groundings(path: str):
    rule_groundings = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            rule_grounding_data = pd.read_pickle(filepath)
            filePrefixEnd = file.find('_groundings_dataframe.pkl')
            if filePrefixEnd > 0:
                grounding_name = file[0:filePrefixEnd]
                rule_groundings[grounding_name] = rule_grounding_data
    return rule_groundings

def load_rule_groundings_json(path: str, dtype):
    rule_groundings = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            rule_grounding_data = pd.read_json(filepath, dtype=dtype)
            filePrefixEnd = file.find('_groundings_dataframe.json')
            if filePrefixEnd > 0:
                grounding_name = file[0:filePrefixEnd]
                rule_groundings[grounding_name] = rule_grounding_data

    return rule_groundings

def save_rule_groundings(rules: List[RuleTemplate], data: pd.DataFrame, output_path: str):
    for rule_name, rule in rules.items():
        rule_grounding = rule.get_rule_groundings(data)
        rule_grounding.to_pickle(output_path + rule_name + '_groundings_dataframe.pkl')