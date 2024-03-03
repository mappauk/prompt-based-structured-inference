import os
import json

def load_dataset_foundation_identification(datasetdir):
    filename_map = {
        'CARE/HARM': 'combined_annotations_care_harm.json',
        'AUTHORITY/SUBVERSION': 'combined_annotations_authority_subversion.json',
        'FAIRNESS/CHEATING': 'combined_annotations_fairness_cheating.json',
        'LOYALTY/BETRAYAL': 'combined_annotations_loyalty_betrayal.json',
        'PURITY/DEGRADATION': 'combined_annotations_sanctity_degradation.json',
    }
    ids = []
    tweets = []
    labels = []
    for key, filename in filename_map:
        filepath = os.path.join(datasetdir, filename)
        with open(filepath) as f:
            data = json.load(f)
            for attribute, value in data.items():
                ids.append(attribute)
                tweets.append(value['text'])
                labels.append(key)
    return ids, tweets, labels

def write_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
                

    


