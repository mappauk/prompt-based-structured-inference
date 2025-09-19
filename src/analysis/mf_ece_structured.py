import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.analysis.analysis_helper as analysis_helper
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import src.helpers.scoring.mf_scoring as mf_scoring
import numpy as np
import sys
import sklearn.metrics as sk
import pandas as pd

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
    rule_type = sys.argv[5]
    
    mf_labels = dataset_loader.load_frame_labels(dataset_dir)
    role_labels = dataset_loader.load_role_labels(dataset_dir)
    mf_labels = mf_labels[~mf_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
    role_labels = role_labels[~role_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
    labels_dict = {}
    for index, row in mf_labels.iterrows():
        labels_dict[row['Id']] = {
            'mf_label': row['Label']
        }
    for index, row in role_labels.iterrows():
        labels_dict[row['Id']][row['Entity']] = row['EntityLabel']

    rule_groundings = mf_scoring.get_scored_groundings(rule_groundings_path, ['rule_one', 'rule_two', 'rule_three', 'rule_four'], rule_type)
    rule_groundings['rule_one'] = rule_groundings['rule_one'][~rule_groundings['rule_one']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_two'] = rule_groundings['rule_two'][~rule_groundings['rule_two']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_three'] = rule_groundings['rule_three'][~rule_groundings['rule_three']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    rule_groundings['rule_four'] = rule_groundings['rule_four'][~rule_groundings['rule_four']['Id'].isin(constants.IDS_TO_EXCLUDE)]
    scores_dict = {}
    for item, row in rule_groundings['rule_one'].iterrows():
        id = row['Id']
        label = row['label']
        scores_dict[f'{id}_{label}'] = row['Score']
    for item, row in rule_groundings['rule_two'].iterrows():
        id = row['Id']
        entity = row['Entity']
        label = row['label']
        scores_dict[f'{id}_{entity}_{label}'] = row['Score']
    for item, row in rule_groundings['rule_three'].iterrows():
        id = row['Id']
        label = row['label']
        scores_dict[f'{id}_{label}'] = (scores_dict[f'{id}_{label}'] + row['Score'])/2
    for item, row in rule_groundings['rule_four'].iterrows():
        id = row['Id']
        entity = row['Entity']
        label = row['label']
        scores_dict[f'{id}_{entity}_{label}'] = (scores_dict[f'{id}_{entity}_{label}'] + row['Score'])/2

    pooling_results = analysis_helper.load_results(pooling_input_path)['solutions']
    predictions_list = analysis_helper.load_multiple_results(predictions_input_path)
    structure_confidences = []
    structure_accuracies = []
    for prediction_data in predictions_list:
        predictions = prediction_data['content']
        for id in constants.IDS_TO_EXCLUDE:
            predictions.pop(id, None)
        for id, value in predictions.items():
            mf_label = value['MoralFrame']
            total_structure_elements = 1
            hamming_count = 0
            prediction_score = 0
            pool_score = 0
            if mf_label != labels_dict[id]['mf_label']:
                hamming_count += 1
            if 'EntityRoles' in value:
                total_structure_elements += len(value['EntityRoles'])
                for i in range(len(value['EntityRoles'])):
                    entity = value['EntityRoles'][i]['Entity']
                    entity_label = value['EntityRoles'][i]['Label']
                    if entity in labels_dict[id] and entity_label != labels_dict[id][entity]:
                        hamming_count += 1 
                    prediction_score += scores_dict[f'{id}_{entity}_{entity_label}']
            prediction_score += scores_dict[f'{id}_{mf_label}']

            for pooling_result in pooling_results:
                pooling_structure = pooling_result[id]
                pooling_structure_mf_label = pooling_structure['MoralFrame']
                pool_score += scores_dict[f'{id}_{pooling_structure_mf_label}']
                if 'EntityRoles' in pooling_structure:
                    for i in range(len(pooling_structure['EntityRoles'])):
                        pooling_structure_entity = pooling_structure['EntityRoles'][i]['Entity']
                        pooling_structure_entity_label = pooling_structure['EntityRoles'][i]['Label']
                        pool_score += scores_dict[f'{id}_{pooling_structure_entity}_{pooling_structure_entity_label}']
            
            structure_accuracy = 1 - (hamming_count/(1 + total_structure_elements))
            structure_accuracies.append(structure_accuracy)
            structure_confidences.append(prediction_score/pool_score)

    
    structure_ece = compute_ece(10, structure_confidences, structure_accuracies)
    print(f'Structure ECE: {structure_ece}')
    
if __name__ == "__main__":
    main()