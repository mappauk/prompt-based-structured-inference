import os
import json
import pandas as pd
import src.helpers.prompting.mf_prompt_constants as constants

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
                #counter += 1
                #if counter > 4:
                #    break
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
                counter += 1
                #if counter > 2:
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

def load_entity_map(datasetdir):
    entities_filepath = os.path.join(datasetdir, 'all_entities.txt')
    entity_map_filepath = os.path.join(datasetdir, 'has_entity_group.txt')
    entity_plain_text_to_id = {}
    entity_map = {}
    with open(entities_filepath, encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            entity_plain_text_to_id[fields[1]] = fields[0]
    with open(entity_map_filepath, encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            if fields[0] in entity_map:
                entity_map[fields[0]].add(fields[1])
            if fields[0] not in entity_map:
                entity_map[fields[0]] = set([fields[1], fields[0]])
            if fields[1] in entity_map:
                entity_map[fields[1]].add(fields[0])
            if fields[1] not in entity_map:
                entity_map[fields[1]] = set([fields[1], fields[0]])
    return entity_plain_text_to_id, entity_map

def get_entity_group_mappings(data, datasetdir):
    entities_filepath = os.path.join(datasetdir, 'entity_groups_final.txt')
    groups = []
    with open(entities_filepath, 'r', encoding='utf8') as file:
        temp_group = set()
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line == '' and len(temp_group) != 0:
                groups.append(temp_group)
                temp_group = set()
            elif line != '':
                temp_group.add(line)
    
    entity_group_map = {}
    entities = data['Entity'].tolist()
    for entity in entities:
        if entity == None or pd.isnull(entity):
            continue
        entity = entity.strip()
        if entity in entity_group_map:
            continue
        entity_groups = []
        for i in range(0, len(groups)):
            if entity in groups[i]:
                entity_groups.append(i)
        entity_group_map[entity] = entity_groups
    return entity_group_map




    


