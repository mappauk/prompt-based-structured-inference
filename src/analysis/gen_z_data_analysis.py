import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.analysis.analysis_helper as analysis_helper
from datasets import load_dataset
import pandas as pd
import sys
import sklearn.metrics as sk

def main():
    dataset = load_dataset('SetFit/sst5')
    ids = []
    text = []
    labels = []
    for i in range(len(dataset['test'])):
        ids.append(i)
        text.append(dataset['test'][i]['text'])
        labels.append(dataset['test'][i]['label_text'])
    
    data = pd.DataFrame(
        {
            'Id': ids,
            'Text': text,
            'label': labels
        }
    )
    predictions = analysis_helper.load_results(r'C:\Users\mpauk\Downloads\gen_z_output.json')
    true_labels = []
    predicted_labels = []
    for index, row in data.iterrows():
        true_labels.append(row['label'])
        predicted_labels.append(predictions[str(row['Id'])]['Label'])
    print(len(true_labels))
    print(len(predicted_labels))
    print('Macro F1:')
    print(sk.f1_score(true_labels, predicted_labels, labels=['negative', 'very negative', 'neutral', 'positive', 'very positive'], average='macro'))
    print('Micro F1:')
    print(sk.f1_score(true_labels, predicted_labels, labels=['negative', 'very negative', 'neutral', 'positive', 'very positive'], average='micro'))
    
if __name__ == "__main__":
    main()