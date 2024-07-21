import json
import src.helpers.coref_prompt_constants as constants

def generate_one_pass_tf_coref_prompt_format(num_shots, example_filepath):
    with open(example_filepath) as f:
        data = json.load(f)
        for foundation_obj in data:
            if num_shots == 0:
                formatted_prompt = ' '.join([constants.COREF_PROMPT_INSTRUCTIONS_ZERO_SHOT, constants.COREF_PROMPT_QUESTION])
            else:
                positive_examples = foundation_obj['positive_examples']
                negative_examples = foundation_obj['negative_examples']
                formatted_examples = []
                for j in range(num_shots):
                    positive_examples[j]['answer'] = 'True'
                    negative_examples[j]['answer'] = 'False'
                    positive_example = constants.COREF_PROMPT_EXAMPLE.format(**positive_examples[j])
                    negative_example = constants.COREF_PROMPT_EXAMPLE.format(**negative_examples[j])
                    formatted_examples.append(positive_example)
                    formatted_examples.append(negative_example)
                formatted_prompt = ' '.join([constants.COREF_PROMPT_INSTRUCTIONS_FEW_SHOT,' '.join(formatted_examples), constants.COREF_PROMPT_QUESTION])
    return formatted_prompt