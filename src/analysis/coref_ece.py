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
import src.helpers.loaders.prompt_data_loader as prompt_data_loader


def compute_ece(num_bins, confidences, predicted_labes, true_labels):
    bins = np.arange(0, num_bins + 1)*0.1
    ece = 0
    total_item_count = len(confidences)
    for i in range(1, len(bins)):
        bin_confidences = []
        bin_accurate = 0
        for j in range(len(confidences)):
            if confidences[j] < bins[i] and confidences[j] >= bins[i - 1]:
                bin_confidences.append(confidences[j])
                if predicted_labes[j] == true_labels[j]:
                    bin_accurate += 1
        no_items = len(bin_confidences)
        if no_items > 0:
            avg_confidence = np.mean(bin_confidences)
            bin_accuracy = bin_accurate/no_items
            ece += abs(avg_confidence - bin_accuracy)*no_items/total_item_count
    return ece

def answer_conversion(answer):
    return 1 if answer == 'Yes' else 0

def main():
    rule_groundings_path = sys.argv[2]
    dataset_dir = sys.argv[1]
    
    data = genia_dataset_loader.preprocess_genia_coref(dataset_dir)
    data['label'] = data['answer'].apply(answer_conversion)
    labels_dict = {}
    for index, row in data.iterrows():
        doc_id = row['doc_id']
        entity1 = row['entity1_id']
        entity2 = row['entity2_id']
        labels_dict[f'{doc_id}_{entity1}_{entity2}'] = row['label']

    confidences = []
    predicted_labels = []
    true_labels = []
    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path)
    for index, row in rule_groundings['rule_one'].iterrows():
        parsedVarName = row['HeadVariable'].split('_')
        parsedId = parsedVarName[1]
        entity_one = parsedVarName[2]
        entity_two = parsedVarName[3]
        if parsedVarName[0] == 'CF' and parsedVarName[len(parsedVarName) - 1] != 'nocoref':
            confidences.append(row['Score'])
            predicted_labels.append(round(row['Score']))
            true_labels.append(labels_dict[f'{parsedId}_{entity_one}_{entity_two}'])
  
    coref_ece = compute_ece(10, confidences, predicted_labels, true_labels)
    print(f'Coref ECE: {coref_ece}')
    
if __name__ == "__main__":
    main()