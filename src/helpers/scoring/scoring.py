import torch
from scipy.special import softmax
import numpy as np

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

