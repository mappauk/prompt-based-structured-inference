import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.analysis.analysis_helper as analysis_helper
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import numpy as np
import sys
import sklearn.metrics as sk
import pandas as pd
import src.helpers.scoring.mf_scoring as mf_scoring

def compute_ece(num_bins, confidences, predicted_labes, true_labels):
    bins = np.arange(0, num_bins + 1)*(1/num_bins)
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
            ece += abs(bin_accuracy - avg_confidence)*no_items/total_item_count
    return ece

def main():
    dataset_dir = sys.argv[1]
    rule_groundings_path = sys.argv[2]
    rule_type = sys.argv[3]
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
    foundation_instance_groupings = rule_groundings['rule_one'].groupby(['Id'])
    moral_foundation_confidences = []
    moral_foundation_predicted_labels = []
    moral_foundation_true_labels = []
    for group_name, group in foundation_instance_groupings:
        max_row = group.iloc[group['Score'].argmax()]
        moral_foundation_confidences.append(max_row['Score'])
        moral_foundation_predicted_labels.append(max_row['label'])
        moral_foundation_true_labels.append(labels_dict[max_row['Id']]['mf_label'])

    role_instance_groupings = rule_groundings['rule_two'].groupby(['Id', 'Entity'])
    role_confidences = []
    role_predicted_labels = []
    role_true_labels = []
    for group_name, group in role_instance_groupings:
        max_row = group.iloc[group['Score'].argmax()]
        if max_row['Entity'] in labels_dict[max_row['Id']]:
            role_confidences.append(max_row['Score'])
            role_predicted_labels.append(max_row['label'])
            role_true_labels.append(labels_dict[max_row['Id']][max_row['Entity']])
    
    mf_ece = compute_ece(10, moral_foundation_confidences, moral_foundation_predicted_labels, moral_foundation_true_labels)
    role_ece = compute_ece(10, role_confidences, role_predicted_labels, role_true_labels)
    print(f'MF ECE: {mf_ece}')
    print(f'Role ECE: {role_ece}')
    
if __name__ == "__main__":
    main()