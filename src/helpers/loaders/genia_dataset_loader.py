#from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import re
from tqdm import tqdm
import xml.etree.ElementTree as ET
from itertools import combinations

class XMLParser():
    def __init__(self, filename):
        with open(filename) as fd:
            self.lines = fd.readlines()
    
    def get_docid(self):
        """ Gets article ID from the lines 
        """
        for line in self.lines:
            if line[:6] == "<PMID>":
                p = re.compile("<PMID>(.*)</PMID>")
                result = p.findall(line)
                return result[0]
        raise Exception("No <PMID> found")

    def get_sent_lines(self):
        self.sent_ids = []
        self.sent_lines = []

        for l_ix, line in enumerate(self.lines):
            if line[:9] == "<sentence":
                p = re.compile("""<sentence id="S(..?)">""")
                result = p.findall(line)
                self.sent_ids.append(int(result[0])-1)
                self.sent_lines.append(l_ix)



    def process_coref_data(self):
        coref_dict = {"sentences": [], "entities": {}, "sent_ixs": []}
        men_id = 0
        ent_dict = {}
        for l_ix, line_id in enumerate(self.sent_lines):
            coref_dict["sent_ixs"].append(0)
            sent_cnt_ix = l_ix

            line = self.lines[line_id]
            sent_p = re.compile("""<sentence id="S(..?)">(.*)</sentence>""")
            line_data = sent_p.findall(line)[0][1]

            token_list = []
            coref_open = False
            meta_open = False
            token_id = -1
            ent_id = None
            skip = 0

            line_data = line_data.replace(" <","<")
            line_data = line_data.replace("<", " <")
            line_data = line_data.replace("> ",">")
            line_data = line_data.replace(">", "> ")

            for token in line_data.split():
                if meta_open:
                    if token[:3] == "ref":
                        try:
                            tok_p = re.compile("ref=\"(.*)\"")
                            ent_id = tok_p.findall(token)[0]
                        except IndexError:
                            tok_p = re.compile("ref=\"(.*)")
                            ent_id = tok_p.findall(token)[0]
                            
                            

                    if token[:2] == "id":
                        tok_p = re.compile("id=\"(.*)\"")
                        try:
                            inter_ent = tok_p.findall(token)[0].replace(">","")
                        except IndexError:
                            print(line_data)
                            print(token)
                            exit()

                        if ent_id == None:
                            ent_id = inter_ent
                        else:
                            parent = ent_id
                            while True:
                                if ent_id in ent_dict.keys():
                                    ent_id = ent_dict[ent_id]
                                else:
                                    break
                            ent_dict[inter_ent] = ent_id
                        
                        meta_open = False
                    continue

                if token == "<coref":
                    if coref_open:
                        skip += 1
                        continue
                    # Case where coref 
                    coref_open = True
                    meta_open = True
                    tok_idx = []
                elif "</coref>" in token:
                    # Closing Multi-word reference text
                    if skip !=0:
                        # Ignore if nested entities
                        skip -= 1
                        continue
                    #token_id += 1
                    #token_list.append(token.replace("</coref>",""))
                    #tok_idx.append(token_id)
                    if ent_id not in coref_dict["entities"].keys():
                        coref_dict["entities"][ent_id] = []    
                    coref_dict["entities"][ent_id].append({"sent_id":sent_cnt_ix, "tok_idx":tok_idx, "mention_id":men_id})
                    men_id += 1
                    coref_open = False
                    ent_id = None
                else:
                    # Normal token
                    if ("id=" in token) or \
                        ("min=" in token) or \
                        ("type=" in token) or \
                        ("ref=" in token):
                        continue
                    token_id += 1
                    token_list.append(token)
                    if coref_open:
                        tok_idx.append(token_id)

            coref_dict["sentences"].append(token_list) 
            #print(line_data.split())
                       
            assert skip == 0 #There should be no open mention
            assert coref_open == False
            assert meta_open == False
        
 
        return coref_dict


def generate_examples(c_dict, doc_id):
        """ Generate positive and negative examples from a document
        """
        examples = []
        entity_list = list(c_dict["entities"].keys())
        traversed = []
        # Iterating over entities
        for ent_id in c_dict["entities"].keys():
            traversed.append(ent_id)
            # We can generate positive examples from entities which
            # occur more than once
            if len(c_dict["entities"][ent_id]) > 1:
                # Curating pairs of mentions for the positive examples
                pairs = list(combinations(c_dict["entities"][ent_id],2))
                for pair in pairs:
                    # Extarcting entities
                    s_id1 = pair[0]["sent_id"]
                    s_id2 = pair[1]["sent_id"]
                    
                    norm_ent1_ids = [i-c_dict["sent_ixs"][s_id1] for i in pair[0]["tok_idx"] ]
                    norm_ent2_ids = [i-c_dict["sent_ixs"][s_id2] for i in pair[1]["tok_idx"] ]
                    
                    ent1 = " ".join([c_dict["sentences"][s_id1][i] for i in norm_ent1_ids])
                    ent2 = " ".join([c_dict["sentences"][s_id2][i] for i in norm_ent2_ids])
                
                    sent1 = " ".join(c_dict["sentences"][s_id1])
                    sent2 = " ".join(c_dict["sentences"][s_id2])

                    mention_id1 = pair[0]["mention_id"]
                    mention_id2 = pair[1]["mention_id"]

                    in_order = True

                    if pair[0]["sent_id"] == pair[1]["sent_id"]:
                        context  = f"{sent1}"
                    elif pair[0]["sent_id"] < pair[1]["sent_id"]:
                        context = f"{sent1} {sent2}"
                    else:
                        in_order = False
                        context = f"{sent2} {sent1}"
                    
                    examples.append([doc_id, c_dict["sentences"],context, "Yes", ent1, ent2, entity_list.index(ent_id), entity_list.index(ent_id), c_dict["sentences"][s_id1], c_dict["sentences"][s_id2],s_id1,s_id2,norm_ent1_ids, norm_ent2_ids, in_order, ent_id, ent_id, mention_id1, mention_id2])
            
            ## Generate negative examples 
            # Iterate over the entities
            for ent in c_dict["entities"][ent_id]:
                s_id1 = ent["sent_id"]
                norm_ent1_ids = [i-c_dict["sent_ixs"][s_id1] for i in ent["tok_idx"] ]
                ent1 = " ".join([c_dict["sentences"][s_id1][i] for i in norm_ent1_ids])
                sent1 = " ".join(c_dict["sentences"][s_id1])
                mention_id1 = ent["mention_id"]
                # Iterating over entites dissimilar to the one considered
                for neg_ent_id in c_dict["entities"].keys():
                    if (neg_ent_id == ent_id) or (neg_ent_id in traversed):
                        continue
                    # Iterating over all negative instances of a negative entity
                    for neg_ent in c_dict["entities"][neg_ent_id]:
                        s_id2 = neg_ent["sent_id"]
                        norm_ent2_ids = [i-c_dict["sent_ixs"][s_id2] for i in neg_ent["tok_idx"] ]
                        ent2 = " ".join([c_dict["sentences"][s_id2][i] for i in norm_ent2_ids])
                        sent2 = " ".join(c_dict["sentences"][s_id2])
                        
                        ent1_id = ent_id
                        ent2_id = neg_ent_id
                        in_order = True
                        mention_id2 = neg_ent["mention_id"]

                        if s_id1 == s_id2:
                            context  = f"{sent1}"
                            if mention_id1 > mention_id2:
                                in_order = False
                        elif s_id1 < s_id2:
                            context = f"{sent1} {sent2}"
                        else:
                            context = f"{sent2} {sent1}"
                            in_order = False
                        

                        examples.append([doc_id, c_dict["sentences"], context, "No", ent1, ent2, entity_list.index(ent1_id), entity_list.index(ent2_id), c_dict["sentences"][s_id1], c_dict["sentences"][s_id2],s_id1,s_id2,norm_ent1_ids, norm_ent2_ids, in_order, ent1_id, ent2_id,mention_id1, mention_id2])
        return examples

def preprocess_doc(filename):
    parser = XMLParser(filename)
    doc_id = parser.get_docid()
    
    parser.get_sent_lines()
    coref_dict = parser.process_coref_data() 
    
    examples = generate_examples(coref_dict, doc_id)

    return examples


def preprocess_genia_coref(filepath, analysis=False):
    """ Preprocess files to dataframe for the Genia dataset
    Input
    ------------
    filepath - str or Path. Folder path to the XML files

    Output
    -----------
    df - pd.DataFrame. Dataframe containing the processed data.
    """
    files = list(Path(filepath).glob("*.xml"))
    files.sort()
    doc = []
    # Iterating over all the files in the set
    for f in tqdm(files):
        if str(f)[-12:] in ["10214854.xml","/8513868.xml", '/10025668.xml']: #Skipping
            continue
        
        examples  = preprocess_doc(f)
        doc.extend(examples)
    columns = ["doc_id","passage","sentence","answer","entity1","entity2","entity1_id","entity2_id","sent1","sent2","sent1_id","sent2_id","ent1_ix","ent2_ix","in_order","ent1_ix_glob", "ent2_ix_glob", "mention_id1", "mention_id2"]
    data_df = pd.DataFrame(doc, columns=columns)
    if not analysis:
        data_df['sent1'] = data_df['sent1'].apply(lambda sent_list: ' '.join(sent_list))
        data_df['sent2'] = data_df['sent2'].apply(lambda sent_list: ' '.join(sent_list))
        data_df['entity1_id'] = data_df['sent1_id'].astype(str) + data_df['mention_id1'].astype(str)
        data_df['entity2_id'] = data_df['sent2_id'].astype(str) + data_df['mention_id2'].astype(str)
        return data_df[['doc_id', 'entity1', 'entity2', 'entity1_id', 'entity2_id', 'sent1', 'sent2', 'answer']]
    else:
        data_df['var_id_entity1'] = data_df['sent1_id'].astype(str) + data_df['mention_id1'].astype(str)
        data_df['var_id_entity2'] = data_df['sent2_id'].astype(str) + data_df['mention_id2'].astype(str)
        return data_df