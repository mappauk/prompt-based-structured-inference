import src.helpers.moral_prompting as moral_prompting
import src.helpers.prompt_constants as constants
import src.helpers.dataset_loader as dataset_loader
import sys
import sklearn.metrics as sk

def main():
    dataset_dir = sys.argv[1]
    input_path = sys.argv[2]
    labels = dataset_loader.load_role_labels(dataset_dir)
    predictions = dataset_loader.load_results(input_path)
    true_labels = []
    predicted_labels = []
    for index, row in labels.iterrows():
        predicted_entities = predictions[row['Id']]['EntityRoles']
        for predicted_entity in predicted_entities:
            if predicted_entity['Entity'] == row['Entity']:
                true_labels.append(row['EntityLabel'])
                predicted_labels.append(predicted_entity['Label'])


    print('Macro F1:')
    print(sk.f1_score(true_labels, predicted_labels, labels=constants.MORAL_FOUNDATION_ROLE, average='macro'))

    print('Micro F1:')
    print(sk.f1_score(true_labels, predicted_labels, labels=constants.MORAL_FOUNDATION_ROLE, average='micro'))
    
if __name__ == "__main__":
    main()
