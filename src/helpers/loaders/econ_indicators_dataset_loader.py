import os
import json
import re
import pandas as pd
import src.helpers.prompting.mf_prompt_constants as constants
import sqlite3
import pickle

def load_econ_indicators_qual(datapath, db_filename):
    data = pickle.load(open(datapath, 'rb'))
    doc_ids = []
    type = []
    conditions = []
    direction = []
    text = []
    for key, value in data.items():
        doc_ids.append(key)
        type.append(value['frame'])
        conditions.append(value['econ_rate'])
        direction.append(value['econ_change'])
        text.append(get_article_text(key, db_filename, clean=True))
    
    return pd.DataFrame(
        {
            'Id': doc_ids,
            'Type': type,
            'Conditions': conditions,
            'Direction': direction,
            "Text": text,
        }
    )

def load_econ_indicators_quant(datapath):
    data = pickle.load(open(datapath, 'rb'))
    doc_ids = []
    ids = []
    quant_ids = []
    type = []
    indicator = []
    polarity = []
    indicator_text = []
    indicator_text_with_context = []
    for key, value in data.items():
        key_split = key.split('_')
        ids.append(key)
        doc_ids.append(key_split[0])
        quant_ids.append(key_split[1])
        type.append(value['type'])
        indicator.append(value['macro_type'])
        polarity.append(value['spin'])
        indicator_text.append(value['indicator'])
        indicator_text_with_context.append(value['excerpt'])
    
    return pd.DataFrame(
        {
            'Id': ids,
            'DocId': doc_ids,
            'QuantId': quant_ids,
            'Type': type,
            'Polarity': polarity,
            'IndicatorType': indicator,
            'IndicatorText': indicator_text, 
            "Context": indicator_text_with_context
        }
    )

def extract_strings(dirty_str: str):
    clean = re.sub('<[^>]+>', '', dirty_str)
    return clean


def get_article_text(article_id: int, db_filename: str, clean: bool = True, headline: bool = False):
    """
    Takes article_id and db filename
    Returns cleaned text of article as string
    """
    con = sqlite3.connect(db_filename)
    cur = con.cursor()

    text = ''

    query = 'SELECT text\
        FROM article ' \
        + 'WHERE id is ' + str(article_id) + ';'
    article_txt = cur.execute(query).fetchone()

    text = article_txt[0]
    if clean:
        text = extract_strings(article_txt[0])
    if headline:
        query = "SELECT headline FROM article WHERE id is " + str(article_id) + ";"
        headline = cur.execute(query).fetchone()
        text = [headline[0], text]
        
    con.close()

    return text