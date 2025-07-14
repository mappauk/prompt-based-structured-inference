import src.helpers.scoring.scoring as scoring
import src.helpers.prompting.coref_prompt_constants as constants
import src.helpers.loaders.prompt_data_loader as prompt_data_loader
import pandas as pd
import src.helpers.loaders.ontonotes_dataset_loader as ontonotes_dataset_loader
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader
from typing import Dict
import pandas as pd
import gurobipy as gp
import torch
from src.inference.gurobi_inference_model import GurobiInferenceModel
import sklearn.metrics as sk
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
import math
from src.rules.rule_template import RuleTemplate
from src.rules.rule_type import RuleType
import src.analysis.analysis_helper as analysis_helper
import json

def answer_conversion(answer):
    return 1 if answer == 'Yes' else 0

def get_scored_groundings(rule_groundings_path, rule_names, rule_type):
    rule_groundings = prompt_data_loader.load_rule_groundings(rule_groundings_path, rule_names)
    if rule_type == 'tf':
        rule_groundings['rule_one'] = scoring.tf_scoring(rule_groundings['rule_one'], ['doc_id', 'entity1_id', 'entity2_id'])
    elif rule_type == 'mc':
        rule_groundings['rule_one'] = scoring.mc_scoring(rule_groundings['rule_one'], ['doc_id', 'entity1_id', 'entity2_id'], constants.COREF_LABEL_TO_CHOICE_INDEX)
    elif rule_type == 'gc':
        rule_groundings['rule_one'] = scoring.gc_scoring(rule_groundings['rule_one'], ['doc_id', 'entity1_id', 'entity2_id'])
    elif rule_type == 'gs':
        rule_groundings['rule_one'] = scoring.gs_scoring(rule_groundings['rule_one'])
    elif rule_type == 'vc':
        rule_groundings['rule_one'] = scoring.vc_scoring(rule_groundings['rule_one'], ['doc_id', 'entity1_id', 'entity2_id'])
    else:
        raise Exception('Invalid Rule Type')
    return rule_groundings

def get_rule_info():
    rule_one = RuleTemplate(
        'rule_one',
        ['doc_id', 'entity1_id', 'entity1', 'entity2_id', 'entity2', 'sent1', 'sent2'],
        ['coreferent', 'distinct'],
        'CF_{doc_id}_{entity1_id}_{entity2_id}_{label}',
        'RuleOne_{doc_id}_{entity1_id}_{entity2_id}_{label}',
        RuleType.BINARY,
    )
    return {
        rule_one.name: rule_one
    }


def get_constraints():
    # get entity groups for entity constraint
    def constr_one(rule_groundings: Dict[str, pd.DataFrame], head_dict: Dict[str, gp.Var], m: gp.Model) -> None:
        coref_groupings = rule_groundings['rule_one'].groupby(['doc_id'])
        for group_name, group in coref_groupings:
            main_row_index = 0
            for i, main_row in group.iterrows():
                doc_id = main_row['doc_id']
                sec_row_index = 0
                for j, sec_row in group.iterrows():
                    if sec_row_index <= main_row_index:
                        sec_row_index += 1
                        continue
                    tr_ent_one = None
                    tr_ent_two = None
                    if main_row['entity1_id'] == sec_row['entity1_id']:
                        tr_ent_one = main_row['entity2_id']
                        tr_ent_two = sec_row['entity2_id']
                    elif main_row['entity1_id'] == sec_row['entity2_id']:
                        tr_ent_one = main_row['entity2_id']
                        tr_ent_two = sec_row['entity1_id']
                    elif main_row['entity2_id'] == sec_row['entity1_id']:
                        tr_ent_one = main_row['entity1_id']
                        tr_ent_two = sec_row['entity2_id']
                    elif main_row['entity2_id'] == sec_row['entity2_id']:
                        tr_ent_one = main_row['entity1_id']
                        tr_ent_two = sec_row['entity1_id']     
                    tr_var_one = 'CF_{0}_{1}_{2}'.format(doc_id, tr_ent_one, tr_ent_two)
                    tr_var_two = 'CF_{0}_{1}_{2}'.format(doc_id, tr_ent_two, tr_ent_one)
                    if tr_ent_one != None and tr_var_one in head_dict:
                        m.addConstr(head_dict[main_row['HeadVariable']] * head_dict[sec_row['HeadVariable']] <= head_dict[tr_var_one])
                    elif tr_ent_one != None and tr_var_two in head_dict:
                        m.addConstr(head_dict[main_row['HeadVariable']] * head_dict[sec_row['HeadVariable']] <= head_dict[tr_var_two])
                    sec_row_index += 1
                main_row_index += 1
    custom_rule_constraints = [constr_one]
    return custom_rule_constraints

def get_training_groundings(data_input_paths, grounding_paths, rule_type, batch_size=32, batch_val_groundings=False, val_batch_size=0, document_batching=False, include_features=False):
    data = None
    final_groundings = {}
    for split, path in grounding_paths.items():
        data_path = data_input_paths[split]

        if 'conll' in data_path:
            data = ontonotes_dataset_loader.preprocess_ontonotes_coref(data_path)
        else:
            data = genia_dataset_loader.preprocess_genia_coref(data_path)
        split_groundings = get_scored_groundings(path, ['rule_one'], rule_type)
        split_groundings['rule_one'] = split_groundings['rule_one'][~split_groundings['rule_one']['HeadVariable'].str.endswith('distinct')]
        split_groundings['rule_one']['HeadVariable'] = split_groundings['rule_one']['HeadVariable'].map(lambda h: h[:-11])
        split_groundings['rule_one']['RuleVariable'] = split_groundings['rule_one']['RuleVariable'].map(lambda h: h[:-11])
        split_groundings['rule_one'] = split_groundings['rule_one'].merge(data, on=['doc_id', 'entity1_id', 'entity2_id'], how='inner')
        if include_features:
            split_groundings['rule_one'].rename(
                columns={
                 "entity1_y": "entity1",
                 "entity2_y": "entity2",
                 "sent1_y": "sent1",
                 "sent2_y": "sent2",
                }, 
                inplace=True)
            split_groundings['rule_one'] = split_groundings['rule_one'][['doc_id', 'entity1_id', 'entity2_id', 'entity1', 'entity2', 'sent1', 'sent2', 'Score', 'RuleVariable', 'HeadVariable', 'label', 'answer']]
        else:
            split_groundings['rule_one'] = split_groundings['rule_one'][['doc_id', 'entity1_id', 'entity2_id', 'Score', 'RuleVariable', 'HeadVariable', 'label', 'answer']]
        
        split_groundings['rule_one'].rename(columns={'answer': 'GroundTruth'}, inplace=True)
        split_groundings['rule_one']['GroundTruth'] = split_groundings['rule_one']['GroundTruth'].apply(answer_conversion)
        split_count = split_groundings['rule_one'].shape[0]
        if split == 'train':
            batched_train_groundings = []
            if document_batching:
                doc_groupings = split_groundings['rule_one'].groupby(['doc_id'])
                for group_name, group in doc_groupings:
                    batched_train_groundings.append({
                        'rule_one': group
                    })
            else:
                num_batches = math.ceil(split_count/batch_size)
                for i in range(num_batches):
                    batched_train_groundings.append({})
                for i in range(num_batches):
                    batch_start = i*batch_size
                    batch_end = min((i + 1)*batch_size, split_count)
                    batched_train_groundings[i]['rule_one'] = split_groundings['rule_one'].iloc[batch_start:batch_end]
            final_groundings['train'] = batched_train_groundings
        elif split == 'val' and batch_val_groundings:
            batched_val_groundings = []
            num_val_batches = math.ceil(split_count/val_batch_size)
            for i in range(num_val_batches):
                batched_val_groundings.append({})
            for i in range(num_val_batches):
                batch_start = i*val_batch_size
                batch_end = min((i + 1)*val_batch_size, split_count)
                batched_val_groundings[i]['rule_one'] = split_groundings['rule_one'].iloc[batch_start:batch_end]
            final_groundings['val'] = batched_train_groundings
        else:
            final_groundings[split] = split_groundings
    return final_groundings

def model_eval(rules, constraints, inputs, outputs=None, softmax_enabled=True, inference_score=True):
    with torch.no_grad():
        # rule f1 before inference
        curr_grounding = inputs['rule_one'].copy()
        if outputs != None and not softmax_enabled:
            curr_grounding['Score'] = list(outputs['rule_one'].detach().numpy())
        elif outputs != None:
            #print(outputs['rule_one'])
            outputs['rule_one'] = torch.nn.functional.sigmoid(torch.squeeze(outputs['rule_one'], 1))
            #print(outputs['rule_one'])
            curr_grounding['Score'] = list(outputs['rule_one'].detach().numpy())
        ground_truth = curr_grounding['GroundTruth'].tolist()
        preds = np.round(curr_grounding['Score'].tolist()).astype(int)
        pre_inf_macro_f1 = sk.f1_score(ground_truth, preds, average='macro')
        #accuracy = sk.accuracy_score(ground_truth, preds)
        print(f'Pre Inference Results')
        print(f'macro f1: {pre_inf_macro_f1}')
        if not inference_score:
            return pre_inf_macro_f1
        else:
            # inference
            inference_model = GurobiInferenceModel(rules, {'rule_one': curr_grounding}, constraints, num_solutions=1)
            solution = inference_model.inference()[0]
            preds = []
            for index, row in inputs['rule_one'].iterrows():
                if solution[row['HeadVariable']] == 1:
                    preds.append(1)
                else:
                    preds.append(0)
            # f1 after inference
            print(f'Post Inference Results')
            post_inf_macro_f1 = sk.f1_score(inputs['rule_one']['GroundTruth'].tolist(), preds, average='macro')
            print(f'macro f1: {post_inf_macro_f1}')
            return post_inf_macro_f1