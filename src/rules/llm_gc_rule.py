from transformers import AutoModelForCausalLM, AutoTokenizer
from src.rules.rule_template import RuleTemplate
from src.rules.rule_type import RuleType
import numpy as np
import pandas as pd
import copy
import torch

class LLMGCRule(RuleTemplate):
    def __init__(self,
                 name: str,
                 features: list, 
                 labels: list, 
                 head_predicate_format: str,
                 rule_variable_format: str,
                 rule_type: str,
                 model: AutoModelForCausalLM, 
                 tokenizer: AutoTokenizer,
                 device_type: str,
                 prompt_map: str,
                 generation_format: str,
                 num_variations: int):
        super(LLMGCRule, self).__init__(name, features, labels, head_predicate_format, rule_variable_format, rule_type)
        self.prompt_map = prompt_map
        self.model = model
        self.tokenizer = tokenizer
        self.device_type = device_type
        self.generation_format = generation_format
        self.num_variations = num_variations
        
    def get_rule_groundings(self, data: pd.DataFrame):
        data_subset = data[self.features].drop_duplicates()
        prompts = []
        output_df_list = []
        char_prompt_positions = []
        for index, row in data_subset.iterrows():
            dict = { }
            for feature in self.features:
                dict[feature] = row[feature]
            if self.rule_type == RuleType.BINARY:
                output_df_row = copy.deepcopy(dict)
                output_df_row['RuleVariable'] = self.rule_variable_format.format(**dict)
                output_df_row['HeadVariable'] = self.head_variable_format.format(**dict)
                output_df_list.append(output_df_row)
                for variation in self.prompt_map:
                    formatted_prompt = variation.format(**dict)
                    char_prompt_positions.append(len(formatted_prompt))
                    formatted_prompt += self.generation_format.format(**dict)
                    prompts.append(formatted_prompt)
            elif self.rule_type == RuleType.MULTI_CLASS:
                for label in self.labels:
                    dict['label'] = label
                    if self.rule_type == RuleType.MULTI_CLASS:
                        output_df_row = copy.deepcopy(dict)
                        output_df_row['RuleVariable'] = self.rule_variable_format.format(**output_df_row)
                        output_df_row['HeadVariable'] = self.head_variable_format.format(**output_df_row)
                        output_df_list.append(output_df_row)
                    for variation in self.prompt_map:
                        formatted_prompt = variation.format(**dict)
                        char_prompt_positions.append(len(formatted_prompt))
                        formatted_prompt += self.generation_format.format(**dict)
                        prompts.append(formatted_prompt)
        output_logits_list = []
        output_probs_list = []
        for i in range(len(prompts)):
            tokenized_prompt = self.tokenizer(prompts[i], padding=True, return_tensors='pt').to(self.device_type)
            with torch.no_grad():
                # output of model is of shape (batch_size, num_tokens, vocab_size)
                outputs = self.model(input_ids = tokenized_prompt['input_ids'], attention_mask=tokenized_prompt['attention_mask'])
            # get starting token position to evaluate probability of the "generated" sequence given the rest of the prompt as context
            start_token_position = tokenized_prompt.char_to_token(char_prompt_positions[i]) - 1
            # get output logits
            output_logits = outputs.logits.cpu().detach().numpy()
            flattened_output_logits = output_logits.flatten()
            # get output token proabilities over the vocab
            output_probs = torch.nn.functional.softmax(outputs.logits, dim=2).cpu().detach().numpy()
            flattened_output_probs = output_probs.flatten()
            # get token ids starting at position 1, because the output logits at position i are predicting the token at position i + 1
            token_ids = tokenized_prompt['input_ids'].cpu().numpy()[:, 1:]
            # flattened token indicies to select
            vocab_size = output_logits.shape[len(output_logits.shape) - 1]
            prompt_token_count = token_ids.shape[1]
            vocab_start_by_token_index = np.arange(prompt_token_count)*vocab_size
            selection_indicies = vocab_start_by_token_index + token_ids.flatten()
            # get logits/probs for each token
            selected_token_probs = np.take(flattened_output_probs, selection_indicies)[start_token_position:]
            selected_token_logits = np.take(flattened_output_logits, selection_indicies)[start_token_position:]
            output_probs_list.append(selected_token_probs)
            output_logits_list.append(selected_token_logits)
        # combine probs/logits over all variations for a particular example
        final_scores = []
        for i in range(0, len(output_logits_list), self.num_variations):
            final_scores.append(
                {
                    'probs': np.array(output_probs_list[i: i + self.num_variations]),
                    'logits': np.array(output_logits_list[i: i + self.num_variations]),
                }
            )
        result_data = pd.DataFrame(output_df_list)
        result_data.insert(0, 'Score', final_scores)
        result_data.dropna(axis=0, how='any', inplace=True)
        return result_data