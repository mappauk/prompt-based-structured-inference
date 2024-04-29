import os
import json
import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

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
    counter = 0
    for key, filename in filename_map.items():
        counter += 1
        filepath = os.path.join(datasetdir, filename)
        if counter == 100:
            break
        with open(filepath) as f:
            data = json.load(f)
            for attribute, value in data.items():
                ids.append(attribute)
                tweets.append(value['text'])
                labels.append(key)
    return ids, tweets, labels

def load_dataset_ilp(datasetdir):
    filename_map = {
        'CARE/HARM': 'combined_annotations_care_harm.json',
        'AUTHORITY/SUBVERSION': 'combined_annotations_authority_subversion.json',
        'FAIRNESS/CHEATING': 'combined_annotations_fairness_cheating.json',
        'LOYALTY/BETRAYAL': 'combined_annotations_loyalty_betrayal.json',
        'PURITY/DEGRADATION': 'combined_annotations_sanctity_degradation.json',
    }
    author_label_map = {
        0: 'Republican',
        1: 'Democrat'
    }
    topic_label_map = {
        'aca': 'affordable care act',
        'immig': 'immigration',
        'abort': 'abortion',
        'guns': 'guns',
        'isis': 'terrorism',
        'lgbt': 'lgbtq'
    }
    ids = []
    topic = []
    author_ideology = []
    tweets = []
    for key, filename in filename_map.items():
        counter = 0
        filepath = os.path.join(datasetdir, filename)
        with open(filepath) as f:
            data = json.load(f)
            for attribute, value in data.items():
                counter += 1
                if counter > 4:
                    break
                author_ideology.append(author_label_map[value['author-label']])
                topic.append(topic_label_map[value['issue']])
                ids.append(attribute)
                tweets.append(value['text'])
    return pd.DataFrame(
        {
            'Id': ids,
            'Topic': topic,
            'Ideology': author_ideology,
            "Tweet": tweets,
        }
    )

def load_moral_frame_data_parse_entity_labels(datasetdir):
    filename_map = {
        'CARE/HARM': 'combined_annotations_care_harm.json',
        'AUTHORITY/SUBVERSION': 'combined_annotations_authority_subversion.json',
        'FAIRNESS/CHEATING': 'combined_annotations_fairness_cheating.json',
        'LOYALTY/BETRAYAL': 'combined_annotations_loyalty_betrayal.json',
        'PURITY/DEGRADATION': 'combined_annotations_sanctity_degradation.json',
    }
    author_label_map = {
        0: 'Republican',
        1: 'Democrat'
    }
    topic_label_map = {
        'aca': 'affordable care act',
        'immig': 'immigration',
        'abort': 'abortion',
        'guns': 'guns',
        'isis': 'terrorism',
        'lgbt': 'lgbtq'
    }
    ids = []
    topic = []
    author_ideology = []
    tweets = []
    entity_ids = []
    entities = []
    for key, filename in filename_map.items():
        counter = 0
        filepath = os.path.join(datasetdir, filename)
        with open(filepath) as f:
            data = json.load(f)
            for attribute, value in data.items():
                counter += 1
                if counter > 10:
                    break
                author_ideology.append(author_label_map[value['author-label']])
                topic.append(topic_label_map[value['issue']])
                ids.append(attribute)
                tweets.append(value['text'])
                tweet_entities = set()
                for i in range(1): #range(len(value['annotations'])):
                    for entity in value['annotations'][i]:
                        entity_name = value['text'][entity['startOffset']:entity['endOffset']]
                        entity_name = entity_name.strip()
                        if entity_name not in tweet_entities and len(tweet_entities) <= 2:
                            tweet_entities.add(entity_name)
                            entities.append(entity_name)
                            entity_ids.append(attribute)

    data = pd.DataFrame(
        {
            'Id': ids,
            'Topic': topic,
            'Ideology': author_ideology,
            "Tweet": tweets,
        }
    )
    entity_data = pd.DataFrame(
        {
            'Id': entity_ids,
            'Entity': entities,
        }
    )
    return data.merge(entity_data, how='left', on='Id')


def load_moral_frame_data_ner(datasetdir):
    raw_data = load_dataset_ilp(datasetdir)
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/wikineural-multilingual-ner")
    model = AutoModelForTokenClassification.from_pretrained("Babelscape/wikineural-multilingual-ner")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True, device_map='cuda')
    ids = []
    entities = []
    for index, row in raw_data.iterrows():
        doc = nlp(row['Tweet'])
        for ent in doc:
            if ent['score'] > 0.6:
                print(ent)
                ids.append(row['Id'])
                entities.append(ent['word'])
    entity_data = pd.DataFrame(
        {
            'Id': ids,
            'Entity': entities, 
        }
    )
    return raw_data.merge(entity_data, how='left', on='Id')

def write_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_prediction_results(filename):
    predictions = []
    true_labels = []
    with open(filename) as f:
        data = json.load(f)
        for attribute, value in data.items():
            predictions.append(value["predicted_labels"])
            true_labels.append(value["true_label"])
    return predictions, true_labels
                

    


