from collections import OrderedDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.rules.rule_type import RuleType
from src.rules.rule_template import RuleTemplate
import pandas as pd
import random
import copy
import torch
import numpy as np

class LLMMV2Rule(RuleTemplate):
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
        super(LLMMV2Rule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
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
    
    def get_prompt(self, dict):
        prompt = self.prompt_map
        return prompt.format(**dict)
    
    def extract_labels(self, output):
        lower_output = output.upper()
        min_index = len(output)
        for label in self.labels:
            index = lower_output.find(label, 0, min_index)
            if index >= 0 and index < min_index:
                return label
        return None
    
    def score_labels(self, output_row):
        label_dict = {}
        for i in range(len(output_row)):
            if output_row[i] not in label_dict:
                label_dict[output_row[i]] = 1
            else:
                label_dict[output_row[i]] = label_dict[output_row[i]] + 1
        label_scores = []
        for label in self.labels:
            if label in label_dict:
                label_scores.append(label_dict[label])
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
            formatted_prompt = self.get_prompt(dict)
            for i in range(int(self.num_votes/self.num_return_sequences)):
                prompt_batch.append(formatted_prompt)
                if len(prompt_batch) == self.batch_size:
                    prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt'))
                    prompt_batch = []
        if len(prompt_batch) != 0:
            prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt'))
        example_predictions = []
        print('Memory After Batching:')
        print(torch.cuda.mem_get_info())
        for i in range(len(prompts)):
            print('Batch ' + str(i) + ':')
            print('Memory before generate: ')
            print(torch.cuda.mem_get_info())
            prompts[i] = prompts[i].to(self.device_type)
            outputs = self.model.generate(
                **prompts[i], 
                max_new_tokens=10, 
                do_sample=True,
                num_return_sequences=self.num_return_sequences,
                temperature=self.temperature, 
                pad_token_id=self.tokenizer.eos_token_id)
            text_outputs = self.tokenizer.batch_decode(outputs.sequences[:, prompts[i].input_ids.shape[1] - 1:])
            for k in range(int(len(text_outputs)/self.num_return_sequences)):
                for l in range(self.num_return_sequences):
                    next_output = text_outputs[k*self.num_return_sequences + l]
                    example_predictions.append(self.extract_labels(next_output))
            print('Memory after generate: ')
            print(torch.cuda.mem_get_info())
        example_predictions = np.array(example_predictions)
        example_predictions = example_predictions.reshape((int(example_predictions.shape[0]/self.num_votes)), self.num_votes)
        scores = []
        for i in range(example_predictions.shape[0]):
            scores.extend(self.score_labels(example_predictions[i, :]))
        scores = np.array(scores)
        scores_by_label = scores.reshape((int(len(scores)/len(self.labels)), len(self.labels)))
        softmax_scores = torch.nn.functional.softmax(torch.from_numpy(scores_by_label), dim=1)
        final_scores = softmax_scores.flatten().tolist()
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', final_scores)
        result_data.dropna(axis=0, how='any', inplace=True)
        return result_data
