
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
    #random_index = random.randint(0, len(negative_prompts) - 1)
    negative_prompts.append(positive_prompt)
    return negative_prompts

def get_mc_training_prompt(system_prompt, example_prompt, data, features, tokenizer, ground_truth):
    dict = {}
    for feature in features:
        dict[feature] = data[feature]
    formatted_example_prompt = example_prompt.format(**dict)
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
            "content": constants.LABEL_TO_MC_LETTER[ground_truth]
        }
    ]
    return [tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)]


def get_training_data(data_input_path, rule_split_path, tokenizer, rules, rule_type='tf'):
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
    if 'rule_one' in rules:
        rule_one_data = data[['Id', 'Tweet', 'Label']].drop_duplicates()
        for item, row in rule_one_data.iterrows():
            if rule_type == 'tf':
                prompts = get_tf_training_prompt(
                    constants.MF_TF_SYSTEM_PROMPT, 
                    constants.MORAL_FOUNDATION_PROMPT_EXAMPLE_FORMAT,
                    row,
                    ['Id', 'Tweet'], 
                    constants.MORAL_FOUNDATIONS,
                    tokenizer,
                    row['Label'])
            elif rule_type == 'mc':
                prompts = get_mc_training_prompt(
                    constants.MF_MC_SYSTEM_PROMPT,
                    constants.MF_MC_EXAMPLE_FORMAT,
                    row,
                    ['Id', 'Tweet'],
                    tokenizer,
                    row['Label']
                )
            ids_to_prompts[row['Id']] = prompts
    # rule two prompts
    if 'rule_two' in rules:
        rule_two_data = data[['Id', 'Tweet', 'Entity', 'EntityLabels']].drop_duplicates()
        for item, row in rule_two_data.iterrows():
            if pd.isna(row['Entity']):
                continue
            if rule_type == 'tf':
                prompts = get_tf_training_prompt(
                    constants.MR_TF_SYSTEM_PROMPT, 
                    constants.MORAL_ROLE_PROMPT_EXAMPLE_FORMAT,
                    row,
                    ['Id', 'Tweet', 'Entity'], 
                    constants.MORAL_FOUNDATION_ROLE,
                    tokenizer, 
                    row['EntityLabels'])
            elif rule_type == 'mc':
                prompts = get_mc_training_prompt(
                    constants.MR_MC_SYSTEM_PROMPT,
                    constants.MR_MC_EXAMPLE_FORMAT,
                    row,
                    ['Id', 'Tweet', 'Entity'], 
                    tokenizer,
                    row['EntityLabels']
                )
            if row['Id'] in ids_to_prompts:
                ids_to_prompts[row['Id']].extend(prompts)
            else:
                ids_to_prompts[row['Id']] = prompts

    # rule three prompts
    if 'rule_three' in rules:
        rule_three_data = data[['Id', 'Tweet', 'Topic', 'Ideology', 'Label']].drop_duplicates()
        for item, row in rule_three_data.iterrows():
            if rule_type == 'tf':
                prompts = get_tf_training_prompt(
                    constants.MF_TF_SYSTEM_PROMPT, 
                    constants.MORAL_FOUNDATION_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
                    row,
                    ['Id', 'Tweet', 'Topic', 'Ideology'],
                    constants.MORAL_FOUNDATIONS,
                    tokenizer, 
                    row['Label'])
            elif rule_type == 'mc':
                prompts = get_mc_training_prompt(
                    constants.MF_MC_SYSTEM_PROMPT,
                    constants.MF_MC_EXAMPLE_FORMAT_WITH_FEATURES,
                    row,
                    ['Id', 'Tweet', 'Topic', 'Ideology'],
                    tokenizer,
                    row['Label']
                )
            if row['Id'] in ids_to_prompts:
                ids_to_prompts[row['Id']].extend(prompts)
            else:
                ids_to_prompts[row['Id']] = prompts

    # rule four prompts
    if 'rule_four' in rules:
        rule_four_data = data[['Id', 'Tweet', 'Entity', 'Ideology', 'Topic', 'EntityLabels']].drop_duplicates()
        for item, row in rule_four_data.iterrows():
            if pd.isna(row['Entity']):
                continue
            if rule_type == 'tf':
                prompts = get_tf_training_prompt(
                    constants.MR_TF_SYSTEM_PROMPT, 
                    constants.MORAL_ROLE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT,
                    row,
                    ['Id', 'Tweet', 'Entity', 'Ideology', 'Topic'], 
                    constants.MORAL_FOUNDATION_ROLE,
                    tokenizer, 
                    row['EntityLabels'])
            elif rule_type == 'mc':
                prompts = get_mc_training_prompt(
                    constants.MR_MC_SYSTEM_PROMPT,
                    constants.MR_MC_EXAMPLE_FORMAT_WITH_FEATURES,
                    row,
                    ['Id', 'Tweet', 'Entity', 'Ideology', 'Topic'], 
                    tokenizer,
                    row['EntityLabels']
                )
            if row['Id'] in ids_to_prompts:
                ids_to_prompts[row['Id']].extend(prompts)
            else:
                ids_to_prompts[row['Id']] = prompts

    return train_test_splits, ids_to_prompts