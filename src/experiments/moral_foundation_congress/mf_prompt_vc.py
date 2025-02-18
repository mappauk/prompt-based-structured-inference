import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.llm_vc_rule import LLMVCRule
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict


def main():
    # hyperparamaters
    device_type = 'cuda'
    topk = 5
    temperature = 0.5
    num_votes = 10
    num_return_sequences = 2
    prompt_batch_size = 8
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # load data
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)


    data = data.head(20)

    # generate moral foundation prompt format strings
    foundation_prompt = constants.MF_VERB_CONF_SELF_PROBING_PROMPT_FORMAT
    foundation_prompt_with_features = constants.MF_VERB_CONF_SELF_PROBING_PROMPT_FORMAT_WITH_CONTEXT

    # generate moral role prompt format strings
    role_prompt = constants.ROLE_VERB_CONF_SELF_PROBING_PROMPT_FORMAT
    role_prompt_with_features = constants.ROLE_VERB_CONF_SELF_PROBING_PROMPT_FORMAT_WITH_CONTEXT

    # load model
    model, tokenizer = model_loader.load_test_model(device_type)
    #model, tokenizer = model_loader.load_mistral_instruct_model(device_type)

    # define rules
    rule_one = LLMVCRule(
        'rule_one',
        ['Id', 'Tweet'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleOne_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        foundation_prompt,
        num_votes,
        num_return_sequences
    )

    rule_two = LLMVCRule(
        'rule_two',
        ['Id', 'Tweet', 'Entity'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleTwo_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        role_prompt,
        num_votes,
        num_return_sequences
    )
    rule_three = LLMVCRule(
        'rule_three',
        ['Id', 'Tweet', 'Topic', 'Ideology'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleThree_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        foundation_prompt_with_features,
        num_votes,
        num_return_sequences
    )
    rule_four = LLMVCRule(
        'rule_four',
        ['Id', 'Tweet', 'Entity', 'Ideology', 'Topic'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleFour_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size, 
        model, 
        tokenizer, 
        topk, 
        temperature, 
        device_type,
        role_prompt_with_features,
        num_votes,
        True
    )
    rules = {
        rule_one.name: rule_one, 
        rule_two.name: rule_two, 
        rule_three.name: rule_three, 
        rule_four.name: rule_four
    }

    # get rule groundings:
    prompt_data_loader.save_rule_groundings(rules, data, output_path)

if __name__ == "__main__":
    main()