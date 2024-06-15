import os
import json
import pandas as pd
import src.helpers.prompt_constants as constants
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
def load_frame_labels(datasetdir):
    filename_map = {
        'CARE/HARM': 'combined_annotations_care_harm.json',
        'AUTHORITY/SUBVERSION': 'combined_annotations_authority_subversion.json',
        'FAIRNESS/CHEATING': 'combined_annotations_fairness_cheating.json',
        'LOYALTY/BETRAYAL': 'combined_annotations_loyalty_betrayal.json',
        'PURITY/DEGRADATION': 'combined_annotations_sanctity_degradation.json',
    }
    ids = []
    labels = []
    for key, filename in filename_map.items():
        filepath = os.path.join(datasetdir, filename)
        with open(filepath) as f:
            data = json.load(f)
            for attribute, value in data.items():
                ids.append(attribute)
                labels.append(key)
    return pd.DataFrame(
        {
            'Id': ids,
            'Label': labels
        }
    )

def load_role_labels(datasetdir):
    filename_map = {
        'CARE/HARM': 'combined_annotations_care_harm.json',
        'AUTHORITY/SUBVERSION': 'combined_annotations_authority_subversion.json',
        'FAIRNESS/CHEATING': 'combined_annotations_fairness_cheating.json',
        'LOYALTY/BETRAYAL': 'combined_annotations_loyalty_betrayal.json',
        'PURITY/DEGRADATION': 'combined_annotations_sanctity_degradation.json',
    }
    ids = []
    entities = []
    entity_labels = []
    for key, filename in filename_map.items():
        filepath = os.path.join(datasetdir, filename)
        with open(filepath) as f:
            data = json.load(f)
            for attribute, value in data.items():
                tweet_entities, tweet_entity_ids, tweet_entity_labels = get_entities(attribute, value['text'], value["annotations"], constants.MORAL_FOUNDATION_TO_QUESTIONS[key], constants.QUESTION_TO_MORAL_FOUNDATION[key])
                ids.extend(tweet_entity_ids)
                entities.extend(tweet_entities)
                entity_labels.extend(tweet_entity_labels)
    return pd.DataFrame(
        {
            'Id': ids,
            'Entity': entities,
            'EntityLabel': entity_labels
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
    entity_labels = []
    for key, filename in filename_map.items():
        counter = 0
        filepath = os.path.join(datasetdir, filename)
        with open(filepath) as f:
            data = json.load(f)
            for attribute, value in data.items():
                #counter += 1
                #if counter > 50:
                #    break
                author_ideology.append(author_label_map[value['author-label']])
                topic.append(topic_label_map[value['issue']])
                ids.append(attribute)
                tweets.append(value['text'])
                tweet_entities, tweet_entity_ids, tweet_entity_labels = get_entities(attribute, value['text'], value["annotations"], constants.MORAL_FOUNDATION_TO_QUESTIONS[key], constants.QUESTION_TO_MORAL_FOUNDATION[key])
                entity_ids.extend(tweet_entity_ids)
                entities.extend(tweet_entities)
                entity_labels.extend(tweet_entity_labels)

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
            'EntityLabels': entity_labels
        }
    )
    return data.merge(entity_data, how='left', on='Id')

def get_entities(id, tweet, annotations, questions, question_to_moral_foundation):
    entity_agreement_map = {}
    entities = []
    ids = []
    labels = []
    for annotation_list in annotations:
        for annotation in annotation_list:
            question_map = {}
            if annotation['label'] not in questions:
                continue
            if annotation['label'] in questions and annotation['label'] in entity_agreement_map:
                question_map = entity_agreement_map[annotation['label']]
            added = False
            entity = tweet[annotation['startOffset']:annotation['endOffset']]
            for question_entity, count in question_map.items():
                if question_entity in entity or entity in question_entity:
                    question_map[question_entity] = count + 1
                    added = True
                    break
            if added == False:
                question_map[entity] = 1
            entity_agreement_map[annotation['label']] = question_map
    for question, question_map in entity_agreement_map.items():
        sorted_map = sorted(question_map.items(), key=lambda item: item[1], reverse=True)
        for entity, count in dict(sorted_map).items():
            if count >= 2:
                entities.append(entity)
                ids.append(id)
                labels.append(question_to_moral_foundation[question])
            break
    return entities, ids, labels

def write_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_results(filename):
    with open(filename) as f:
        return json.load(f)                

    


