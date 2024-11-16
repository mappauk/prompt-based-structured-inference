import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.analysis.analysis_helper as analysis_helper
import sys
import sklearn.metrics as sk
import pandas as pd

def main():
    dataset_dir = sys.argv[1]
    input_path = sys.argv[2]
    mf_labels = dataset_loader.load_frame_labels(dataset_dir)
    role_labels = dataset_loader.load_role_labels(dataset_dir)
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(dataset_dir)
    entity_plaintext_to_id, entity_map = dataset_loader.load_entity_map(dataset_dir)
    predictions_list = analysis_helper.load_multiple_results(input_path)
    for prediction_data in predictions_list:
        mf_labels = mf_labels[~mf_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
        role_labels = role_labels[~role_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
        data = data[~data['Id'].isin(constants.IDS_TO_EXCLUDE)]
        predictions = prediction_data['content']
        for id in constants.IDS_TO_EXCLUDE:
            predictions.pop(id, None)
        
        true_mf_labels = []
        predicted_mf_labels = []
        true_role_labels = []
        predicted_role_labels = []
        for index, row in mf_labels.iterrows():
            true_mf_labels.append(row['Label'])
            predicted_mf_labels.append(predictions[row['Id']]['MoralFrame'])
        true_role_labels = []
        predicted_role_labels = []
        for index, row in role_labels.iterrows():
            predicted_entities = predictions[row['Id']]['EntityRoles']
            for predicted_entity in predicted_entities:
                if predicted_entity['Entity'] == row['Entity']:
                    true_role_labels.append(row['EntityLabel'])
                    predicted_role_labels.append(predicted_entity['Label'])
        print('Prediction File ' + prediction_data['name'] + ' :')
        print('Moral Foundations Macro F1:')
        print(sk.f1_score(true_mf_labels, predicted_mf_labels, labels=constants.MORAL_FOUNDATIONS, average='macro'))
        print('Moral Foundations Micro F1:')
        print(sk.f1_score(true_mf_labels, predicted_mf_labels, labels=constants.MORAL_FOUNDATIONS, average='micro'))

        print('Moral Role Macro F1:')
        print(sk.f1_score(true_role_labels, predicted_role_labels, labels=constants.MORAL_FOUNDATION_ROLE, average='macro'))
        print('Moral Role Micro F1:')
        print(sk.f1_score(true_role_labels, predicted_role_labels, labels=constants.MORAL_FOUNDATION_ROLE, average='micro'))
        constraint_violation_calculation(data, predictions, entity_plaintext_to_id, entity_map)
        print('\n')


def constraint_violation_calculation(data, predictions, entity_plaintext_to_id, entity_map):
    entity_frame_mismatch = 0
    duplicate_role_assignment = 0
    polarity_violation = 0
    for id, id_result in predictions.items():
        entity_pred_dict = {}
        if 'EntityRoles' in id_result:
            for entity_pred in id_result['EntityRoles']:
                if  id_result['MoralFrame'] != constants.MORAL_FOUNDATION_ROLE_TO_MF[entity_pred['Label']]:
                    entity_frame_mismatch += 1
                if entity_pred['Label'] in entity_pred_dict:
                    duplicate_role_assignment += 1
                else:
                    entity_pred_dict[entity_pred['Label']] = 1
    data_groupings = data.groupby(['Ideology', 'Topic'])
    for group_name, group in data_groupings:
        if len(group) == 1:
            continue
        counter = 0
        for item, row in group.iterrows():
            counter = counter + 1
            for item_two, row_two in group.iloc[counter:].iterrows():
                if row_two['Id'] != row['Id']:
                    row_one_result = predictions[row['Id']]
                    entity_row_one_result = None
                    entity_row_two_result = None
                    if 'EntityRoles' in row_one_result:
                        for entity_pred in row_one_result['EntityRoles']:
                            if entity_pred['Entity'] == row['Entity']:
                                entity_row_one_result = entity_pred['Label']
                    row_two_result = predictions[row_two['Id']]
                    if 'EntityRoles' in row_two_result:
                        for entity_pred in row_two_result['EntityRoles']:
                            if entity_pred['Entity'] == row_two['Entity']:
                                entity_row_two_result = entity_pred['Label']
                    entity_one = row['Entity'] if type(row['Entity']) != str else row['Entity'].strip()
                    entity_two = row_two['Entity'] if type(row_two['Entity']) != str else row_two['Entity'].strip()
                    entity_one_id = None if entity_one not in entity_plaintext_to_id else entity_plaintext_to_id[entity_one]
                    entity_two_id = None if entity_two not in entity_plaintext_to_id else entity_plaintext_to_id[entity_two]
                    are_entities_equal = (entity_one_id in entity_map and entity_two_id in entity_map[entity_one_id])
                    if (entity_row_one_result in constants.POLARITY_MAP and 
                        entity_row_two_result in constants.POLARITY_MAP and 
                        are_entities_equal and
                        constants.POLARITY_MAP[entity_row_one_result] != constants.POLARITY_MAP[entity_row_two_result]):
                        polarity_violation += 1
    print('Entity Role and Moral Frame Mismatch Constraint Violations: ' + str(entity_frame_mismatch))
    print('Duplicate Role Assignment Constraint Violations: ' + str(duplicate_role_assignment))
    print('Entity Polarity Constraint Violations: ' + str(polarity_violation))
    
if __name__ == "__main__":
    main()