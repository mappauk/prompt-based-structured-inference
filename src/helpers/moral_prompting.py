import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import helpers.prompt_constants as constants

def load_mistral_model():
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1", device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
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