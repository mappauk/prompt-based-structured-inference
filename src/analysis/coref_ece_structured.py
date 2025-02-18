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

def answer_conversion(answer):
    return 1 if answer == 'Yes' else 0

def compute_ece(num_bins, confidences, accuracies):
    bins = np.arange(0, num_bins + 1)*0.1
    ece = 0
    total_item_count = len(confidences)
    for i in range(1, len(bins)):
        bin_confidences = []
        bin_accuracies = []
        for j in range(len(confidences)):
            if confidences[j] < bins[i] and confidences[j] >= bins[i - 1]:
                bin_confidences.append(confidences[j])
                bin_accuracies.append(accuracies[j])
        no_items = len(bin_confidences)
        if no_items > 0:
            avg_confidence = np.mean(bin_confidences)
            bin_accuracy = np.mean(bin_accuracies)
            ece += abs(avg_confidence - bin_accuracy)*no_items/total_item_count
    return ece

def main():
    dataset_dir = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    predictions_input_path = sys.argv[3]
    pooling_input_path = sys.argv[4]
    
    data = genia_dataset_loader.preprocess_genia_coref(dataset_dir)
    data['label'] = data['answer'].apply(answer_conversion)
    labels_dict = {}
    for index, row in data.iterrows():
        doc_id = row['doc_id']
        entity1 = row['entity1_id']
        entity2 = row['entity2_id']
        labels_dict[f'{doc_id}_{entity1}_{entity2}'] = row['label']

    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path)
    scores_dict = {}
    for index, row in rule_groundings['rule_one'].iterrows():
        parsedVarName = row['HeadVariable'].split('_')
        parsedId = parsedVarName[1]
        entity_one = parsedVarName[2]
        entity_two = parsedVarName[3]
        if parsedVarName[0] == 'CF' and parsedVarName[len(parsedVarName) - 1] != 'nocoref':
            scores_dict[f'{parsedId}_{entity_one}_{entity_two}_1'] = row['Score']
            scores_dict[f'{parsedId}_{entity_one}_{entity_two}_0'] = 1 - row['Score']

    pooling_results = analysis_helper.load_results(pooling_input_path)['solutions']

    predictions_list = analysis_helper.load_multiple_results(predictions_input_path)
    structure_confidences = []
    structure_accuracies = []

    for prediction_data in predictions_list:
        for doc_id, doc_values in prediction_data['content'].items():
            for doc_value in doc_values:
                entity1 = doc_value['Entity_1']
                entity2 = doc_value['Entity_2']
                accuracy = 0
                predicted_value = int(doc_value['Value'])
                if labels_dict[f'{doc_id}_{entity1}_{entity2}'] == predicted_value:
                    accuracy = 1
                prediction_score = scores_dict[f'{doc_id}_{entity1}_{entity2}_{predicted_value}']
                pooling_scores = 0
                for pooling_result in pooling_results:
                    pooling_doc_values = pooling_result[doc_id]
                    for pooling_doc_value in pooling_doc_values:
                        if pooling_doc_value['Entity_1'] == entity1 and pooling_doc_value['Entity_2'] == entity2:
                            pooling_predicted_value = int(pooling_doc_value['Value'])
                            pooling_scores += scores_dict[f'{doc_id}_{entity1}_{entity2}_{pooling_predicted_value}']
                structure_accuracies.append(accuracy)
                structure_confidences.append(prediction_score/pooling_scores)
    
    structure_ece = compute_ece(10, structure_confidences, structure_accuracies)
    print(f'Structure ECE: {structure_ece}')
    
if __name__ == "__main__":
    main()