from collections import OrderedDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
import pandas as pd
import random
import copy
import torch
import numpy as np

class LLMGSRule(RuleTemplate):
    def __init__(self,
                 name: str,
                 features: list, 
                 labels: list, 
                 head_predicate_format: str,
                 rule_variable_format: str,
                 rule_type: str,
                 batch_size: int, 
                 model: AutoModelForCausalLM, 
                 tokenizer: AutoTokenizer,
                 topk: int,
                 temperature: int,
                 device_type: str,
                 prompt_map: str,
                 num_votes: int,
                 max_generate_tokens: int,
                 num_return_sequences: int = 2):
        super(LLMGSRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.prompt_map = prompt_map
        self.batch_size = batch_size
        self.model = model
        self.tokenizer = tokenizer
        self.topk = topk
        self.temperature = temperature
        self.device_type = device_type
        self.num_votes = num_votes
        self.num_return_sequences = num_return_sequences
        self.max_generate_tokens = max_generate_tokens
    
    def get_prompt(self, label, dict):
        prompt = self.prompt_map[label]
        return prompt.format(**dict)
        
    def get_rule_groundings(self, data: pd.DataFrame):
        data_subset = data[self.features].drop_duplicates()
        prompts = []
        output_df_list = []
        prompt_batch = []
        for index, row in data_subset.iterrows():
            dict = { }
            for feature in self.features:
                dict[feature] = row[feature]
            if self.rule_type == RuleType.BINARY:
                formatted_prompt = self.prompt_map.format(**dict)
                output_df_row = copy.deepcopy(dict)
                output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                output_df_list.append(output_df_row)
                prompt_batch.append(formatted_prompt)
                if len(prompt_batch) == self.batch_size:
                    prompts.append(prompt_batch)
                    prompt_batch = [] 
            elif self.rule_type == RuleType.MULTI_CLASS:
                for label in self.labels:
                    dict['label'] = label
                    formatted_prompt = self.get_prompt(label, dict)
                    output_df_row = copy.deepcopy(dict)
                    output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                    output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                    output_df_list.append(output_df_row)
                    prompt_batch.append(formatted_prompt)
                    if len(prompt_batch) == self.batch_size:
                        prompts.append(prompt_batch)
                        prompt_batch = []
        if len(prompt_batch) != 0:
            prompts.append(prompt_batch)
        example_predictions = []
        for i in range(len(prompts)):
            tokenized_prompt = self.tokenizer(prompts[i], padding=True, return_tensors='pt').to(self.device_type)
            outputs = self.model.generate(
                **tokenized_prompt,
                max_new_tokens=self.max_generate_tokens,
                do_sample=True,
                top_k=self.topk,
                num_return_sequences=self.num_return_sequences,
                temperature=self.temperature, 
                pad_token_id=self.tokenizer.eos_token_id)
            text_outputs = self.tokenizer.batch_decode(outputs)
            example_predictions.extend(text_outputs)
        example_predictions = np.array(example_predictions)
        example_predictions = example_predictions.reshape((int(example_predictions.shape[0]/self.num_votes)), self.num_votes)
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', example_predictions)
        result_data.dropna(axis=0, how='any', inplace=True)
        return result_data