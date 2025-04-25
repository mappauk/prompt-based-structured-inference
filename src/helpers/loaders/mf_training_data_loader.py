
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import json
import random
import pandas as pd

def get_tf_training_prompt(system_prompt, example_prompt, data, features, labels, tokenizer, ground_truth):
    dict = {}
    for feature in features:
        dict[feature] = data[feature]
    positive_prompt = None
    negative_prompts = []
    for label in labels:
        dict['label'] = label
        formatted_example_prompt = example_prompt.format(**dict)
        is_positive = label == ground_truth
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": formatted_example_prompt
            },
            {
                "role": "assistant",
                "content": "true" if is_positive else "false"
            }
        ]
        if is_positive:
            positive_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        else:
            negative_prompts.append(tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False))
    random_index = random.randint(0, len(negative_prompts) - 1)
    return [positive_prompt, negative_prompts[random_index]]


def get_training_data(data_input_path, rule_split_path, tokenizer):
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(data_input_path)
    mf_labels = dataset_loader.load_frame_labels(data_input_path)
    role_labels = dataset_loader.load_role_labels(data_input_path)

    # exclude few shot example ids from evaluation
    mf_labels = mf_labels[~mf_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
    role_labels = role_labels[~role_labels['Id'].isin(constants.IDS_TO_EXCLUDE)]
    data = data[~data['Id'].isin(constants.IDS_TO_EXCLUDE)]

    # join labels
    data = data.merge(mf_labels, on=['Id'], how='inner')

    train_test_splits = None
    with open(rule_split_path) as f:
        train_test_splits = json.load(f)
    ids_to_prompts = {}

    # rule one prompts
    rule_one_data = data[['Id', 'Tweet', 'Label']].drop_duplicates()
    for item, row in rule_one_data.iterrows():
        prompts = get_tf_training_prompt(
            constants.MF_TF_SYSTEM_PROMPT, 
            constants.MORAL_FOUNDATION_PROMPT_EXAMPLE_FORMAT,
            row,
            ['Id', 'Tweet'], 
            constants.MORAL_FOUNDATIONS,
            tokenizer,
            row['Label'])
        ids_to_prompts[row['Id']] = prompts

    # rule two prompts
    rule_two_data = data[['Id', 'Tweet', 'Entity', 'EntityLabels']].drop_duplicates()
    for item, row in rule_two_data.iterrows():
        if pd.isna(row['Entity']):
            continue
        prompts = get_tf_training_prompt(
            constants.MR_TF_SYSTEM_PROMPT, 
            constants.MORAL_ROLE_PROMPT_EXAMPLE_FORMAT,
            row,
            ['Id', 'Tweet', 'Entity'], 
            constants.MORAL_FOUNDATION_ROLE,
            tokenizer, 
            row['EntityLabels'])
        ids_to_prompts[row['Id']].extend(prompts)
    # rule three prompts
    rule_three_data = data[['Id', 'Tweet', 'Topic', 'Ideology', 'Label']].drop_duplicates()
    for item, row in rule_three_data.iterrows():
        prompts = get_tf_training_prompt(
            constants.MF_TF_SYSTEM_PROMPT, 
            constants.MORAL_FOUNDATION_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
            row,
            ['Id', 'Tweet', 'Topic', 'Ideology'],
            constants.MORAL_FOUNDATIONS,
            tokenizer, 
            row['Label'])
        ids_to_prompts[row['Id']].extend(prompts)

    # rule four prompts
    rule_four_data = data[['Id', 'Tweet', 'Entity', 'Ideology', 'Topic', 'EntityLabels']].drop_duplicates()
    for item, row in rule_four_data.iterrows():
        if pd.isna(row['Entity']):
            continue
        prompts = get_tf_training_prompt(
            constants.MR_TF_SYSTEM_PROMPT, 
            constants.MORAL_ROLE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
            row,
            ['Id', 'Tweet', 'Entity', 'Ideology', 'Topic'], 
            constants.MORAL_FOUNDATION_ROLE,
            tokenizer, 
            row['EntityLabels'])
        ids_to_prompts[row['Id']].extend(prompts)

    return train_test_splits, ids_to_prompts