import src.helpers.prompting.moral_prompting as moral_prompting
import src.helpers.prompting.mf_prompt_constants as constants
import src.helpers.loaders.mf_dataset_loader as dataset_loader
import src.analysis.analysis_helper as analysis_helper
import sys
import sklearn.metrics as sk
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from typing import List
import networkx as nx
import src.helpers.loaders.genia_dataset_loader as genia_dataset_loader



def create_coref_dumps(rel_rows, gold_clus, pred_clus, g_base_id, p_base_id, gold_dump, pred_dump):
    sent_ids = []
    sentences = []
    gold_ent_tags = []
    pred_ent_tags = []
    mention_traversed = []
   
    with open(gold_dump, "a+") as f:
        f.write(f"""#begin document ({rel_rows[0]['doc_id']});\n""")
    with open(pred_dump, "a+") as f:
        f.write(f"""#begin document ({rel_rows[0]['doc_id']});\n""")


    for row in rel_rows:
        doc_id = row['doc_id']
        if row["sent1_id"] not in sent_ids:
            sent_ids.append(row["sent1_id"])
            sentences.append(row["sent1"])
            gold_ent_tags.append(["_"]*len(row['sent1']))
            pred_ent_tags.append(["_"]*len(row['sent1']))
        if row["sent2_id"] not in sent_ids:
            sent_ids.append(row["sent2_id"])
            sentences.append(row["sent2"])
            gold_ent_tags.append(["_"]*len(row['sent2']))
            pred_ent_tags.append(["_"]*len(row['sent2']))
        
        if row["mention_id1"] not in mention_traversed:
            gold_cluster_id =  get_cluster(gold_clus, row["mention_id1"])
            pred_cluster_id =  get_cluster(pred_clus, row["mention_id1"])
            
            sent_ref_id = sent_ids.index(row["sent1_id"]) # Location of the corresponding sentence
           
            if len(row["ent1_ix"]) == 1:
                gold_ent_tags[sent_ref_id][row["ent1_ix"][0]] = f"({gold_cluster_id+g_base_id})"
                pred_ent_tags[sent_ref_id][row["ent1_ix"][0]] = f"({pred_cluster_id+p_base_id})"
            else:
                gold_ent_tags[sent_ref_id][row["ent1_ix"][0]] = f"({gold_cluster_id+g_base_id}"
                pred_ent_tags[sent_ref_id][row["ent1_ix"][0]] = f"({pred_cluster_id+p_base_id}"
                gold_ent_tags[sent_ref_id][row["ent1_ix"][-1]] = f"{gold_cluster_id+g_base_id})"
                pred_ent_tags[sent_ref_id][row["ent1_ix"][-1]] = f"{pred_cluster_id+p_base_id})"

            mention_traversed.append(row["mention_id1"])

        if row["mention_id2"] not in mention_traversed:
            gold_cluster_id =  get_cluster(gold_clus, row["mention_id2"])
            pred_cluster_id =  get_cluster(pred_clus, row["mention_id2"])

            sent_ref_id = sent_ids.index(row["sent2_id"])

            if len(row["ent2_ix"]) == 1:
                gold_ent_tags[sent_ref_id][row["ent2_ix"][0]] = f"({gold_cluster_id+g_base_id})"
                pred_ent_tags[sent_ref_id][row["ent2_ix"][0]] = f"({pred_cluster_id+p_base_id})"
            else:
                gold_ent_tags[sent_ref_id][row["ent2_ix"][0]] = f"({gold_cluster_id+g_base_id}"
                pred_ent_tags[sent_ref_id][row["ent2_ix"][0]] = f"({pred_cluster_id+p_base_id}"
                gold_ent_tags[sent_ref_id][row["ent2_ix"][-1]] = f"{gold_cluster_id+g_base_id})"
                pred_ent_tags[sent_ref_id][row["ent2_ix"][-1]] = f"{pred_cluster_id+p_base_id})"


            mention_traversed.append(row["mention_id2"])
    
     
    last_words = 0
    for ix, sent in enumerate(sentences):
        sent_id = sent_ids[ix]
        for w_ix, word in enumerate(sent): 
            with open(gold_dump, "a+") as f:
                f.write(f"""{doc_id}\t{sent_id}\t{last_words+w_ix}\t{word}\t{gold_ent_tags[ix][w_ix]}\n""")
            with open(pred_dump, "a+") as f:
                f.write(f"""{doc_id}\t{sent_id}\t{last_words+w_ix}\t{word}\t{pred_ent_tags[ix][w_ix]}\n""")

        last_words += len(sent)

    with open(gold_dump, "a+") as f:
        f.write(f"""\n""")
        f.write("#end document\n")
    with open(pred_dump, "a+") as f:
        f.write(f"""\n""")
        f.write("#end document\n")


    return g_base_id+len(gold_clus), p_base_id+len(pred_clus)

       

def eval_ontonotes(data, preds, meta):
    """ Evaluate Coref dataset
    """
    doc = None
    gold_ans = []
    gold_relation_ids = []
    pred_relation_ids = []
    pred_relation_ids_no = []

    all_relation_ids = []
    post_inf_ans = []
    rel_rows = []
    max_nodes = 0

    gold_base_id = 0
    pred_base_id = 0

    with open(meta['gold_dump_file'], "w+") as f:
        f.write("")
    with open(meta['pred_dump_file'], "w+") as f:
        f.write("")

    g_viol = 0
    p_viol = 0
    num_transitivity = 0
    
    debug_flag = False

    for ix, row in data.iterrows():
        
        if doc == None:
            doc = row["doc_id"]


        # Change in doc_id implies a new structure
        if doc != row["doc_id"]:
        
            gold_clus, gold_violations  = right_to_left_search(gold_relation_ids, max_nodes)
            pred_clus, _  = right_to_left_search(pred_relation_ids, max_nodes)
            
            pred_violations, total_checks = check_violations(pred_relation_ids, pred_relation_ids_no, max_nodes)

            g_viol += gold_violations
            p_viol += pred_violations
        

            num_transitivity += total_checks
            if not meta['constrained']:
                modified_ans = get_modified_ans(pred_clus, all_relation_ids)
                post_inf_ans.extend(modified_ans)

            gold_base_id, pred_base_id = create_coref_dumps(rel_rows, gold_clus, pred_clus, gold_base_id, pred_base_id, meta['gold_dump_file'], meta['pred_dump_file'])

            # Refresh List
            gold_relation_ids = []
            pred_relation_ids = []
            pred_relation_ids_no = []
            all_relation_ids = []
            doc = row["doc_id"]
            max_nodes = 0
            rel_rows = []

        gold_ans.append(row['answer'])  # List which stores the gold answers
        max_nodes = max(max_nodes, row["mention_id1"]+1, row["mention_id2"]+1)
        rel_rows.append(row)
        # Curate edges to form the clusters ultimately
        
        if row['answer'] == 'Yes':
            gold_relation_ids.append([row['mention_id1'], row["mention_id2"]])
        if preds[ix] == 'Yes':
            pred_relation_ids.append([row['mention_id1'], row["mention_id2"]])
        elif preds[ix] == 'No':
            pred_relation_ids_no.append([row['mention_id1'], row["mention_id2"]])

        all_relation_ids.append([row['mention_id1'], row["mention_id2"]])


    # For the last document
    gold_clus, gold_violations = right_to_left_search(gold_relation_ids, max_nodes)
    pred_clus, _ = right_to_left_search(pred_relation_ids, max_nodes)

    pred_violations, total_checks = check_violations(pred_relation_ids, pred_relation_ids_no, max_nodes)

    g_viol += gold_violations
    p_viol += pred_violations
    num_transitivity += total_checks

    if not meta['constrained']:
        modified_ans = get_modified_ans(pred_clus, all_relation_ids)
        post_inf_ans.extend(modified_ans)

    _, _ = create_coref_dumps(rel_rows, gold_clus, pred_clus, gold_base_id, pred_base_id, meta['gold_dump_file'], meta['pred_dump_file'])



    f1 = f1_score(gold_ans, preds, average='macro')
    print(f"F1 Score (Pre-inference): {f1}")
    if not meta['constrained']:
        f1_post = f1_score(gold_ans, post_inf_ans, average='macro')
        print(f"F1 Score (Post-inference): {f1_post}")
    #print(f"Gold Violations: {g_viol}")
    if not meta['constrained']:
        print(f"Transitivity Violations (Prediciton): {p_viol}")
        print(f"Total transitivity checks: {num_transitivity}")

def get_cluster(clusters, ent_id):
    for c_ix, clus in enumerate(clusters):
        if ent_id in clus:
            return c_ix
        
def check_violations(yes_ids, no_ids, max_mentions):
    rel_mat = np.full((max_mentions,max_mentions),"N", dtype=str)
    for rel in yes_ids:
        low = min(rel)
        high = max(rel)
        rel_mat[low][high] = "Y"
   
    for rel in no_ids:
        low = min(rel)
        high = max(rel)
        rel_mat[low][high] = "N"
    
    
    transitivity_viol = 0
    total_checks = 0

    # Computing transivity violations
    for i in range(1, max_mentions):
        for j in range(i+1, max_mentions):
            for k in range(j+1, max_mentions):
                at_least_two_edges = False 
                if (rel_mat[i][j] == "Y") and (rel_mat[j][k] == "Y"):
                    if rel_mat[i][k] != "N/A":
                        at_least_two_edges = True
                    if rel_mat[i][k] == "N":
                        transitivity_viol += 1
                        #print(i,j,k)
                elif (rel_mat[i][k] == "Y") and (rel_mat[j][k] == "Y"):
                    if rel_mat[i][j] != "N/A":
                        at_least_two_edges = True
                    if rel_mat[i][j] == "N":
                        transitivity_viol += 1
                        #print(i,j,k)
                elif (rel_mat[i][j] == "Y") and (rel_mat[i][k] == "Y"):
                    if rel_mat[j][k] != "N/A":
                        at_least_two_edges = True
                    if rel_mat[j][k] == "N":
                        transitivity_viol += 1
                        #print(i,j,k)

                if at_least_two_edges:
                    total_checks += 1
    
    return transitivity_viol, total_checks
        
def get_modified_ans(clusters, all_relations):
    # In case the where there were violations and corrections
    # were to be made, we need to get the modified answers for the prompts
    
    modified_ans = []
    for rel in all_relations:
        ent1_clus = None
        ent2_clus = None
        for c_ix, clus in enumerate(clusters):
            if rel[0] in clus:
                ent1_clus = c_ix 
                break
        for c_ix, clus in enumerate(clusters):
            if rel[1] in clus:
                ent2_clus = c_ix 
                break

        assert ent1_clus != None
        assert ent2_clus != None

        if ent1_clus == ent2_clus:
            modified_ans.append("Yes")
        else:
            modified_ans.append("No")
    
    return modified_ans.copy() 

def right_to_left_search(rel_ids, max_mentions):
    """ Anaphora resolution heuristic
    """
    #prinre
    rel_mat = np.full((max_mentions,max_mentions),"N", dtype=str)
    for rel in rel_ids:
        low = min(rel)
        high = max(rel)
        rel_mat[low][high] = "Y"
    
    clusters = [[0]]
    viol = 0
    transitivity_viol = 0

    # Computing transivity violations
    for i in range(1, max_mentions):
        for j in range(i+1, max_mentions):
            for k in range(j+1, max_mentions):
                trans_sum = 0
                if rel_mat[i][j] == "Y":
                    trans_sum += 1
                if rel_mat[j][k] == "Y":
                    trans_sum += 1
                if rel_mat[i][k] == "Y":
                    trans_sum += 1
                
                # The transitivity constrint is broken if exactly two 
                # edges exists between the mentions
                if trans_sum == 2:
                    transitivity_viol += 1


    for i in range(1,max_mentions):
        flag = True
        cluster_id = None
        for j in range(i-1,-1,-1):
            # Analyse if the model says coreferrent
            if rel_mat[j][i] == "Y":
                if flag:
                    # Condition when the nearest antexedent matches
                    for c_ix, clus in enumerate(clusters):
                        if j in clus:
                            clusters[c_ix].append(i)
                            flag = False
                            cluster_id = c_ix
                            break
                else:
                    # All other antecedents not in the same 
                    # cluster are considered violations
                    if j not in clusters[cluster_id]:
                        viol += 1
        if flag:
            clusters.append([i])
       
    return clusters, transitivity_viol

def get_all_cliques(relations, max_vertices):
    """ Get all cliques from pairwise connections. This function can be used to 
    obtain cliques based on pairs of connections. Useful for applications like
    coref resolution.

    Inputs
    --------------------
    relations - List[List[int]]. List of connections in the form of tuple
    max_vertices - int. Number of verices in the graph.
    """
    gr = nx.Graph()
    nodes = list(range(max_vertices))
    gr.add_nodes_from(nodes)
    gr.add_edges_from(relations)

    clusters = []

    violations = 0

    max_clique = list(nx.algorithms.approximation.max_clique(gr)) 
    clusters.append(max_clique)

    prev_rels = relations
    
    # Compute cliques for rest of the graph
    while True:
        # Remove already clustered nodes
        for node in clusters[-1]:
            nodes.remove(node)
        
        if len(nodes)==0:
            break

        new_rels = []
        for rel in prev_rels:
            if ((rel[0] in clusters[-1]) and (rel[1] in nodes)) or ((rel[1] in clusters[-1]) and (rel[0] in nodes)):
                violations += 1
            elif (rel[0] in nodes) and (rel[1] in nodes):
                new_rels.append(rel)
        prev_rels = new_rels
        
        sub_gr = nx.Graph()
        sub_gr.add_nodes_from(nodes)
        sub_gr.add_edges_from(new_rels)

        m_clique = list(nx.algorithms.approximation.max_clique(sub_gr)) 
        clusters.append(m_clique)
        
    return clusters, violations
def main():
    dataset_dir = sys.argv[1]
    input_path = sys.argv[2]
    data = genia_dataset_loader.preprocess_genia_coref(dataset_dir, True)
    predictions_list = analysis_helper.load_multiple_results(input_path)
    for prediction_data in predictions_list:
        predicted_labels = []
        for index, row in data.iterrows():
            document_predictions = prediction_data['content'][row['doc_id']]
            for pred in document_predictions:
                if pred['Entity_1'] == row['var_id_entity1'] and pred['Entity_2'] == row['var_id_entity2']:
                    predicted_labels.append('Yes' if int(pred['Value']) == 1 else 'No')
        meta = {
            'gold_dump_file': 'C:\\Users\\mpauk\\Downloads\\gold.txt',
            'pred_dump_file': 'C:\\Users\\mpauk\\Downloads\\pred.txt',
            'constrained': False
        }
        print('Results ' + prediction_data['name'] + ' :')
        eval_ontonotes(data, predicted_labels, meta)
        print('\n\n')
'''
def main():
    dataset_dir = sys.argv[1]
    input_path = sys.argv[2]
    data = genia_dataset_loader.preprocess_genia_coref(dataset_dir)
    predictions_list = analysis_helper.load_multiple_results(input_path)
    for prediction_data in predictions_list:
        true_labels = []
        predicted_labels = []
        for index, row in data.iterrows():
            true_labels.append(1 if row['answer'] == 'Yes' else 0)
            document_predictions = prediction_data['content'][row['doc_id']]
            for pred in document_predictions:
                if pred['Entity_1'] == row['entity1_id'] and pred['Entity_2'] == row['entity2_id']:
                    predicted_labels.append(int(pred['Value']))
        print('Results ' + prediction_data['name'] + ' :')
        print('F1: ')
        print(sk.f1_score(true_labels, predicted_labels, average='macro'))
        print('\n\n')
'''
    
if __name__ == "__main__":
    main()