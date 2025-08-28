

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
    'better'
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
    'jobs',
    'market',
    'housing',
    'macro',
    'wages',
    'prices',
    'retail',
    # confidence ?
    'interest',
    'currency',
    'energy',
    'other'
]

QUANTITY_POLARITY_LABELS = [
    "positive",
    "negative",
    "neutral"
]

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

TF_ARTICLE_DIRECTION_USER_PROMPT = '''
Consider the task of identifying the type of economic information covered in a U.S News Article. Given the content of the article, answer the following true/false question corresponding to whether or not a specific type of economic information was most prevalent in the article.'''

TF_ARTICLE_DIRECTION_USER_PROMPT = '''
Article Text: {Text}

Q. The main type of economic information covered in the article is {label} - true or false? A.'''


