import os
import json
import src.helpers.prompting.mf_prompt_constants as constants

def generate_tf_prompts(system_prompt, example_format, num_shots, filepath, tokenizer, use_system_prompt=True, remove_date_prompt=False):
    prompt_map = {}
    with open(filepath) as f:
        data = json.load(f)
        for foundation_obj in data:
            foundation = foundation_obj['label']
            positive_examples = foundation_obj['positive_examples']
            negative_examples = foundation_obj['negative_examples']
            messages = []
            final_system_prompt = system_prompt
            if num_shots > 0:
                final_system_prompt += constants.SYSTEM_PROMPT_EXAMPLE_LEAD_IN
            if use_system_prompt:
                messages.append(
                    {
                        "role": "system",
                        "content": final_system_prompt
                    }
                )
            for i in range(num_shots):
                positive_examples[i]['label'] = foundation
                negative_examples[i]['label'] = foundation
                positive_example = example_format.format(**positive_examples[i])
                negative_example = example_format.format(**negative_examples[i])
                if i == 0 and not use_system_prompt:
                    positive_example = final_system_prompt + positive_example
                messages.append({
                    "role": "user",
                    "content": positive_example
                })
                messages.append({
                    "role": "assistant",
                    "content": "true"
                })
                messages.append({
                    "role": "user",
                    "content": negative_example
                })
                messages.append({
                    "role": "assistant",
                    "content": "false"
                })
            messages.append({
                "role": "user",
                "content": example_format
            })
            foundation_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            if remove_date_prompt:
                foundation_prompt = foundation_prompt.replace("Cutting Knowledge Date: December 2023\nToday Date: 26 Jul 2024\n\n", "")
            prompt_map[foundation] = foundation_prompt
    return prompt_map

def generate_vc_prompt(system_prompt, prompt_format, tokenizer, use_system_prompt=True, remove_date_prompt=False):
    messages = []
    if use_system_prompt:
        messages.append(
            {
                "role": "system" if use_system_prompt else "user",
                "content": system_prompt
            }
        )
        messages.append(
            {
                "role": "user",
                "content": prompt_format
            }
        )
    else:
        messages.append(
            {
                "role": "user",
                "content": system_prompt + prompt_format
            }
        )
    foundation_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    if remove_date_prompt:
        foundation_prompt = foundation_prompt.replace("Cutting Knowledge Date: December 2023\nToday Date: 26 Jul 2024\n\n", "")
    return foundation_prompt


def generate_one_pass_gz_moral_foundation_prompt_format(label_sentences, example_format, num_shots, num_variations, example_dir):
    filepath = os.path.join(example_dir, 'moral_foundation_examples.json')
    foundation_prompt_map = {}
    with open(filepath) as f:
        data = json.load(f)
        for foundation_obj in data:
            foundation = foundation_obj['moral_foundation']
            definition = constants.MORAL_FOUNDATION_DEFINITIONS_MAP[foundation]
            foundation_prompt_map[foundation] = []
            for i in range(num_variations):
                foundation_formatted_prompt = label_sentences[i].format(MORAL_FOUNDATION=foundation, MORAL_FOUNDATION_DEFINITION=definition)
                if num_shots == 0:
                    formatted_prompt = ' '.join([constants.GEN_Z_MF_INTRO_ZERO_SHOT, constants.GEN_Z_MF_PREFIX, foundation_formatted_prompt])
                else:
                    positive_examples = foundation_obj['positive_examples']
                    formatted_examples = []
                    for j in range(num_shots):
                        positive_example_description = foundation_formatted_prompt.format(**positive_examples[j])
                        positive_example = example_format.format(positive_example_description, positive_examples[j]['Tweet'])
                        formatted_examples.append(positive_example)
                    formatted_prompt = ' '.join([constants.GEN_Z_MF_FEW_SHOT_EXAMPLES,' '.join(formatted_examples), constants.GEN_Z_MF_PREFIX, foundation_formatted_prompt])
                foundation_prompt_map[foundation].append(formatted_prompt)
    return foundation_prompt_map

