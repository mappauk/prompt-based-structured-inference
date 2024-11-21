import json
import src.helpers.prompting.coref_prompt_constants as constants

def generate_one_pass_tf_coref_prompt_format(num_shots, example_filepath):
    with open(example_filepath) as f:
        data = json.load(f)
        if num_shots == 0:
            positive_prompt = ' '.join([constants.COREF_PROMPT_INSTRUCTIONS_ZERO_SHOT, constants.COREF_PROMPT_QUESTION])
            negative_prompt = ' '.join([constants.COREF_PROMPT_INSTRUCTIONS_ZERO_SHOT_NONCOREF, constants.COREF_PROMPT_QUESTION_NONCOREF])
        else:
            positive_examples = data['positive_examples']
            negative_examples = data['negative_examples']
            formatted_examples_coref = []
            formatted_examples_noncoref = []
            for j in range(num_shots):
                # coref examples
                positive_example_coref = constants.COREF_PROMPT_EXAMPLE.format(**positive_examples[j])
                negative_example_coref = constants.COREF_PROMPT_EXAMPLE.format(**negative_examples[j])
                formatted_examples_coref.append(positive_example_coref)
                formatted_examples_coref.append(negative_example_coref)
                # non coref examples
                positive_examples[j]['answer'] = 'false'
                negative_examples[j]['answer'] = 'true'
                positive_example_noncoref = constants.COREF_PROMPT_EXAMPLE_NONCOREF.format(**negative_examples[j])
                negative_example_noncoref = constants.COREF_PROMPT_EXAMPLE_NONCOREF.format(**positive_examples[j])
                formatted_examples_noncoref.append(positive_example_noncoref)
                formatted_examples_noncoref.append(negative_example_noncoref)
            positive_prompt = ' '.join([constants.COREF_PROMPT_INSTRUCTIONS_FEW_SHOT,' '.join(formatted_examples_coref), constants.COREF_PROMPT_QUESTION])
            negative_prompt = ' '.join([constants.COREF_PROMPT_INSTRUCTIONS_FEW_SHOT_NONCOREF,' '.join(formatted_examples_noncoref), constants.COREF_PROMPT_QUESTION_NONCOREF])
    prompt_map = {
        'coref': positive_prompt,
        'nocoref': negative_prompt
    }
    return prompt_map

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