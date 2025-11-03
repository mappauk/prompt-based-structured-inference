from datasets import load_dataset
import pandas as pd
import src.helpers.prompting.delidata_prompt_constants as constants
import os

def load_delidata():
    dataset = load_dataset("gkaradzhov/DeliData", token=os.getenv('HF_TOKEN'))
    df = pd.DataFrame(dataset['train'])

    df = df.query("annotation_type != '0'")
    df.loc[:, 'annotation_target'] = df['annotation_target'].str.replace('0','None')
    df['original_text'].fillna("None", inplace=True)
    df['annotation_type'].fillna("None", inplace=True)
    df['annotation_target'].fillna("None", inplace=True)
    df["annotation_type"].replace(constants.LEVEL_1_LABEL_TO_INDEX, inplace=True)
    df["annotation_target"].replace(constants.LEVEL_2_LABEL_TO_INDEX, inplace=True)
    df = df[df['message_type'] == 'MESSAGE']
    return df[['group_id', 'message_id', 'original_text', 'annotation_type', 'annotation_target']]

