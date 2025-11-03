import src.helpers.prompting.delidata_prompt_constants as constants
import json

def delidata_prompting(tokenizer, system_prompt, example_format, num_shots, example_filepath, label_to_choice_map, example_types_per_shot=1):
    messages = []
    final_system_prompt = system_prompt
    if num_shots > 0:
        final_system_prompt += constants.SYSTEM_PROMPT_EXAMPLE_LEAD_IN
    messages.append(
        {
            "role": "system",
            "content": final_system_prompt
        }
    )
    if num_shots > 0:
        with open(example_filepath) as f:
            data = json.load(f)
            for i in range(num_shots):
                counter = 0
                for label_data in data:
                    if i*len(data) + counter >= num_shots*example_types_per_shot:
                        break
                    positive_examples = label_data['positive_examples']
                    positive_example = example_format.format(**positive_examples[i])
                    #print(positive_example)
                    messages.append({
                        "role": "user",
                        "content": positive_example
                    })
                    #print(label_to_choice_map[label_data['label']])
                    messages.append({
                        "role": "assistant",
                        "content": label_to_choice_map[label_data['label']]
                    })
                    counter += 1
    messages.append({
        "role": "user",
        "content": example_format
    })
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)