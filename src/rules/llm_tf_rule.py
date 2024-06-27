from collections import OrderedDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.helpers import prompt_constants
from src.rules.rule_template import RuleTemplate
import numpy as np
import pandas as pd
import random
import copy
import torch

class LLMTFRule(RuleTemplate):
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
                 renormalize: bool = False):
        super(LLMTFRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.prompt_map = prompt_map
        self.batch_size = batch_size
        self.model = model
        self.tokenizer = tokenizer
        self.topk = topk
        self.temperature = temperature
        self.device_type = device_type
        self.renormalize = renormalize
    
    def get_prompt(self, label, dict):
        prompt = self.prompt_map[label]
        return prompt.format(**dict)
        
    def get_rule_groundings(self, data: pd.DataFrame):
        data_subset = data[self.features].drop_duplicates()
        prompts = []
        output_df_list = []
        scores = []
        prompt_batch = []
        tIndex = self.tokenizer.encode('True')[1]
        fIndex = self.tokenizer.encode('False')[1]
        for index, row in data_subset.iterrows():
            dict = { }
            for feature in self.features:
                dict[feature] = row[feature]
            for label in self.labels:
                dict['label'] = label
                formatted_prompt = self.get_prompt(label, dict)
                output_df_row = copy.deepcopy(dict)
                output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                output_df_list.append(output_df_row)
                prompt_batch.append(formatted_prompt)
                if len(prompt_batch) == self.batch_size:
                    prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type))
                    prompt_batch = []
        if len(prompt_batch) != 0:
            prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type))
        for i in range(len(prompts)):
            outputs = self.model.generate(
                **prompts[i], 
                max_new_tokens=1,
                do_sample=True,
                num_return_sequences=1,
                return_dict=True,
                output_logits=True,
                temperature=self.temperature, 
                pad_token_id=self.tokenizer.eos_token_id)
            softmax_over_tokens = torch.nn.functional.softmax(outputs.logits[0], dim=1)
            softmax_over_answers = torch.nn.functional.softmax(softmax_over_tokens[:, [tIndex, fIndex]], dim=1)
            scores.extend(softmax_over_answers[:, 0].cpu().tolist())
        #for i in range(len(scores)):
        #    scores[i] = random.uniform(0, 1)
        if self.renormalize:
            scores_by_label = np.reshape(scores, (int(len(scores)/len(self.labels)), len(self.labels)))
            softmax_over_labels = torch.nn.functional.softmax(torch.from_numpy(scores_by_label), dim=1)
            scores = softmax_over_labels.flatten().tolist()
        
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', scores)
        return result_data






