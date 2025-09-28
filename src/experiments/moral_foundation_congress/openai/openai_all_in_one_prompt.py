import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.openai_all_in_one_mf_rule import AIOMFRule
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
    model_name = 'gpt-5'
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)
    # generate moral foundation prompt format strings
    foundation_messages = moral_prompting.generate_allinone_openai_prompts(
        constants.MF_ALL_IN_ONE_SYSTEM_PROMPT, 
        num_shots, 
        os.path.join(example_path, 'mf_all_in_one_examples.json')
    )

    rule_one = AIOMFRule(
        'all_in_one_rule',
        ['Id', 'Tweet'],
        constants.MORAL_FOUNDATIONS,
        'AllInOne_{Id}',
        'AllInOne_{Id}',
        RuleType.MULTI_CLASS,
        model_name,
        foundation_messages,
    )

    rules = {
        rule_one.name: rule_one
    }
    # get rule groundings:
    prompt_data_loader.save_rule_grounding_batches(rules, data, output_path)


if __name__ == "__main__":
    main()
