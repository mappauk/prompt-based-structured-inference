from collections import OrderedDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
import pandas as pd
import random
import copy
import torch
import numpy as np
import src.helpers.prompting.mf_prompt_constants as constants


class AIOMFRule(RuleTemplate):
    def __init__(self,
                 name: str,
                 features: list, 
                 labels: list, 
                 head_predicate_format: str,
                 rule_variable_format: str,
                 rule_type: str,
                 model: str,
                 messages: str):
        super(AIOMFRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.model = model
        self.messages = messages

    def get_rule_groundings(self, data: pd.DataFrame):
        tweet_groups = data.groupby(['Id'])
        prompts = []
        for group_name, group in tweet_groups:
            entities = []
            tweet = None
            for index, row in group.iterrows():
                tweet = {
                    'Tweet': row['Tweet']
                }
                if not pd.isna(row['Entity']):
                    entities.append({
                        'Entity': row['Entity']
                    })
            example_str = constants.MF_ALL_IN_ONE_EXAMPLE_FORMAT_FOUNDATION.format(**tweet)
            for entity in entities:
                example_str += constants.MF_ALL_IN_ONE_EXAMPLE_FORMAT_ENTITY.format(**entity)     
            formatted_prompt_message = {
                'role': 'user',
                'content': example_str
            }
            prompts.append({
                "custom_id": self.rule_variable_format.format(**{ 'Id': row['Id']}),
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": self.model,
                    "messages": self.messages + [formatted_prompt_message],
                    "max_completion_tokens": 1000,
                    "n": 2, # number of chat completion choices to generate for each input message
                    "prompt_cache_key": "mppauk-" + self.name,
                    "reasoning_effort": "medium",
                    "temperature": 1,
                    "verbosity": "low"
                },

            })
            # fields that might be useful for structured prediction - prediction, response_format
        return prompts