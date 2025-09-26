import os
import pandas as pd
from typing import List
from src.rules.rule_template import RuleTemplate
import jsonlines
import numpy as np
import torch
import glob
import json

def load_rule_groundings(path: str, rule_names: list):
    rule_groundings = {}
    for rule_name in rule_names:
        files = glob.glob(os.path.join(path, rule_name + '*_groundings_dataframe.pkl'))
        rule_grounding_chunks = []
        for file in files:
            rule_grounding_data = pd.read_pickle(file)
            rule_grounding_chunks.append(rule_grounding_data)
        rule_groundings[rule_name] = pd.concat(rule_grounding_chunks)
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

def save_rule_groundings(rules: List[RuleTemplate], data: pd.DataFrame, output_path: str, startIndex = 0):
    num_splits = 5
    data_split = np.array_split(data, num_splits)
    for i in range(startIndex, num_splits):
        for rule_name, rule in rules.items():
            rule_grounding = rule.get_rule_groundings(data_split[i])
            rule_grounding.to_pickle(output_path + rule_name + f'_{i}_groundings_dataframe.pkl')

def save_rule_grounding_batches(rules: List[RuleTemplate], data: pd.DataFrame, output_path: str, startIndex = 0):
    for rule_name, rule in rules.items():
        rule_grounding = rule.get_rule_groundings(data)
        with jsonlines.open(output_path + rule_name + '.jsonl', 'w') as writer:
            writer.write_all(rule_grounding)
    
def load_rule_grounding_batches(rules, input_path):
    rule_outputs = {}
    for rule_name, rule in rules.items():
        current_rule_output = []
        with jsonlines.open(input_path + rule_name +'_openai_output.jsonl') as reader:
            for obj in reader:
                current_rule_output.append(obj)
        rule_outputs[rule_name] = current_rule_output
    return rule_outputs