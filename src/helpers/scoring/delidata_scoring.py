import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import src.helpers.scoring.scoring as scoring
import src.helpers.prompting.delidata_prompt_constants as constants
import sklearn.metrics as sk

def get_scored_groundings(rule_groundings, rule_names, rule_type):
    if type(rule_groundings) == str:
        rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings, rule_names)
    if rule_type == 'mc':
        rule_groundings['rule_one'] = scoring.mc_scoring(rule_groundings['rule_one'], ['message_id'], constants.LEVEL_1_LABEL_TO_INDEX)
        rule_groundings['rule_two'] = scoring.mc_scoring(rule_groundings['rule_two'], ['message_id'], constants.LEVEL_2_LABEL_TO_INDEX)
    else:
        raise Exception('Invalid Rule Type')
    
    # drop duplicates: duplicates happen due to the splitting of the dataframe and duplicate id rows for examples with multiple entities to predict
    rule_groundings['rule_one'].drop_duplicates(['message_id','label'], inplace=True)
    rule_groundings['rule_two'].drop_duplicates(['message_id','label'], inplace=True)

    return rule_groundings

def eval(level_1_preds, level_2_preds, level_1_labels, level_2_labels):
    level_1_f1 = sk.f1_score(level_1_labels, level_1_preds, average='macro')
    level_2_f1 = sk.f1_score(level_2_labels, level_2_preds, average='macro')
    constraint_violations = 0
    for i in range(len(level_1_preds)):
        if (level_1_preds[i] == 0  and level_2_preds[i] != 0) or (level_1_preds[i] != 0 and level_2_preds[i] == 0):
            constraint_violations += 1
        if level_1_preds[i] == 1 and level_2_preds[i] not in [1, 3, 4]:
            constraint_violations += 1
        if level_2_preds == 2 and level_2_preds[i] not in [5, 1, 2]:
            constraint_violations += 1
    print(f'Constraint Violations: {constraint_violations}')
    print(f'Level 1 Macro F1: {level_1_f1}')
    print(f'Level 2 Macro F1: {level_2_f1}')
        
        