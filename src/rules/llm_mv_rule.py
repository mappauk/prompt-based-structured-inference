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
                 renormalize: bool = False,
                 num_return_sequences: int = 2,
                 isseq2seq: bool = False):
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
        self.isseq2seq = isseq2seq
    
    def get_prompt(self, label, dict):
        prompt = self.prompt_map[label]
        return prompt.format(**dict)
    
    def extract_labels(self, output):
        lower_output = output.lower()
        min_index = len(output)
        for label in ['true', 'false']:
            index = lower_output.find(label, 0, min_index)
            if index >= 0 and index < min_index:
                return label
        return None
    
    def score_labels(self, output_row):
        score = 0
        for i in range(len(output_row)):
            if output_row[i] == 'true':
                score += 1
        return max(score/len(output_row), 0.01)
        
    def get_rule_groundings(self, data: pd.DataFrame):
        data_subset = data[self.features].drop_duplicates()
        prompts = []
        output_df_list = []
        scores = []
        prompt_batch = []
        if self.isseq2seq:
            tIndex = self.tokenizer.encode('true')[0]
            fIndex = self.tokenizer.encode('false')[0]
        else:
            tIndex = self.tokenizer.encode('true')[1]
            fIndex = self.tokenizer.encode('false')[1]
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
                for i in range(int(self.num_votes/self.num_return_sequences)):
                    prompt_batch.append(formatted_prompt)
                    if len(prompt_batch) == self.batch_size:
                        prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type))
                        prompt_batch = [] 
            elif self.rule_type == RuleType.MULTI_CLASS:
                for label in self.labels:
                    dict['label'] = label
                    formatted_prompt = self.get_prompt(label, dict)
                    output_df_row = copy.deepcopy(dict)
                    output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                    output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                    output_df_list.append(output_df_row)
                    for i in range(int(self.num_votes/self.num_return_sequences)):
                        prompt_batch.append(formatted_prompt)
                        if len(prompt_batch) == self.batch_size:
                            prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type))
                            prompt_batch = []
        if len(prompt_batch) != 0:
            prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type))
        example_predictions = []
        for i in range(len(prompts)):
            outputs = self.model.generate(
                **prompts[i],
                max_new_tokens=1,
                do_sample=True,
                num_return_sequences=self.num_return_sequences,
                prefix_allowed_tokens_fn=lambda batch_idx, prefix_beam: [tIndex, fIndex],
                return_dict=True,
                output_logits=True,
                temperature=self.temperature, 
                pad_token_id=self.tokenizer.eos_token_id)
            if self.isseq2seq:
                text_outputs = self.tokenizer.batch_decode(outputs.sequences)
            else:
                text_outputs = self.tokenizer.batch_decode(outputs.sequences[:, prompts[i].input_ids.shape[1] - 1:])
            for k in range(int(len(text_outputs)/self.num_return_sequences)):
                for l in range(self.num_return_sequences):
                    next_output = text_outputs[k*self.num_return_sequences + l]
                    example_predictions.append(self.extract_labels(next_output))
        example_predictions = np.array(example_predictions)
        example_predictions = example_predictions.reshape((int(example_predictions.shape[0]/self.num_votes)), self.num_votes)
        scores = []
        for i in range(example_predictions.shape[0]):
            scores.append(self.score_labels(example_predictions[i, :]))
        scores = np.array(scores)
        if self.rule_type == RuleType.MULTI_CLASS:
            scores_by_label = scores.reshape((int(len(scores)/len(self.labels)), len(self.labels)))
            scores = torch.nn.functional.softmax(torch.from_numpy(scores_by_label), dim=1)
        final_scores = scores.flatten().tolist()
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', final_scores)
        result_data.dropna(axis=0, how='any', inplace=True)
        return result_data