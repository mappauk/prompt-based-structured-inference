

ARTICLE_ECONOMIC_TYPE_LABELS = [
    'macro',
    'government',
    'industry',
    'business',
    'other',
    'personal'
]

ARTICLE_ECONOMIC_CONDITIONS_LABELS = [
    'irrelevant',
    'good',
    'poor',
    'none'
]

ARTICLE_ECONOMIC_DIRECTION_LABELS = [
    'same',
    'worse',
    'better',
    'none',
    'irrelevant'
]

QUANTITY_TYPE_LABELS = [
    'macro',
    'government',
    'industry',
    'business',
    'personal',
    'other'
]

QUANTITY_INDICATOR_LABELS = [
    'jobs', # macro
    'retail', # macro, industry
    'interest', # macro, government
    'prices', # macro
    'energy', # macro
    'wages', # macro
    'macro', # macro
    'market', # macro
    'currency', # macro
    'housing', # macro, government
    'other',
    'none'
]

QUANTITY_POLARITY_LABELS = [
    "positive",
    "negative",
    "neutral"
]

QUANTITY_POLARITY_TO_ARTICLE_CONDITIONS = {
    'negative': 'poor',
    'positive': 'good'
}

QUANTITY_POLARITY_TO_ARTICLE_DIRECTION = {
    'negative': 'worse',
    'positive': 'better'
}

SYSTEM_PROMPT_EXAMPLE_LEAD_IN = 'Consider the following examples:\n'

TF_ARTICLE_TYPE_SYSTEM_PROMPT = '''
Consider the task of identifying the type of economic information covered in a U.S News Article. Given the content of the article, answer the following true/false question corresponding to whether or not a specific type of economic information was most prevalent in the article.'''

TF_ARTICLE_TYPE_EXAMPLE_PROMPT = '''
Article Text: {Text}

Q. The main type of economic information covered in the article is {label} - true or false? A.'''

TF_ARTICLE_CONDITIONS_SYSTEM_PROMPT = '''
Consider the task of identifying the general economic conditions based on the economic information covered in a U.S News Article. Given the content of the article, answer the following true/false question corresponding to the framing of the general economic conditions.'''

TF_ARTICLE_CONDITIONS_USER_PROMPT = '''
Article Text: {Text}

Q. The main type of economic information covered in the article is {label} - true or false? A.'''

TF_ARTICLE_DIRECTION_SYSTEM_PROMPT = '''
Consider the task of identifying the type of economic information covered in a U.S News Article. Given the content of the article, answer the following true/false question corresponding to whether or not a specific type of economic information was most prevalent in the article.'''

TF_ARTICLE_DIRECTION_USER_PROMPT = '''
Article Text: {Text}

Q. The main type of economic information covered in the article is {label} - true or false? A.'''

TF_QUANTITY_TYPE_SYSTEM_PROMPT = '''
Consider the task of identifying the type of a piece of economic data from a U.S news article. Given an excerpt from an article discussing a piece of economic data, answer the following true/false question regarding whether or not the economic data presented is of a specific type.
'''

TF_QUANTITY_TYPE_USER_PROMPT = '''
Economic Data: {IndicatorText}
Excerpt: {Context}

Q. The type of the economic data is {Type} - true or false? A.'''

TF_QUANTITY_INDICATOR_SYSTEM_PROMPT = '''
Consider the task of identifying what type of economic indicator is being represented by a piece of economic data in a U.S news article. Given an excerpt from an article discussing a piece of economic data, answer the following true/false question regarding what type of economic indicator is being reported.
'''

TF_QUANTITY_INDICATOR_USER_PROMPT = '''
Economic Data: {IndicatorText}
Excerpt: {Context}

Q. The economic indicator type associated with the economic data is {Type} - true or false? A.
'''

TF_QUANTITY_POLARITY_SYSTEM_PROMPT = '''
Consider the task of identifying the polarity of a piece of economic data from a U.S news article. Given an excerpt from an article discussing a piece of economic data, answer the following true/false question regarding the polarity of the economic data. The polarity of the economic data can either be positive, negative, or neutral.
'''

TF_QUANTITY_POLARITY_USER_PROMPT = '''
Economic Data: {IndicatorText}
Excerpt: {Context}

Q. The polarity of the economic data is {Polarity} - true or false? A.
'''

MC_TASK_TO_CHOICE_MAP = {
    
}


