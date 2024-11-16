import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.analysis.analysis_helper as analysis_helper
import sys
import sklearn.metrics as sk
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from typing import List
import networkx as nx
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader


def answer_conversion(answer):
    return 1 if answer == 'Yes' else 0

def constraint_violation_calculation(prediction_data):
    transitivity_constraint_violation_count = 0
    for doc_id, doc_values in prediction_data['content'].items():
        entity_map = {}
        for doc_value in doc_values:
            if doc_value['Value'] != 1:
                continue
            entity1 = doc_value['Entity_1']
            entity2 = doc_value['Entity_2']
            if entity1 in entity_map:
                entity_map[entity1].add(entity2)
            else:
                temp_entity1_list = set()
                temp_entity1_list.add(entity2)
                entity_map[entity1] = temp_entity1_list
            if entity2 in entity_map:
                entity_map[entity2].add(entity1)
            else:
                temp_entity2_list = set()
                temp_entity2_list.add(entity1)
                entity_map[entity2] = temp_entity2_list
        for entity_id, coref_list in entity_map.items():
            for coref_entity in coref_list:
                for trans_coref_entity in entity_map[coref_entity]:
                    if trans_coref_entity not in coref_list and trans_coref_entity != entity_id:
                        transitivity_constraint_violation_count += 1
    print(f'Transitivity Constraints: {transitivity_constraint_violation_count}')

def main():
    dataset_dir = sys.argv[1]
    input_path = sys.argv[2]
    data = genia_dataset_loader.preprocess_genia_coref(dataset_dir)
    data['label'] = data['answer'].apply(answer_conversion)
    predictions_list = analysis_helper.load_multiple_results(input_path)
    for prediction_data in predictions_list:
        true_labels = []
        predicted_labels = []
        predicted_results = {}
        for doc_id, doc_values in prediction_data['content'].items():
            for doc_value in doc_values:
                entity1 = doc_value['Entity_1']
                entity2 = doc_value['Entity_2']
                predicted_results[f'{doc_id}_{entity1}_{entity2}'] = int(doc_value['Value'])
        for index, row in data.iterrows():
            true_labels.append(row['label'])
            doc_id = row['doc_id']
            entity1 = row['entity1_id']
            entity2 = row['entity2_id']
            predicted_labels.append(predicted_results[f'{doc_id}_{entity1}_{entity2}'])
        print('Results ' + prediction_data['name'] + ' :')
        print('F1: ')
        print(sk.f1_score(true_labels, predicted_labels, average='macro'))
        print('Constraint Violations: ')
        constraint_violation_calculation(prediction_data)
        break
    
if __name__ == "__main__":
    main()