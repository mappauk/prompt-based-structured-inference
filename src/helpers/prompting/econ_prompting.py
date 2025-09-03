import os
import json
import src.helpers.prompting.econ_prompt_constants as constants


def generate_tf_prompts(system_prompt, example_format, num_shots, filepath, tokenizer, task_name):
    prompt_map = {}
    final_system_prompt = system_prompt
    if num_shots > 0:
        final_system_prompt += constants.SYSTEM_PROMPT_EXAMPLE_LEAD_IN
    with open(filepath) as f:
        data = json.load(f)
        task = data[task_name]
        for label_examples in task:
            messages = []
            messages.append(
                {
                    "role": "system",
                    "content": final_system_prompt
                }
            )
            label = label_examples['label']
            positive_examples = label_examples['positive_examples']
            negative_examples = label_examples['negative_examples']
            for i in range(num_shots):
                positive_examples[i]['label'] = label
                negative_examples[i]['label'] = label
                positive_example = example_format.format(**positive_examples[i])
                negative_example = example_format.format(**negative_examples[i])
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
            tf_prompt_template = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            prompt_map[label] = tf_prompt_template
    return prompt_map