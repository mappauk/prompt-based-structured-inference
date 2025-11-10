from collections import OrderedDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.rules.rule_template import RuleTemplate
from src.rules.rule_type import RuleType
import numpy as np
import pandas as pd
import random
import copy
import torch

class LLMMCRule(RuleTemplate):
    def __init__(self,
                 name: str,
                 features: list, 
                 labels: list, 
                 head_predicate_format: str,
                 rule_variable_format: str,
                 rule_type: RuleType,
                 batch_size: int,
                 model: AutoModelForCausalLM, 
                 tokenizer: AutoTokenizer,
                 device_type: str,
                 prompt_map,
                 choices: list,
                 isseq2seq: bool = False,
                 prompt_map_key: str = None):
        super(LLMMCRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.prompt_map = prompt_map
        self.batch_size = batch_size
        self.model = model
        self.tokenizer = tokenizer
        self.device_type = device_type
        self.isseq2seq = isseq2seq
        self.choices = choices
        self.prompt_map_key = prompt_map_key
        
    def get_prompt(self, key):
        return self.prompt_map[key]
        
    def get_rule_groundings(self, data: pd.DataFrame):
        data_subset = data[self.features].drop_duplicates()
        data_subset = data_subset.dropna()
        prompts = []
        output_df_list = []
        scores = []
        prompt_batch = []
        choice_token_indicies = []
        for choice in self.choices:
            if self.isseq2seq:
                choice_token_indicies.append(self.tokenizer.encode(choice)[0])
            else:
                choice_token_indicies.append(self.tokenizer.encode(choice)[1])
        for index, row in data_subset.iterrows():
            dict = { }
            for feature in self.features:
                dict[feature] = row[feature]
            prompt_format_str = self.prompt_map
            if self.prompt_map_key != None:
                prompt_format_str = self.get_prompt(dict[self.prompt_map_key])
            formatted_prompt = prompt_format_str.format(**dict)
            prompt_batch.append(formatted_prompt)
            if len(prompt_batch) == self.batch_size:
                prompts.append(prompt_batch)
                prompt_batch = []
            if self.rule_type == RuleType.BINARY:
                output_df_row = copy.deepcopy(dict)
                output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                output_df_list.append(output_df_row) 
            elif self.rule_type == RuleType.MULTI_CLASS:
                for label in self.labels:
                    dict['label'] = label
                    output_df_row = copy.deepcopy(dict)
                    output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                    output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                    output_df_list.append(output_df_row)
        if len(prompt_batch) != 0:
            prompts.append(prompt_batch)
        for i in range(len(prompts)):
            curr_prompt = self.tokenizer(prompts[i], padding=True, return_tensors='pt').to(self.device_type)
            outputs = self.model.generate(
                **curr_prompt, 
                max_new_tokens=1,
                do_sample=True,
                num_return_sequences=1,
                return_dict_in_generate=True,
                output_logits=True,
                pad_token_id=self.tokenizer.eos_token_id)
            output_logits = outputs.logits[0]
            softmax_over_tokens = torch.nn.functional.softmax(outputs.logits[0], dim=1)
            mc_logits = output_logits[:, choice_token_indicies].cpu()
            mc_probs = softmax_over_tokens[:, choice_token_indicies].cpu()
            interm_scores = np.concatenate((mc_logits, mc_probs), axis=1)
            for row in interm_scores:
                for i in range(len(self.choices)):
                    scores.append(row.tolist())
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', scores)
        result_data.dropna(axis=0, how='any', inplace=True)
        return result_data
