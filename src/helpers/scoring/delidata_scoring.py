import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import src.helpers.scoring.scoring as scoring
import src.helpers.prompting.delidata_prompt_constants as constants
import sklearn.metrics as sk
from sklearn.metrics import precision_recall_curve, auc
from sklearn.preprocessing import label_binarize
import numpy as np
import pandas as pd

def get_scored_groundings(rule_groundings, rule_names, rule_type):
    if type(rule_groundings) == str:
        rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings, rule_names)

    if rule_type == 'mc':
        rule_groundings['rule_one'] = scoring.mc_scoring(rule_groundings['rule_one'], ['message_id'], constants.LEVEL_1_LABEL_TO_INDEX)
        rule_groundings['rule_two'] = scoring.mc_scoring(rule_groundings['rule_two'], ['message_id'], constants.LEVEL_2_LABEL_TO_INDEX)
        rule_groundings['rule_three'] = scoring.mc_scoring(rule_groundings['rule_three'], ['message_id', 'previous_annotation_type'], constants.LEVEL_1_LABEL_TO_INDEX)
        rule_groundings['rule_four'] = scoring.mc_scoring(rule_groundings['rule_four'], ['message_id', 'previous_annotation_target'], constants.LEVEL_2_LABEL_TO_INDEX)
    else:
        raise Exception('Invalid Rule Type')
    
    # drop duplicates: duplicates happen due to the splitting of the dataframe and duplicate id rows for examples with multiple entities to predict
    rule_groundings['rule_one'].drop_duplicates(['message_id','label'], inplace=True)
    rule_groundings['rule_two'].drop_duplicates(['message_id','label'], inplace=True)
    rule_groundings['rule_three'].drop_duplicates(['message_id', 'previous_annotation_type', 'label'], inplace=True)
    rule_groundings['rule_four'].drop_duplicates(['message_id', 'previous_annotation_target', 'label'], inplace=True)
    return rule_groundings

def eval(level_1_preds, level_2_preds, level_1_labels, level_2_labels,):
    level_1_f1 = sk.f1_score(level_1_labels, level_1_preds, average='macro')
    level_2_f1 = sk.f1_score(level_2_labels, level_2_preds, average='macro')

    pred_constraint_violations = 0
    for i in range(len(level_1_preds)):
        if (level_1_preds[i] == 0  and level_2_preds[i] != 0) or (level_1_preds[i] != 0 and level_2_preds[i] == 0):
            pred_constraint_violations += 1
        if level_1_preds[i] == 1 and level_2_preds[i] not in [1, 2, 3, 4]:
            pred_constraint_violations += 1
        if level_1_preds[i] == 2 and level_2_preds[i] not in [5, 1, 2]:
            pred_constraint_violations += 1
    
    gold_constraint_violations = 0
    for i in range(len(level_1_preds)):
        if (level_1_labels[i] == 0  and level_2_labels[i] != 0) or (level_1_labels[i] != 0 and level_2_labels[i] == 0):
            gold_constraint_violations += 1
        if level_1_labels[i] == 1 and level_2_labels[i] not in [1, 2, 3, 4]:
            gold_constraint_violations += 1
        if level_1_labels[i] == 2 and level_2_labels[i] not in [5, 1, 2]:
            gold_constraint_violations += 1
    
    level_1_classes = list(constants.LEVEL_1_LABEL_TO_INDEX.values())
    level_2_classes = list(constants.LEVEL_2_LABEL_TO_INDEX.values())
    level_1_y_bin = label_binarize(level_1_labels, classes=level_1_classes)
    level_1_y_pred_bin = label_binarize(level_1_preds, classes=level_1_classes)
    # PR-AUC for each class
    level_1_pr_aucs = []
    for i in range(len(level_1_classes)):
        precision, recall, _ = precision_recall_curve(level_1_y_bin[:, i], level_1_y_pred_bin[:, i])
        level_1_pr_aucs.append(auc(recall, precision))

    level_2_y_bin = label_binarize(level_2_labels, classes=level_2_classes)
    level_2_y_pred_bin = label_binarize(level_2_preds, classes=level_2_classes)
    # PR-AUC for each class
    level_2_pr_aucs = []
    for i in range(len(level_2_classes)):
        precision, recall, _ = precision_recall_curve(level_2_y_bin[:, i], level_2_y_pred_bin[:, i])
        level_2_pr_aucs.append(auc(recall, precision))
    avg_level_1_pr_auc = np.mean(level_1_pr_aucs)
    avg_level_2_pr_auc = np.mean(level_2_pr_aucs)
    print(f'Constraint Violations: {pred_constraint_violations}')
    print(f'Gold Constraint Violations: {gold_constraint_violations}')
    print(f'Level 1 Macro F1: {level_1_f1}')
    print(f'Level 1 Avg PR_AUC: {avg_level_1_pr_auc}')
    print(level_1_pr_aucs)
    print(f'Level 2 Macro F1: {level_2_f1}')
    print(f'Level 2 Avg PR_AUC: {avg_level_2_pr_auc}')
    print(level_2_pr_aucs)
        
        