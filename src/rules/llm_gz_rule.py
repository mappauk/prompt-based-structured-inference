from transformers import AutoModelForCausalLM, AutoTokenizer
from src.rules.rule_template import RuleTemplate
import numpy as np
import pandas as pd
import copy
import torch

class LLMGZRule(RuleTemplate):
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
                 device_type: str,
                 prompt_map: str,
                 generation_format: str,
                 num_variations: int):
        super(LLMGZRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.prompt_map = prompt_map
        self.batch_size = batch_size
        self.model = model
        self.tokenizer = tokenizer
        self.device_type = device_type
        self.generation_format = generation_format
        self.num_variations = num_variations
        
    def get_rule_groundings(self, data: pd.DataFrame):
        data_subset = data[self.features].drop_duplicates()
        prompts = []
        output_df_list = []
        scores = []
        start_token_positions = []
        prompt_batch = []
        char_batch_posiitions = []
        for index, row in data_subset.iterrows():
            dict = { }
            for feature in self.features:
                dict[feature] = row[feature]
            for label in self.labels:
                dict['label'] = label
                label_sentences = self.prompt_map[label]
                output_df_row = copy.deepcopy(dict)
                output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                output_df_list.append(output_df_row)
                for sentence in label_sentences:
                    formatted_prompt = sentence.format(**dict)
                    char_batch_posiitions.append(len(formatted_prompt) + 1)
                    formatted_prompt += self.generation_format()
                    prompt_batch.append(formatted_prompt)
                    if len(prompt_batch) == self.batch_size:
                        tokenized_prompt_batch = self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type)
                        prompts.append(tokenized_prompt_batch)
                        for i in range(len(tokenized_prompt_batch)):
                            start_token_positions.append(tokenized_prompt_batch.char_to_token(i, char_batch_posiitions))
                        prompt_batch = []
                        char_batch_posiitions = []
        if len(prompt_batch) != 0:
            tokenized_prompt_batch = self.tokenizer(prompt_batch, padding=True, return_tensors='pt').to(self.device_type)
            prompts.append(tokenized_prompt_batch)
            for i in range(len(tokenized_prompt_batch)):
                start_token_positions.append(tokenized_prompt_batch.char_to_token(i, char_batch_posiitions))
        for i in range(len(prompts)):
            outputs = self.model(input_ids = prompts[i]['input_ids'], attention_mask=prompts[i]['attention_mask'], labels=prompts[i]['input_ids'])
            vocab_probs = torch.nn.functional.softmax(outputs.logits, dim=2).cpu().detach().numpy()
            #token_ids = prompts[i]['input_ids'].cpu().numpy()
            token_ids = prompts[i]['input_ids'].cpu().numpy()[:, 1:]
            batch_token_count = token_ids.shape[1]
            vocab_size = vocab_probs.shape[len(vocab_probs.shape) - 1]
            batch_size = len(prompts[i])
            vocab_start_by_token_index = np.arange(batch_token_count*batch_size)*vocab_size
            flattened_vocab_probs = vocab_probs.flatten()
            flattened_vocab_indicies = vocab_start_by_token_index + token_ids.flatten()
            flattened_token_probs = np.take(flattened_vocab_probs, flattened_vocab_indicies)
            token_probs = np.reshape(flattened_token_probs, (batch_size, batch_token_count))
            for i in range(batch_size):
                index = len(scores)
                score = np.sum(token_probs[i, start_token_positions[index]:])/(batch_token_count - start_token_positions[index])
                scores.append(score)
        scores_by_variation = np.reshape(scores, (int(len(scores)/self.num_variations), self.num_variations))
        scores_across_variations = np.sum(scores_by_variation, axis=1)
        scores_by_label = np.reshape(scores_across_variations, int(len(scores_across_variations)/len(self.labels)), len(self.labels))
        softmax_over_labels = torch.nn.functional.softmax(torch.from_numpy(scores_by_label), dim=1)
        final_scores = softmax_over_labels.flatten().tolist()
        
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', final_scores)
        result_data.dropna(axis=0, how='any', inplace=True)
        return result_data