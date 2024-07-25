from collections import OrderedDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
import pandas as pd
import random
import copy
import torch
import numpy as np

class LLMMVRule(RuleTemplate):
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
                 num_return_sequences: int,
                 renormalize: bool = False):
        super(LLMMVRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.prompt_map = prompt_map
        self.batch_size = batch_size
        self.model = model
        self.tokenizer = tokenizer
        self.topk = topk
        self.temperature = temperature
        self.device_type = device_type
        self.renormalize = renormalize
        self.num_votes = num_votes
        self.num_return_sequences = num_return_sequences
    
    def get_prompt(self, label, dict):
        prompt = self.prompt_map[label]
        return prompt.format(**dict)
    
    def extract_labels(output, labels):
        lower_output = output.upper()
        min_index = len(output)
        for label in labels:
            index = lower_output.find(label, 0, min_index)
            if index >= 0 and index < min_index:
                return label
        return None
    
    def score_labels(output_row, labels):
        label_dict = {}
        for i in range(len(output_row)):
            if output_row[i] not in label_dict:
                label_dict[output_row[i]] = 1
            else:
                label_dict[output_row[i]] = label_dict[output_row[i]] + 1
        label_scores = []
        for label in labels:
            if label in label_dict:
                label_scores.append(label_dict[label] + 0.01)
            else:
                label_scores.append(0.01)
        return label_scores
        
    def get_rule_groundings(self, data: pd.DataFrame):
        data_subset = data[self.features].drop_duplicates()
        prompts = []
        output_df_list = []
        scores = []
        prompt_batch = []
        for index, row in data_subset.iterrows():
            dict = { }
            for feature in self.features:
                dict[feature] = row[feature]
            if self.rule_type == RuleType.BINARY:
                output_df_row = copy.deepcopy(dict)
                output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                output_df_list.append(output_df_row)
            if self.rule_type == RuleType.MULTI_CLASS:
                for label in self.labels:
                    dict['label'] = label
                    output_df_row = copy.deepcopy(dict)
                    output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                    output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                    output_df_list.append(output_df_row)
            formatted_prompt = self.get_prompt(label, dict)
            for i in range(int(self.num_votes/self.num_return_sequences)):
                prompt_batch.append(formatted_prompt)
                if len(prompt_batch) == self.batch_size:
                    prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type))
                    prompt_batch = []
        if len(prompt_batch) != 0:
            prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type))
        for i in range(len(prompts)):
            outputs = self.model.generate(
                **prompts[i], 
                max_new_tokens=10, 
                do_sample=True,
                num_return_sequences=self.num_return_sequences,
                return_dict=True,
                output_logits=True,
                temperature=self.temperature, 
                pad_token_id=self.tokenizer.eos_token_id)
            text_outputs = self.tokenizer.batch_decode(outputs[:, prompts[i].input_ids.shape[1] - 1:])
            for k in range(int(len(text_outputs)/self.num_return_sequences)):
                example_predictions = []
                for l in range(self.num_return_sequences):
                    next_output = text_outputs[k*self.num_return_sequences + l]
                    example_predictions.append(self.extract_labels(next_output))
        example_predictions = np.array(example_predictions)
        example_predictions.reshape((int(example_predictions.shape[0]/self.num_votes)), self.num_votes)
        scores = []
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', scores)
        result_data.dropna(axis=0, how='any', inplace=True)
        return result_data