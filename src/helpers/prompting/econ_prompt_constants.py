

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
Consider the task of identifying the type of economic information covered in a U.S News Article. Given the content of the article, answer the following true/false question corresponding to whether or not a specific type of economic information was most prevalent in the article.
The possible economic information types are macro, government, personal, industry, and business. If the article discusses some economic information that does not fit into any of these categories it is classified as "other".
'''

TF_ARTICLE_TYPE_EXAMPLE_PROMPT = '''
Article Text: {Text}

Q. The main type of economic information covered in the article is {label} - true or false? A.'''

TF_ARTICLE_CONDITIONS_SYSTEM_PROMPT = '''
Consider the task of identifying the general economic conditions based on the economic information covered in a U.S News Article. Given the content of the article, answer the following true/false question corresponding to the framing of the general economic conditions.
Economic conditions can be described as good, poor, irrelevant, or none. Irrelevant is used to describe articles that do not discuss the general U.S economic conditions at all, while none describes those articles that discuss general economic conditions but do not fit into the good or poor categories.
'''

TF_ARTICLE_CONDITIONS_USER_PROMPT = '''
Article Text: {Text}

Q. The condition of the economy as reported by the article is {label} - true or false? A.'''

TF_ARTICLE_DIRECTION_SYSTEM_PROMPT = '''
Consider the task of identifying the direction the U.S economy is headed based on the economic information covered in a U.S News Article. Given the content of the article, answer the following true/false question corresponding to the framing of the direction the U.S economy is headed.
The direction the economy is headed can be described as same, worse, better, irrelevant, or none. Irrelevant is used to describe articles that do not discuss the general U.S economic conditions and their direction at all, while none describes those articles that discuss the direction the economy is headed but do not fit into any of the other categories.
'''

TF_ARTICLE_DIRECTION_USER_PROMPT = '''
Article Text: {Text}

Q. The direction the U.S economy is headed based on the information covered in the article is {label} - true or false? A.'''

TF_QUANTITY_TYPE_SYSTEM_PROMPT = '''
Consider the task of identifying the type of a piece of economic data from a U.S news article. Given an excerpt from an article discussing a piece of economic data, answer the following true/false question regarding whether or not the economic data presented is of a specific type.
The possible economic information types are macro, government, personal, industry, and business. If the article discusses some economic information that does not fit into any of these categories it is classified as "other".

'''

TF_QUANTITY_TYPE_USER_PROMPT = '''
Economic Data: {IndicatorText}
Excerpt: {Context}

Q. The type of the economic data is {label} - true or false? A.'''

TF_QUANTITY_INDICATOR_SYSTEM_PROMPT = '''
Consider the task of identifying what type of economic indicator is being represented by a piece of economic data in a U.S news article. Given an excerpt from an article discussing a piece of economic data, answer the following true/false question regarding what type of economic indicator is being reported.
The possible economic indicator types are jobs, retail, interest, prices, energy, wages, macro, market, currency, housing, other, and none. Other represents economic data focused on some indicator that is not one of the given types. None describes any economic data that is not focused on a particular U.S economic indicator.
'''

TF_QUANTITY_INDICATOR_USER_PROMPT = '''
Economic Data: {IndicatorText}
Excerpt: {Context}

Q. The economic indicator type associated with the economic data is {label} - true or false? A.
'''

TF_QUANTITY_POLARITY_SYSTEM_PROMPT = '''
Consider the task of identifying the polarity of a piece of economic data from a U.S news article. Given an excerpt from an article discussing a piece of economic data, answer the following true/false question regarding the polarity of the economic data. The polarity of the economic data can either be positive, negative, or neutral.
'''

TF_QUANTITY_POLARITY_USER_PROMPT = '''
Economic Data: {IndicatorText}
Excerpt: {Context}

Q. The polarity of the economic data is {label} - true or false? A.
'''

MC_TASK_TO_CHOICE_MAP = {
    
}


ECON_RULE_TO_LABEL_COLUMN_NAME = {
    'rule_one': 'Type',
    'rule_two': 'Conditions',
    'rule_three': 'Direction',
    'rule_four': 'Type',
    'rule_five': 'IndicatorType',
    'rule_six': 'Polarity'
}

