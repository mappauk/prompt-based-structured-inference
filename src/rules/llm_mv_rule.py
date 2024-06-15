from collections import OrderedDict
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.helpers import prompt_constants
from src.helpers import moral_prompting
from src.rules.rule_template import RuleTemplate
import pandas as pd
import random
import copy
import torch

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
                 label_cluster_map: dict):
        super(LLMMVRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.prompt_map = prompt_map
        self.batch_size = batch_size
        self.model = model
        self.tokenizer = tokenizer
        self.topk = topk
        self.temperature = temperature
        self.device_type = device_type
        self.num_votes = num_votes
        self.num_return_sequences = num_return_sequences
        self.prompt_label_cluster_map = label_cluster_map
    
    def get_prompt(self, label, dict):
        prompt = self.prompt_map[label]
        return prompt.format(**dict)
        
    def get_rule_groundings(self, data: pd.DataFrame):
        data_subset = data[self.features].drop_duplicates()
        prompts = []
        output_df_list = []
        scores = []
        prompt_batch = []
        prompt_clusers = []
        for index, row in data_subset.iterrows():
            dict = { }
            for feature in self.features:
                dict[feature] = row[feature]
            for cluster, labels in self.prompt_label_cluster_map.items():
                formatted_prompt = self.get_prompt(cluster, dict)
                prompt_batch.append(formatted_prompt)
                prompt_clusers.append(cluster)
                if len(prompt_batch) == self.batch_size:
                    prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type))
                    prompt_batch = []
                for label in labels:
                    dict['label'] = label
                    output_df_row = copy.deepcopy(dict)
                    output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                    output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                    output_df_list.append(output_df_row)
        if len(prompt_batch) != 0:
            prompts.append(self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type))
        for i in range(len(prompts)):
            prompt_batch_votes = [dict() for x in range(prompts[i])]
            for j in range(self.num_votes):
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
                    for l in range(self.num_return_sequences):
                        next_output = text_outputs[k*self.num_return_sequences + l]
                        extracted_mf_output = moral_prompting.extract_moral_foundation_label(next_output)
                        if extracted_mf_output != None and extracted_mf_output in prompt_batch_votes[k]:
                            prompt_batch_votes[k][extracted_mf_output] = prompt_batch_votes[k][extracted_mf_output] + 1
                        elif extracted_mf_output != None:
                            prompt_batch_votes[k][extracted_mf_output] = 1
            for j in range(prompts[i]):
                label_cluster = prompt_clusers[i*self.batch_size + j]
                labels = self.prompt_label_cluster_map[label_cluster]
                for k in range(len(labels)):
                    if label in prompt_batch_votes[j]:
                        scores.append(prompt_batch_votes[j]/(self.num_votes*self.num_return_sequences) + 0.01)
                    else:
                        scores.append(0.01)
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', scores)
        return result_data
                                    

                        





        
        result_data = pd.DataFrame(output_df_list)
        for i in range(len(scores)):
            scores[i] = random.uniform(0, 1)
        result_data.insert(0, 'Score', scores)
        return result_data






