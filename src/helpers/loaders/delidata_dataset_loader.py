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

    conversations = df.groupby(['group_id'])
    message_ids = []
    previous_messages = []
    previous_annotation_types = []
    previous_annotation_targets = []
    previous_annotation_gold_types = []
    previous_annotation_gold_targets = []
    for group_name, group in conversations:
        previous_message = None
        previous_level_1_gold_label = None
        previous_level_2_gold_label = None
        for item, row in group.iterrows():
            for label_index in range(len(constants.LEVEL_2_LABELS)):
                message_ids.append(row['message_id'])
                previous_messages.append(previous_message)
                previous_annotation_types.append(constants.LEVEL_1_LABELS[min(label_index, len(constants.LEVEL_1_LABELS) - 1)])
                previous_annotation_targets.append(constants.LEVEL_2_LABELS[label_index])
                previous_annotation_gold_types.append(previous_level_1_gold_label)
                previous_annotation_gold_targets.append(previous_level_2_gold_label)
            previous_message = row['original_text']
            previous_level_1_gold_label = row['annotation_type']
            previous_level_2_gold_label = row['annotation_target']
    previous_df = pd.DataFrame({
        'message_id': message_ids,
        'previous_original_text': previous_messages,
        'previous_annotation_type': previous_annotation_types,
        "previous_annotation_target": previous_annotation_targets,
        'previous_annotation_gold_type': previous_annotation_gold_types,
        'previous_annotation_gold_target': previous_annotation_gold_targets
    })

    new_df = pd.merge(df, previous_df, how='left', on='message_id')
    new_df.reset_index(inplace=True)
    return new_df[['group_id', 'message_id', 'original_text', 'annotation_type', 'annotation_target', 'previous_original_text', 'previous_annotation_type', 'previous_annotation_target', 'previous_annotation_gold_type', 'previous_annotation_gold_target']]

