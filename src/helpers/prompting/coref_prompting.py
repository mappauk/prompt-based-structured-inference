import json
import src.helpers.prompting.coref_prompt_constants as constants

def generate_tf_prompts(num_shots, filepath, tokenizer):
    with open(filepath) as f:
        data = json.load(f)
        coref_messages = []
        non_coref_messages = []
        final_system_prompt = constants.COREF_TF_SYSTEM_PROMPT
        if num_shots > 0:
            final_system_prompt += constants.SYSTEM_PROMPT_EXAMPLE_LEAD_IN

        coref_messages.append(
            {
                "role": "system",
                "content": final_system_prompt
            }
        )

        positive_examples = data['positive_examples']
        negative_examples = data['negative_examples']

        for i in range(num_shots):
            positive_examples[i]['label'] = 'coreferent'
            negative_examples[i]['label'] = 'coreferent'
            positive_coref_example = constants.COREF_TF_PROMPT_EXAMPLE.format(**positive_examples[i])
            negative_coref_example = constants.COREF_TF_PROMPT_EXAMPLE.format(**negative_examples[i])
            coref_messages.append({
                "role": "user",
                "content": positive_coref_example             
            })
            coref_messages.append({
                "role": "assistant",
                "content": "true"
            })
            coref_messages.append({
                "role": "user",
                "content": negative_coref_example             
            })
            coref_messages.append({
                "role": "assistant",
                "content": "false"
            })

            positive_examples[i]['label'] = 'distinct'
            negative_examples[i]['label'] = 'distinct'
            positive_distinct_example = constants.COREF_TF_PROMPT_EXAMPLE.format(**negative_examples[i])
            negative_distinct_example = constants.COREF_TF_PROMPT_EXAMPLE.format(**positive_examples[i])
            non_coref_messages.append({
                "role": "user",
                "content": positive_distinct_example             
            })
            non_coref_messages.append({
                "role": "assistant",
                "content": "true"
            })
            non_coref_messages.append({
                "role": "user",
                "content": negative_distinct_example             
            })
            non_coref_messages.append({
                "role": "assistant",
                "content": "false"
            })

        coref_messages.append({
            "role": "user",
            "content": constants.COREF_TF_PROMPT_EXAMPLE
        })

        non_coref_messages.append({
            "role": "user",
            "content": constants.COREF_TF_PROMPT_EXAMPLE          
        })
    prompt_map = {
        'coreferent': tokenizer.apply_chat_template(coref_messages, tokenize=False, add_generation_prompt=True),
        'distinct': tokenizer.apply_chat_template(non_coref_messages, tokenize=False, add_generation_prompt=True)
    }
    return prompt_map

def generate_mc_prompts(num_shots, filepath, tokenizer, both_per_shot=False):
    with open(filepath) as f:
        data = json.load(f)
        messages = []
        final_system_prompt = constants.COREF_MC_SYSTEM_PROMPT
        if num_shots > 0:
            final_system_prompt += constants.SYSTEM_PROMPT_EXAMPLE_LEAD_IN

        messages.append(
            {
                "role": "system",
                "content": final_system_prompt
            }
        )

        positive_examples = data['positive_examples']
        negative_examples = data['negative_examples']
        for i in range(num_shots):
            positive_coref_example = constants.COREF_MC_PROMPT_EXAMPLE.format(**positive_examples[i])
            negative_coref_example = constants.COREF_MC_PROMPT_EXAMPLE.format(**negative_examples[i])
            if both_per_shot:
                messages.append({
                    "role": "user",
                    "content": positive_coref_example             
                })
                messages.append({
                    "role": "assistant",
                    "content": "A"
                })
                messages.append({
                    "role": "user",
                    "content": negative_coref_example             
                })
                messages.append({
                    "role": "assistant",
                    "content": "B"
                })
            elif i % 2 == 0:
                messages.append({
                    "role": "user",
                    "content": positive_coref_example             
                })
                messages.append({
                    "role": "assistant",
                    "content": "A"
                })
            else:
                messages.append({
                    "role": "user",
                    "content": negative_coref_example             
                })
                messages.append({
                    "role": "assistant",
                    "content": "B"
                })
        messages.append({
            "role": "user",
            "content": constants.COREF_MC_PROMPT_EXAMPLE             
        })
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

def generate_gs_prompts(num_shots, filepath, tokenizer, both_per_shot=False):
    with open(filepath) as f:
        data = json.load(f)
        messages = []
        final_system_prompt = constants.COREF_GS_SYSTEM_PROMPT
        if num_shots > 0:
            final_system_prompt += constants.SYSTEM_PROMPT_EXAMPLE_LEAD_IN

        messages.append(
            {
                "role": "system",
                "content": final_system_prompt
            }
        )

        positive_examples = data['positive_examples']
        negative_examples = data['negative_examples']
        for i in range(num_shots):
            positive_coref_example = constants.COREF_GS_PROMPT_EXAMPLE.format(**positive_examples[i])
            negative_coref_example = constants.COREF_GS_PROMPT_EXAMPLE.format(**negative_examples[i])
            if both_per_shot:
                messages.append({
                    "role": "user",
                    "content": positive_coref_example             
                })
                messages.append({
                    "role": "assistant",
                    "content": "coreferent"
                })
                messages.append({
                    "role": "user",
                    "content": negative_coref_example             
                })
                messages.append({
                    "role": "assistant",
                    "content": "distinct"
                })
            elif i % 2 == 0:
                messages.append({
                    "role": "user",
                    "content": positive_coref_example             
                })
                messages.append({
                    "role": "assistant",
                    "content": "coreferent"
                })
            else:
                messages.append({
                    "role": "user",
                    "content": negative_coref_example             
                })
                messages.append({
                    "role": "assistant",
                    "content": "distinct"
                })
        messages.append({
            "role": "user",
            "content": constants.COREF_GS_PROMPT_EXAMPLE             
        })
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

def generate_vc_prompt(tokenizer):
    messages = []
    messages.append(
        {
            "role": "system",
            "content": constants.COREF_VC_SYSTEM_PROMPT
        }
    )
    messages.append({
        "role": "user",
        "content": constants.COREF_VC_EXAMPLE_PROMPT             
    })
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

def generate_gc_prompt(num_shots, num_variations, filepath, tokenizer, both_per_shot=False):
    with open(filepath) as f:
        data = json.load(f)
        prompts = []
        for i in range(num_variations):
                messages = []
                final_system_prompt = constants.COREF_GC_SYSTEM_PROMPT
                if num_shots > 0:
                    final_system_prompt += constants.SYSTEM_PROMPT_EXAMPLE_LEAD_IN

                messages.append(
                    {
                        "role": "system",
                        "content": final_system_prompt
                    }
                )
                positive_examples = data['positive_examples']
                negative_examples = data['negative_examples']
                for j in range(num_shots):
                    positive_examples[j]['label'] = 'coreferent'
                    negative_examples[j]['label'] = 'distinct'
                    positive_coref_example = constants.COREF_GC_EXAMPLE_FORMAT.format(constants.GEN_Z_COREF_LABEL_SENTENCES[i]).format(**positive_examples[j])
                    negative_coref_example = constants.COREF_GC_EXAMPLE_FORMAT.format(constants.GEN_Z_COREF_LABEL_SENTENCES[i]).format(**negative_examples[j])
                    if both_per_shot:
                        messages.append({
                            "role": "user",
                            "content": positive_coref_example             
                        })
                        messages.append({
                            "role": "assistant",
                            "content": constants.COREF_GENERATION_FORMAT.format(**positive_examples[j])
                        })
                        messages.append({
                            "role": "user",
                            "content": negative_coref_example             
                        })
                        messages.append({
                            "role": "assistant",
                            "content": constants.COREF_GENERATION_FORMAT.format(**negative_examples[j])
                        })
                    elif j % 2 == 0:
                        messages.append({
                            "role": "user",
                            "content": positive_coref_example             
                        })
                        messages.append({
                            "role": "assistant",
                            "content": constants.COREF_GENERATION_FORMAT.format(**positive_examples[j])
                        })
                    else:
                        messages.append({
                            "role": "user",
                            "content": negative_coref_example             
                        })
                        messages.append({
                            "role": "assistant",
                            "content": constants.COREF_GENERATION_FORMAT.format(**negative_examples[j])
                        })

                messages.append({
                    "role": "user",
                    "content": constants.COREF_GC_EXAMPLE_FORMAT.format(constants.GEN_Z_COREF_LABEL_SENTENCES[i])          
                })
                prompts.append(
                    tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                )

    return prompts