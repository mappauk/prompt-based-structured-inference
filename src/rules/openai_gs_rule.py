from collections import OrderedDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
import pandas as pd
import random
import copy
import torch
import numpy as np

class OAGSRule(RuleTemplate):
    def __init__(self,
                 name: str,
                 features: list, 
                 labels: list, 
                 head_predicate_format: str,
                 rule_variable_format: str,
                 rule_type: str,
                 model: str,
                 messages: str,
                 prompt_format: str):
        super(OAGSRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.model = model
        self.messages = messages
        self.prompt_format = prompt_format

    def get_rule_groundings(self, data: pd.DataFrame):
        data_subset = data[self.features].drop_duplicates()
        prompts = []
        for index, row in data_subset.iterrows():
            dict = { }
            for feature in self.features:
                dict[feature] = row[feature]
            formatted_prompt = self.prompt_format.format(**dict)
            formatted_prompt_message = {
                'role': 'user',
                'content': formatted_prompt
            }
            prompts.append({
                "custom_id": self.rule_variable_format.format(**dict),
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": self.model,
                    "messages": self.messages + [formatted_prompt_message],
                    "max_completion_tokens": 3000,
                    "n": 2, # number of chat completion choices to generate for each input message
                    "prompt_cache_key": "mppauk-" + self.name,
                    "reasoning_effort": "medium",
                    "temperature": 1,
                    "verbosity": "low"
                }
            })
        # fields that might be useful for structured prediction - prediction, response_format
        return prompts