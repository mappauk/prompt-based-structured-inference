import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSeq2SeqLM, GPTJForCausalLM

def load_mistral_model(device_type: str):
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1", device_map=device_type, return_dict_in_generate=True)
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def load_mistral_instruct_model(device_type: str):
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", device_map=device_type, return_dict_in_generate=True)
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
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

def load_llama_model_small(device_type: str):
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3.1-8B", device_map=device_type, return_dict_in_generate=True)
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def load_llama_model_large(device_type: str):
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-70B", device_map=device_type, return_dict_in_generate=True)
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-70B")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def load_flan_model(device_type: str):
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xl", device_map=device_type, return_dict_in_generate=True)
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xl")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def load_gpt_j_model(device_type: str):
    model = GPTJForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", revision="float16", torch_dtype=torch.float16, device_map=device_type)
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer
    
