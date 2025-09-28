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
import src.helpers.loaders.model_loader as model_loader

class AIOMFRule(RuleTemplate):
    def __init__(self,
                 name: str,
                 features: list, 
                 labels: list, 
                 head_predicate_format: str,
                 rule_variable_format: str,
                 rule_type: str,
                 messages: str,
                 batch_size: int, 
                 model: AutoModelForCausalLM, 
                 tokenizer: AutoTokenizer,
                 topk: int,
                 temperature: int,
                 device_type: str):
        super(AIOMFRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.model = model
        self.messages = messages
        self.topk = topk
        self.tokenizer = tokenizer
        self.batch_size = batch_size
        self.temperature = temperature
        self.device_type = device_type

    def get_rule_groundings(self, data: pd.DataFrame):
        tweet_groups = data.groupby(['Id'])
        prompts = []
        prompt_batch = []
        ids = []
        for group_name, group in tweet_groups:
            entities = []
            tweet = None
            for index, row in group.iterrows():
                id = row['Id']
                tweet = {
                    'Tweet': row['Tweet']
                }
                if not pd.isna(row['Entity']):
                    entities.append({
                        'Entity': row['Entity']
                    })
            ids.append(id)
            example_str = constants.MF_ALL_IN_ONE_EXAMPLE_FORMAT_FOUNDATION.format(**tweet)
            for entity in entities:
                example_str += constants.MF_ALL_IN_ONE_EXAMPLE_FORMAT_ENTITY.format(**entity)     
            formatted_prompt_messages = self.messages + [{
                'role': 'user',
                'content': example_str
            }]
            formatted_prompt = self.tokenizer.apply_chat_template(formatted_prompt_messages, tokenize=False, add_generation_prompt=True)
            prompt_batch.append(formatted_prompt)
            if len(prompt_batch) == self.batch_size:
                prompts.append(prompt_batch)
                prompt_batch = []
        if len(prompt_batch) != 0:
            prompts.append(prompt_batch)
        example_predictions = []
        #model, tokenizer = model_loader.load_test_model(self.device_type, return_dict=False)
        for i in range(len(prompts)):
            tokenized_prompt = self.tokenizer(prompts[i], padding=True, return_tensors='pt').to(self.device_type)
            outputs = self.model.generate(
                **tokenized_prompt,
                max_new_tokens=200,
                do_sample=True,
                top_k=self.topk,
                num_return_sequences=1,
                temperature=self.temperature, 
                pad_token_id=self.tokenizer.eos_token_id)
            text_outputs = self.tokenizer.batch_decode(outputs[:, tokenized_prompt.input_ids.shape[1] - 1:], skip_special_tokens=True)
            example_predictions.extend(text_outputs)
        result_data = pd.DataFrame({
            'Id': ids,
            'Response': example_predictions
        })
        return result_data