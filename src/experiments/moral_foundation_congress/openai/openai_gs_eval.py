import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
from src.rules.rule_template import RuleTemplate
import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.helpers.loaders.model_loader as model_loader
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
from src.rules.rule_type import RuleType
from typing import Dict
import os

def transform_openai_response(rule_groundings, responses):
    for rule_name, response_data in responses.items():
        labels = None
        if rule_name == 'rule_one' or rule_name == 'rule_three':
            ids = []
            labels = []
            for response in response_data[rule_name]:
                id = response['custom_id'].split('_')[1]
                response_choices = response['response']['body']['choices']
                choices = []
                for i in range(len(response_choices)):
                    choices.append(response_choices['message']['content'])
            response_dataframe = pd.DataFrame({
                'Id': ids,
                'Labels': labels
            })
            response_dataframe = response_dataframe.groupby(['Id'], sort=False).agg(sum).reset_index()
        else:
            ids = []
            entities = []
            labels = []
            for response in response_data[rule_name]:
                id_split = response['custom_id'].split('_', 2)
                id = id_split[1]
                entity = id_split[2]
                response_choices = response['response']['body']['choices']
                choices = []
                for i in range(len(response_choices)):
                    choices.append(response_choices['message']['content'])
                ids.append(id)
                entities.append(entity)
                labels.append(choices)

            response_dataframe = pd.DataFrame({
                'HeadVariable': ids,
                'Labels': labels
            })
            response_dataframe = response_dataframe.groupby(['Id'], sort=False).agg(sum).reset_index()
            

    


    
        


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    # define rules
    rule_one = RuleTemplate(
        'rule_one',
        ['Id', 'Tweet'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleOne_{Id}_{label}',
        RuleType.MULTI_CLASS
    )
    rule_two = RuleTemplate(
        'rule_two',
        ['Id', 'Tweet', 'Entity'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleTwo_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS
    )
    rule_three = RuleTemplate(
        'rule_three',
        ['Id', 'Tweet', 'Topic', 'Ideology'],
        constants.MORAL_FOUNDATIONS,
        'MF_{Id}_{label}',
        'RuleThree_{Id}_{label}',
        RuleType.MULTI_CLASS
    )
    rule_four = RuleTemplate(
        'rule_four',
        ['Id', 'Tweet', 'Entity', 'Ideology', 'Topic'],
        constants.MORAL_FOUNDATION_ROLE,
        'Role_{Id}_{Entity}_{label}',
        'RuleFour_{Id}_{Entity}_{label}',
        RuleType.MULTI_CLASS
    )
    rules = {
        rule_one.name: rule_one, 
        rule_two.name: rule_two, 
        rule_three.name: rule_three, 
        rule_four.name: rule_four
    }
    data = dataset_loader.load_moral_frame_data_parse_entity_labels(input_path)
    responses = prompt_data_loader.load_rule_grounding_batches(rules, input_path)
    raise Exception()

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
