import src.helpers.prompting.delidata_prompt_constants as constants
import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np


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
                    messages.append({
                        "role": "user",
                        "content": positive_example
                    })
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

def delidata_prompting_cosine_similarity(tokenizer, num_shots, data, level_1_system_prompt, level_2_system_prompt, features, level_1_example_format, level_2_example_format, level_1_prompt, level_2_prompt):
    level_1_system_prompt = level_1_system_prompt + constants.SYSTEM_PROMPT_EXAMPLE_LEAD_IN
    level_2_system_prompt = level_2_system_prompt + constants.SYSTEM_PROMPT_EXAMPLE_LEAD_IN
    embeddings = []
    model = SentenceTransformer('sentence-transformers/gtr-t5-xl')
    utterances = []

    data_subset = data[features].drop_duplicates().reset_index(inplace=False)
    # get embeddings for all examples
    for item, row in data_subset.iterrows():
        utterances.append(row['original_text'])
    embeddings = model.encode(utterances)


    level_one_map = {}
    level_two_map = {}
    for i in range(len(utterances)):
        message_id = data_subset.loc[i, 'message_id']
        similarities = cosine_similarity([embeddings[i]], embeddings)[0]
        most_similar_indicies = np.argsort(similarities)[::-1]
        level_1_messages = [
            {
                "role": "system",
                "content": level_1_system_prompt
            }
        ]
        level_2_messages = [
            {
                "role": "system",
                "content": level_2_system_prompt
            }
        ]
        for i in range(len(most_similar_indicies)):
            if len(level_2_messages)/2 >= num_shots:
                break
            row = data_subset.iloc[most_similar_indicies[i], :]
            if row.isnull().any() or row['message_id'] == message_id:
                continue
            level_1_label = row['annotation_type']
            level_2_label = row['annotation_target']
            level_1_example = level_1_example_format.format(**row.to_dict())
            level_2_example = level_2_example_format.format(**row.to_dict())
            level_1_messages.append({
                "role": "user",
                "content": level_1_example
            })
            level_2_messages.append({
                "role": "user",
                "content": level_2_example
            })
            level_1_messages.append({
                "role": "assistant",
                "content": constants.LEVEL_1_TO_CHOICE_MAP[level_1_label]
            })
            level_2_messages.append({
                "role": "assistant",
                "content": constants.LEVEL_2_TO_CHOICE_MAP[level_2_label]
            })
        level_1_messages.append({
            "role": "user",
            "content": level_1_prompt
        })
        level_2_messages.append({
            "role": "user",
            "content": level_2_prompt
        })
        level_one_prompt = tokenizer.apply_chat_template(level_1_messages, tokenize=False, add_generation_prompt=True)
        level_two_prompt = tokenizer.apply_chat_template(level_2_messages, tokenize=False, add_generation_prompt=True)
        level_one_map[message_id] = level_one_prompt
        level_two_map[message_id] = level_two_prompt
    return level_one_map, level_two_map