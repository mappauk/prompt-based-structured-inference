import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.all_in_one_mf_rule import AIOMFRule
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict
import os

def main():
    input_path = sys.argv[1]
    num_shots = int(sys.argv[2])
    example_path = sys.argv[3]
    output_path = sys.argv[4]
    device_type = 'cuda'
    batch_size = 2
    topk = 5
    temperature = 0.5
    model, tokenizer = model_loader.load_llama_instruct_model(device_type, eight_bit=True, flash_attention_2=True, return_dict=False)

    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)
    #data = data.head(20)
    # generate moral foundation prompt format strings
    foundation_messages = moral_prompting.generate_allinone_prompts(
        constants.MF_ALL_IN_ONE_SYSTEM_PROMPT, 
        num_shots, 
        os.path.join(example_path, 'mf_all_in_one_examples.json'),
        is_openai_format=False
    )

    rule_one = AIOMFRule(
        'all_in_one_rule',
        ['Id', 'Tweet'],
        constants.MORAL_FOUNDATIONS,
        'AllInOne_{Id}',
        'AllInOne_{Id}',
        RuleType.MULTI_CLASS,
        foundation_messages,
        batch_size,
        model,
        tokenizer,
        topk,
        temperature,
        device_type
    )

    rules = {
        rule_one.name: rule_one
    }
    # get rule groundings:
    prompt_data_loader.save_rule_groundings(rules, data, output_path)


if __name__ == "__main__":
    main()