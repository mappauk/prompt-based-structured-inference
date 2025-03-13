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

def generate_mc_prompt(system_prompt, example_format, label_to_choice_map, num_shots, filepath, tokenizer, foundations_per_shot, use_system_prompt=True, remove_date_prompt=False, example_count=5):
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
    if num_shots > 0:
        with open(filepath) as f:
            data = json.load(f)
            for i in range(example_count):
                foundation_counter = 0
                for foundation_obj in data:
                    if i*len(data) + foundation_counter >= num_shots*foundations_per_shot:
                        break
                    positive_examples = foundation_obj['positive_examples']
                    positive_example = example_format.format(**positive_examples[i])
                    if i == 0 and not use_system_prompt:
                        positive_example = final_system_prompt + positive_example
                    messages.append({
                        "role": "user",
                        "content": positive_example
                    })
                    messages.append({
                        "role": "assistant",
                        "content": label_to_choice_map[foundation_obj['label']]
                    })
                    foundation_counter += 1
    messages.append({
        "role": "user",
        "content": example_format
    })
    foundation_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    if remove_date_prompt:
        foundation_prompt = foundation_prompt.replace("Cutting Knowledge Date: December 2023\nToday Date: 26 Jul 2024\n\n", "")
    return foundation_prompt

def generate_gc_prompt(system_prompt, label_sentences, example_format, num_shots, num_variations, filepath, tokenizer, foundations_per_shot, use_system_prompt=True, remove_date_prompt=False, example_count=5):
    prompts = []
    for i in range(num_variations):
        messages = []
        example_format_with_description = example_format.format(label_sentences[i])
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
        if num_shots > 0:
            with open(filepath) as f:
                data = json.load(f)
                for i in range(example_count):
                    foundation_counter = 0
                    for foundation_obj in data:
                        if i*len(data) + foundation_counter >= num_shots*foundations_per_shot:
                            break
                        positive_examples = foundation_obj['positive_examples']
                        positive_examples[i]['label'] = foundation_obj['label']
                        positive_example = example_format_with_description.format(**positive_examples[i])
                        if i == 0 and not use_system_prompt:
                            positive_example = final_system_prompt + positive_example
                        messages.append({
                            "role": "user",
                            "content": positive_example
                        })
                        messages.append({
                            "role": "assistant",
                            "content": positive_examples[i]['Tweet']
                        })
                        foundation_counter += 1
        messages.append({
            "role": "user",
            "content": example_format_with_description
        })
        foundation_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        if remove_date_prompt:
            foundation_prompt = foundation_prompt.replace("Cutting Knowledge Date: December 2023\nToday Date: 26 Jul 2024\n\n", "")
        prompts.append(foundation_prompt)
    return prompts

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




