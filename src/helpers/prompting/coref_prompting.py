import json
import src.helpers.prompting.coref_prompt_constants as constants

def generate_one_pass_tf_coref_prompt_format(num_shots, example_filepath):
    with open(example_filepath) as f:
        data = json.load(f)
        if num_shots == 0:
            formatted_prompt = ' '.join([constants.COREF_PROMPT_INSTRUCTIONS_ZERO_SHOT, constants.COREF_PROMPT_QUESTION])
        else:
            positive_examples = data['positive_examples']
            negative_examples = data['negative_examples']
            formatted_examples = []
            for j in range(num_shots):
                positive_example = constants.COREF_PROMPT_EXAMPLE.format(**positive_examples[j])
                negative_example = constants.COREF_PROMPT_EXAMPLE.format(**negative_examples[j])
                formatted_examples.append(positive_example)
                formatted_examples.append(negative_example)
            formatted_prompt = ' '.join([constants.COREF_PROMPT_INSTRUCTIONS_FEW_SHOT,' '.join(formatted_examples), constants.COREF_PROMPT_QUESTION])
    return formatted_prompt

def generate_one_pass_gz_coref_prompt_format(num_variations, example_path, num_shots):
    with open(example_path) as f:
        data = json.load(f)
        positive_prompts = []
        negative_prompts = []
        for i in range(num_variations):
            positive_prompt_format = constants.GEN_Z_COREF_EXAMPLE_FORMAT.format(constants.GEN_Z_COREF_LABEL_SENTENCES_POSITIVE[i])
            negative_prompt_format = constants.GEN_Z_COREF_EXAMPLE_FORMAT.format(constants.GEN_Z_COREF_LABEL_SENTENCES_NEGATIVE[i])
            if num_shots == 0:
                positive_prompts.append(' '.join([constants.GEN_Z_COREF_INTRO_ZERO_SHOT, positive_prompt_format]))
                negative_prompts.append(' '.join([constants.GEN_Z_COREF_INTRO_ZERO_SHOT, negative_prompt_format]))
            else:
                positive_examples = data['positive_examples']
                negative_examples = data['negative_examples']
                positive_example_prompts = []
                negative_example_prompts = []
                for j in range(num_shots):
                    positive_example_prompts.append((positive_prompt_format + constants.GEN_Z_COREF_FORMAT).format(**positive_examples[j]))
                    negative_example_prompts.append((negative_prompt_format + constants.GEN_Z_COREF_FORMAT).format(**negative_examples[j]))
                positive_prompts.append(' '.join([constants.GEN_Z_COREF_INTRO_FEW_SHOT, ' '.join(positive_example_prompts), positive_prompt_format]))
                negative_prompts.append(' '.join([constants.GEN_Z_COREF_INTRO_FEW_SHOT, ' '.join(negative_example_prompts), negative_prompt_format]))
    prompt_map = {
        'coref': positive_prompts,
        'nocoref': negative_prompts
    }
    return prompt_map