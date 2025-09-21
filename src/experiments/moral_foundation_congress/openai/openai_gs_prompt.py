import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.openai_gs_rule import OAGSRule
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
    foundation_messages, foundation_prompt = moral_prompting.generate_gs_openai_prompts(
        constants.MF_GS_SYSTEM_PROMPT, 
        constants.MF_GS_EXAMPLE_FORMAT,
        num_shots, 
        os.path.join(example_path, 'moral_foundation_examples.json')
    )
    foundation_messages_with_features, foundation_prompt_with_features = moral_prompting.generate_gs_openai_prompts(
        constants.MF_GS_SYSTEM_PROMPT, 
        constants.MF_GS_EXAMPLE_FORMAT_WITH_FEATURES,
        num_shots,
        os.path.join(example_path, 'moral_foundation_examples.json')
    )
    # generate moral role prompt format strings
    role_messages, role_prompt = moral_prompting.generate_gs_openai_prompts(
        constants.MR_GS_SYSTEM_PROMPT, 
        constants.MR_GS_EXAMPLE_FORMAT,
        num_shots,
        os.path.join(example_path, 'moral_role_examples.json')
    )
    role_messages_with_features, role_prompt_with_features = moral_prompting.generate_gs_openai_prompts(
        constants.MR_GS_SYSTEM_PROMPT, 
        constants.MR_GS_EXAMPLE_FORMAT_WITH_FEATURES,
        num_shots,
        os.path.join(example_path, 'moral_role_examples.json')
    )

    rule_one = OAGSRule(
        'rule_one',
        ['Id', 'Tweet'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}',
        'RuleOne_{Id}',
        RuleType.MULTI_CLASS,
        model_name,
        foundation_messages,
        foundation_prompt
    )
    rule_two = OAGSRule(
        'rule_two',
        ['Id', 'Tweet', 'Entity'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}',
        'RuleTwo_{Id}_{Entity}',
        RuleType.MULTI_CLASS,
        model_name,
        role_messages,
        role_prompt
    )
    rule_three = OAGSRule(
        'rule_three',
        ['Id', 'Tweet', 'Topic', 'Ideology'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}',
        'RuleThree_{Id}',
        RuleType.MULTI_CLASS,
        model_name,
        foundation_messages_with_features,
        foundation_prompt_with_features
    )
    rule_four = OAGSRule(
        'rule_four',
        ['Id', 'Tweet', 'Entity', 'Ideology', 'Topic'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}',
        'RuleFour_{Id}_{Entity}',
        RuleType.MULTI_CLASS,
        model_name,
        role_messages_with_features,
        role_prompt_with_features
    )
    rules = {
        rule_one.name: rule_one, 
        rule_two.name: rule_two, 
        rule_three.name: rule_three, 
        rule_four.name: rule_four
    }
    # get rule groundings:
    prompt_data_loader.save_rule_grounding_batches(rules, data, output_path)


if __name__ == "__main__":
    main()
