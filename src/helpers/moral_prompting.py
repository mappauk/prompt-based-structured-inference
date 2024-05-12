import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import src.helpers.prompt_constants as constants

def load_mistral_model(device_type: str):
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1", device_map=device_type, return_dict_in_generate=True)
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def load_test_model():
    model = AutoModelForCausalLM.from_pretrained("facebook/opt-125m", device_map="cuda", return_dict_in_generate=True)
    tokenizer = AutoTokenizer.from_pretrained("facebook/opt-125m")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def load_mixtral_model():
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x7B-v0.1", torch_dtype=torch.float16, attn_implementation="flash_attention_2")
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
    predicted_foundation = ''
    for foundation in possible_foundations:
        index = lower_output.find(foundation, 0, min_index)
        if index >= 0 and index < min_index:
            min_index = index
            predicted_foundation = foundation
    return predicted_foundation

def generate_one_pass_tf_prompt(num_shots):
    examples = []
    for mf in constants.MORAL_FOUNDATION_DEFINITIONS_MAP.keys(): 
            positive_examples = constants.MORAL_FOUNDATION_POSITIVE_EXAMPLES_MAP[mf][0:num_shots]
            negative_examples = constants.MORAL_FOUNDATION_NEGATIVE_EXAMPLES_MAP[mf][0:num_shots]
            for i in range(num_shots):
                examples.append(constants.MORAL_FOUNDATION_IDENTIFICATION_EXAMPLE_FORMAT.format(positive_examples[i], mf, "True"))
                examples.append(constants.MORAL_FOUNDATION_IDENTIFICATION_EXAMPLE_FORMAT.format(negative_examples[i], mf, "False"))
    return constants.MORAL_FOUNDATION_IDENTIFICATION_ONE_PASS_TF.format(' '.join(examples))

def generate_one_pass_tf_role_prompt(num_shots):
    for role in constants.MORAL_FOUNDATION_ROLE:
        negative_examples = 