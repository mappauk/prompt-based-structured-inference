import torch
from scipy.special import softmax
import numpy as np
import re

# tf scoring methods

def tf_scoring(data, groupby):
    return tf_one_vs_rest_normalized(data, groupby)
    #return tf_softmax_across_labels(data, groupby)
    #return tf_one_vs_rest(data)

def tf_softmax_across_labels(data, groupby):
    data['Score'] = data['Score'].apply(lambda score: score[0])
    data['Score'] = data.groupby(groupby)['Score'].transform(softmax)
    return data

def tf_one_vs_rest(data):
    data['Score'] = data['Score'].apply(lambda score: softmax(score[0:2])[0])
    return data

def tf_one_vs_rest_normalized(data, groupby):
    data['Score'] = data['Score'].apply(lambda score: softmax(score[0:2])[0])
    data['Score'] = data.groupby(groupby)['Score'].transform(lambda score: score/score.sum())
    return data

# mc scoring methods

def mc_scoring(data, groupby, choice_map):
    return mc_logit_softmax(data, groupby, choice_map)

def mc_logit_softmax(data, groupby, choice_map):
    data['Score'] = data.apply(lambda x:  x['Score'][choice_map[x['label']]], axis=1)
    data['Score'] = data.groupby(groupby)['Score'].transform(softmax)
    return data

# gc scoring methods

def gc_scoring(data, groupby):
    return gc_average_logit_sequence_softmax(data, groupby)

def gc_sum_logit_softmax(data, groupby):
    data['Score'] = data['Score'].apply(lambda score: np.sum(score['logits']))
    data['Score'] = data.groupby(groupby)['Score'].transform(softmax)
    return data

def gc_average_logit_softmax(data, groupby):
    data['Score'] = data['Score'].apply(lambda score: np.mean(score['logits']))
    data['Score'] = data.groupby(groupby)['Score'].transform(softmax)
    return data

def gc_average_logit_sequence_softmax(data, groupby):
    data['Score'] = data['Score'].apply(lambda score: np.sum(score['logits'], axis=1))
    data['Score'] = data['Score'].apply(lambda score: np.mean(score))
    data['Score'] = data.groupby(groupby)['Score'].transform(softmax)
    return data

# gs scoring methods

def gs_scoring(data):
    return gs_scoring_probs(data)

def gs_scoring_probs(data):
    data['Score'] = data.apply(lambda x: np.where(np.char.strip((x['Score']), chars='\n') == x['label'])[0].shape[0]/len(x['Score']), axis=1)
    return data

# vc scoring methods

def vc_scoring(data, groupby):
    return vc_scoring_normalize(data, groupby)
    return vc_scoring_softmax(data, groupby)

def vc_scoring_normalize(data, groupby):
    data['Score'] = data['Score'].apply(lambda score: extract_score(score))
    data['Score'] = data.groupby(groupby)['Score'].transform(lambda score: score/score.sum())
    return data

def vc_scoring_softmax(data, groupby):
    data['Score'] = data['Score'].apply(lambda score: extract_score(score))
    data['Score'] = data.groupby(groupby)['Score'].transform(softmax)
    return data

def extract_score(score_output):
    scores = []
    for i in range(len(score_output)):
        output = score_output[i]
        pattern = r'Confidence:?.?[0-9]+(?:\.[0-9]+)?'
        percentages = re.findall(pattern, output)
        if percentages == None or len(percentages) == 0:
            scores.append(0)
            continue
        confidence_str = percentages[0]
        number_pattern = r'[0-9]+(?:\.[0-9]+)?'
        number = re.findall(number_pattern, confidence_str)
        if number == None or len(number) != 1:
            scores.append(0)
            continue
        float_number = float(number[0])
        if float_number < 0 or float_number > 100:
            scores.append(0)
        else:
            scores.append(float_number)
    return np.array(scores).mean()
