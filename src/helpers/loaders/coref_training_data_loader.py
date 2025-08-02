
import src.helpers.prompting.coref_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
import json
import random
import pandas as pd

def answer_conversion(answer):
    return 'coreferent' if answer == 'Yes' else 'distinct'

def get_tf_training_prompt(system_prompt, example_prompt, data, features, labels, tokenizer, ground_truth):
    dict = {}
    for feature in features:
        dict[feature] = data[feature]
    positive_prompt = None
    negative_prompt = None
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
            negative_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    return [positive_prompt, negative_prompt]

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
            "content": constants.COREF_LABEL_TO_CHOICE[ground_truth]
        }
    ]
    return [tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)]


def get_training_data(train_data_input_path, val_data_input_path, tokenizer, rule_type):
    training_data = genia_dataset_loader.preprocess_genia_coref(train_data_input_path)
    training_data['answer'] = training_data['answer'].apply(answer_conversion)
    training_prompts = []
    for item, row in training_data.iterrows():
        if rule_type == 'tf':
            prompts = get_tf_training_prompt(
                constants.COREF_TF_SYSTEM_PROMPT, 
                constants.COREF_TF_PROMPT_EXAMPLE,
                row,
                ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
                ['coreferent', 'distinct'],
                tokenizer,
                row['answer'])
        elif rule_type == 'mc':
            prompts = get_mc_training_prompt(
                constants.COREF_MC_SYSTEM_PROMPT,
                constants.COREF_MC_PROMPT_EXAMPLE,
                row,
                ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
                tokenizer,
                row['answer']
            )
        training_prompts.extend(prompts)

    validation_data = genia_dataset_loader.preprocess_genia_coref(val_data_input_path)
    validation_data['answer'] = validation_data['answer'].apply(answer_conversion)
    validation_prompts = []
    for item, row in validation_data.iterrows():
        if rule_type == 'tf':
            prompts = get_tf_training_prompt(
                constants.COREF_TF_SYSTEM_PROMPT, 
                constants.COREF_TF_PROMPT_EXAMPLE,
                row,
                ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
                ['coreferent', 'distinct'],
                tokenizer,
                row['answer'])
        elif rule_type == 'mc':
            prompts = get_mc_training_prompt(
                constants.COREF_MC_SYSTEM_PROMPT,
                constants.COREF_MC_PROMPT_EXAMPLE,
                row,
                ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
                tokenizer,
                row['answer']
            )
        validation_prompts.extend(prompts)
    return training_prompts, validation_prompts