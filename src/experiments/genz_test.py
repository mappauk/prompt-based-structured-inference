import sys
import pandas as pd
from src.rules.llm_gz_rule import LLMGZRule
import src.helpers.loaders.model_loader as model_loader
import src.analysis.analysis_helper as analysis_helper
from datasets import load_dataset

from src.rules.rule_type import RuleType

def main():
    # hyperparamaters
    device_type = 'cuda'
    num_variations = 6
    prompt_batch_size = 8
    output_path = sys.argv[1]
    # load data
    dataset = load_dataset('SetFit/sst5')
    ids = []
    text = []
    labels = []
    domain = []
    for i in range(len(dataset['test'])):
        ids.append(i)
        text.append(dataset['test'][i]['text'])
        labels.append(dataset['test'][i]['label_text'])
        domain.append('movie review')

    data = pd.DataFrame(
        {
            'Id': ids,
            'Text': text,
            'label': labels
        }
    )
    possible_labels = ['negative', 'very negative', 'neutral', 'positive', 'very positive']

    # generate moral foundation prompt format strings
    sentiment_prompts = generate_gz_prompt_map(num_variations, possible_labels)
    generation_format = ' ### Movie Review: {Text}'

    # load model
    model, tokenizer = model_loader.load_gpt_j_model(device_type)
    # define rules
    rule_one = LLMGZRule(
        'rule_one',
        ['Id', 'Text'],
        possible_labels,
        'SA_{Id}_{label}',
        'RuleOne_{Id}_{label}',
        RuleType.MULTI_CLASS,
        prompt_batch_size,
        model,
        tokenizer,
        device_type,
        sentiment_prompts,
        generation_format,
        num_variations
    )

    sentiment_predictions = rule_one.get_rule_groundings(data)
  
    # save results
    results = {}
    for group_name, group in sentiment_predictions.groupby(['Id']):
        max_row = group.iloc[group['Score'].argmax()]
        results[str(max_row['Id'])] = {
            'Text': max_row['Text'],
            'Label': max_row['label']
        }
    analysis_helper.write_json_file(output_path, results)

def generate_gz_prompt_map(num_variations, labels):
    label_sentences = [
        'This movie review leans {0}',
        'This review skews {0}.',
        'The tone of this movie review is {0}.',
        'This critique reflects a {0} perspective.',
        'The review takes a {0} stance.',
        'This movie critique is clearly {0}.',
        'The sentiment in this review is {0}.',
        'This review expresses a {0} opinion.',
        'This critique leans toward a {0} view.',
        'The perspective in this movie review is {0}.',
        'This review conveys a {0} sentiment.'
    ]
    prompt_map = {}
    for label in labels:
        prompt_map[label] = []
        for i in range(num_variations):
            formatted_prompt = ' '.join(['Generate text based on the following description.', '### Generation description:', label_sentences[i].format(label)])
            prompt_map[label].append(formatted_prompt)
    return prompt_map

if __name__ == "__main__":
    main()
