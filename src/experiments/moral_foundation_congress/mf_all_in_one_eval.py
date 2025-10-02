import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.rule_template import RuleTemplate
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict
import os
import src.helpers.scoring.mf_scoring as mf_scoring
import src.analysis.analysis_helper as analysis_helper
from src.inference.gurobi_inference_model import GurobiInferenceModel
from collections import Counter
import re


def transform_groundings(data, response_dataframe):
    data = data.merge(response_dataframe['all_in_one_rule'], on='Id', how='left')
    id_groups = data.groupby(['Id'])
    missing_foundations = 0
    missing_roles = 0
    results = {}
    for group_name, group in id_groups:
        response_content = None
        id = None
        entities = []
        for item, row in group.iterrows():
            id = row['Id']
            response_content = row['Response']
            if not pd.isna(row['Entity']):
                entities.append(row['Entity'])
        foundation_search = re.search('Moral Foundation:(.*)(\n|$)', response_content)
        if foundation_search:
            foundation = foundation_search.group(1).strip()
        elif response_content.strip() in constants.MORAL_FOUNDATIONS:
            foundation = response_content.strip()
        else:
            missing_foundations += 1
        entity_results = []
        for entity in entities:
            stripped_entitiy = entity.strip()
            entity_search = re.search(f'Moral Role of \"\s*{stripped_entitiy}\s*\":(.*)(\n|$)', response_content)
            if entity_search:
                entity_label = entity_search.group(1)
                entity_results.append({
                    'Entity': entity,
                    'Label': entity_label.strip()
                })
            else:
                print(group)
                print(entity)
                print(response_content)
                print('\n\n\n\n\n')
                missing_roles += 1
                entity_results.append({
                    'Entity': entity,
                    'Label': ""
                })
        result = {
            'MoralFrame': foundation
        }
        if len(entity_results) != 0:
            result['EntityRoles'] = entity_results
        results[id] = result
    print(missing_foundations)
    print(missing_roles)
    return results


def main():
    data_input_path = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    output_path = sys.argv[3]
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(data_input_path)
    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path, ['all_in_one_rule'])
    results = transform_groundings(data, rule_groundings)
    analysis_helper.write_json_file(output_path + 'few_shot.json', results)

if __name__ == "__main__":
    main()