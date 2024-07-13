import os
import json
import src.helpers.mf_prompt_constants as constants

def generate_one_pass_tf_moral_foundation_prompt_format(prompt_format, example_format, num_shots, example_dir):
    filepath = os.path.join(example_dir, 'moral_foundation_examples.json')
    foundation_prompt_map = {}
    with open(filepath) as f:
        data = json.load(f)
        for foundation_obj in data:
            foundation = foundation_obj['moral_foundation']
            positive_examples = foundation_obj['positive_examples']
            negative_examples = foundation_obj['negative_examples']
            formatted_examples = []
            for i in range(num_shots):
                positive_examples[i]['label'] = foundation
                negative_examples[i]['label'] = foundation
                positive_examples[i]['answer'] = 'True'
                negative_examples[i]['answer'] = 'False'
                positive_example = example_format.format(**positive_examples[i])
                negative_example = example_format.format(**negative_examples[i])
                formatted_examples.append(positive_example)
                formatted_examples.append(negative_example)
            definition = constants.MORAL_FOUNDATION_DEFINITIONS_MAP[foundation]
            formatted_prompt = ' '.join([definition, ' '.join(formatted_examples), prompt_format])
            foundation_prompt_map[foundation] = formatted_prompt
    return foundation_prompt_map

def generate_one_pass_tf_moral_role_prompt_format(prompt_format, example_format, num_shots, example_dir):
    filepath = os.path.join(example_dir, 'moral_role_examples.json')
    foundation_prompt_map = {}
    with open(filepath) as f:
        data = json.load(f)
        for foundation_obj in data:
            foundation = foundation_obj['moral_role']
            positive_examples = foundation_obj['positive_examples']
            negative_examples = foundation_obj['negative_examples']
            formatted_examples = []
            for i in range(num_shots):
                positive_examples[i]['label'] = foundation
                negative_examples[i]['label'] = foundation
                positive_examples[i]['answer'] = 'True'
                negative_examples[i]['answer'] = 'False'
                positive_example = example_format.format(**positive_examples[i])
                negative_example = example_format.format(**negative_examples[i])
                formatted_examples.append(positive_example)
                formatted_examples.append(negative_example)
            definition = constants.MORAL_FOUNDATION_DEFINITIONS_MAP[foundation]
            formatted_prompt = ' '.join([definition, ' '.join(formatted_examples), prompt_format])
            foundation_prompt_map[foundation] = formatted_prompt
    return foundation_prompt_map

def generate_all_vs_one_moral_foundation_prompt_format(prompt_format, example_format, num_shots, example_dir):
    filepath = os.path.join(example_dir, 'moral_foundation_examples.json')
    foundation_prompt_map = {}
    with open(filepath) as f:
        data = json.load(f)
        for foundation_obj in data:
            foundation = foundation_obj['moral_foundation']
            positive_examples = foundation_obj['positive_examples']
            negative_examples = foundation_obj['negative_examples']
            formatted_examples = []
            for i in range(num_shots):
                positive_examples[i]['label'] = foundation
                negative_examples[i]['label'] = foundation
                positive_examples[i]['answer'] = 'True'
                negative_examples[i]['answer'] = 'False'
                positive_example = example_format.format(**positive_examples[i])
                negative_example = example_format.format(**negative_examples[i])
                formatted_examples.append(positive_example)
                formatted_examples.append(negative_example)
            definition = constants.MORAL_FOUNDATION_ALL_DEFINITION
            formatted_prompt = ' '.join([definition, ' '.join(formatted_examples), prompt_format])
            foundation_prompt_map[foundation] = formatted_prompt
    return foundation_prompt_map



