from collections import OrderedDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
from src.helpers.loaders.utilities import print_gpu_memory_usage
import pandas as pd
import random
import copy
import torch
import numpy as np
import json

class LLMVCRule(RuleTemplate):
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
                 num_samples: int,
                 num_return_sequences: int = 2):
        super(LLMVCRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.prompt_map = prompt_map
        self.batch_size = batch_size
        self.model = model
        self.tokenizer = tokenizer
        self.topk = topk
        self.temperature = temperature
        self.device_type = device_type
        self.num_samples = num_samples
        self.num_return_sequences = num_return_sequences
        
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
                for j in range(int(self.num_samples/self.num_return_sequences)):
                    prompt_batch.append(formatted_prompt)
                    if len(prompt_batch) == self.batch_size:
                        prompts.append(prompt_batch)
                        prompt_batch = []
            elif self.rule_type == RuleType.MULTI_CLASS:
                for label in self.labels:
                    dict['label'] = label
                    formatted_prompt = self.prompt_map.format(**dict)
                    output_df_row = copy.deepcopy(dict)
                    output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                    output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                    output_df_list.append(output_df_row)
                    for j in range(int(self.num_samples/self.num_return_sequences)):
                        prompt_batch.append(formatted_prompt)
                        if len(prompt_batch) == self.batch_size:
                            prompts.append(prompt_batch)
                            prompt_batch = []
        if len(prompt_batch) != 0:
            prompts.append(prompt_batch)
        string_outputs = []
        for i in range(len(prompts)):
            curr_prompt_batch = self.tokenizer(prompts[i], padding=True, return_tensors='pt').to(self.device_type)
            outputs = self.model.generate(
                **curr_prompt_batch,
                max_new_tokens=10,
                do_sample=True,
                num_return_sequences=self.num_return_sequences,
                temperature=self.temperature, 
                pad_token_id=self.tokenizer.eos_token_id)
            text_outputs = self.tokenizer.batch_decode(outputs[:, curr_prompt_batch.input_ids.shape[1] - 1:], skip_special_tokens=True)
            string_outputs.extend(text_outputs)
        string_outputs = np.array(string_outputs)
        string_outputs = string_outputs.reshape((int(string_outputs.shape[0]/self.num_samples)), self.num_samples)
        scores = []
        for i in range(string_outputs.shape[0]):
            scores.append(string_outputs[i, :])
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', scores)
        result_data.dropna(axis=0, how='any', inplace=True)
        return result_data