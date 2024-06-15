import torch
import os
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import src.helpers.prompt_constants as constants

def load_mistral_model(device_type: str):
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1", device_map=device_type, return_dict_in_generate=True)
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def load_test_model(device_type: str):
    model = AutoModelForCausalLM.from_pretrained("facebook/opt-125m", device_map=device_type, return_dict_in_generate=True)
    tokenizer = AutoTokenizer.from_pretrained("facebook/opt-125m")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def load_mixtral_model(device_type: str):
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x7B-v0.1", device_map=device_type, torch_dtype=torch.float16, attn_implementation="flash_attention_2")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x7B-v0.1")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def generate_moral_foundation_identification_prompt_one_pass(tweet):
    return constants.MORAL_FOUNDATION_IDENTIFICATION_ONE_PASS.format(tweet)

def extract_moral_foundation_label(output):
    possible_foundations = constants.MORAL_FOUNDATION_DEFINITIONS_MAP.keys()
    lower_output = output.upper()
    min_index = len(output)
    for foundation in possible_foundations:
        index = lower_output.find(foundation, 0, min_index)
        if index >= 0 and index < min_index:
            return foundation
    return None

def generate_one_pass_tf_moral_foundation_prompt_format(prompt_format, example_format, num_shots, example_dir):
    filepath = os.path.join(example_dir, 'moral_foundation_examples.json')
    foundation_prompt_map = {}
    with open(filepath) as f:
        data = json.load(f)
        for foundation_obj in data:
            foundation = foundation_obj['moral_foundation']
            positive_examples = foundation_obj['positive_examples']
            negative_examples = foundation_obj['negative_examples']
            formatted_examples = []
            for i in range(num_shots):
                positive_examples[i]['label'] = foundation
                negative_examples[i]['label'] = foundation
                positive_examples[i]['answer'] = 'True'
                negative_examples[i]['answer'] = 'False'
                positive_example = example_format.format(**positive_examples[i])
                negative_example = example_format.format(**negative_examples[i])
                formatted_examples.append(positive_example)
                formatted_examples.append(negative_example)
            definition = constants.MORAL_FOUNDATION_DEFINITIONS_MAP[foundation]
            formatted_prompt = ' '.join([definition, ' '.join(formatted_examples), prompt_format])
            foundation_prompt_map[foundation] = formatted_prompt
    return foundation_prompt_map

def generate_one_pass_tf_moral_role_prompt_format(prompt_format, example_format, num_shots, example_dir):
    filepath = os.path.join(example_dir, 'moral_role_examples.json')
    foundation_prompt_map = {}
    with open(filepath) as f:
        data = json.load(f)
        for foundation_obj in data:
            foundation = foundation_obj['moral_role']
            positive_examples = foundation_obj['positive_examples']
            negative_examples = foundation_obj['negative_examples']
            formatted_examples = []
            for i in range(num_shots):
                positive_examples[i]['label'] = foundation
                negative_examples[i]['label'] = foundation
                positive_examples[i]['answer'] = 'True'
                negative_examples[i]['answer'] = 'False'
                positive_example = example_format.format(**positive_examples[i])
                negative_example = example_format.format(**negative_examples[i])
                formatted_examples.append(positive_example)
                formatted_examples.append(negative_example)
            definition = constants.MORAL_FOUNDATION_DEFINITIONS_MAP[foundation]
            formatted_prompt = ' '.join([definition, ' '.join(formatted_examples), prompt_format])
            foundation_prompt_map[foundation] = formatted_prompt
    return foundation_prompt_map

def generate_all_vs_one_moral_foundation_prompt_format(prompt_format, example_format, num_shots, example_dir):
    filepath = os.path.join(example_dir, 'moral_foundation_examples.json')
    foundation_prompt_map = {}
    with open(filepath) as f:
        data = json.load(f)
        for foundation_obj in data:
            foundation = foundation_obj['moral_foundation']
            positive_examples = foundation_obj['positive_examples']
            negative_examples = foundation_obj['negative_examples']
            formatted_examples = []
            for i in range(num_shots):
                positive_examples[i]['label'] = foundation
                negative_examples[i]['label'] = foundation
                positive_examples[i]['answer'] = 'True'
                negative_examples[i]['answer'] = 'False'
                positive_example = example_format.format(**positive_examples[i])
                negative_example = example_format.format(**negative_examples[i])
                formatted_examples.append(positive_example)
                formatted_examples.append(negative_example)
            definition = constants.MORAL_FOUNDATION_ALL_DEFINITION
            formatted_prompt = ' '.join([definition, ' '.join(formatted_examples), prompt_format])
            foundation_prompt_map[foundation] = formatted_prompt
    return foundation_prompt_map



