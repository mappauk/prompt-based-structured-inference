### Moral Foundation Identification

## One Pass
MORAL_FOUNDATION_IDENTIFICATION_ONE_PASS = ('Moral Foundation Definitions: CARE/HARM: Care for others, generosity, compassion, ability to feel pain of others, sensitivity '
    'to suffering of others, prohibiting actions that harm others. FAIRNESS/CHEATING: Demand for Fairness, rights, equality, justice, '
    'reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. LOYALTY/BETRAYAL: '
    'Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. '
    'AUTHORITY/SUBVERSION: Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, '
    'prohibiting rebellion against authority. PURITY/DEGRADATION: Associations with the sacred and holy, disgust, contamination, religious'
    'notions which guide how to live, prohibiting violating the sacred. ### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling '
    'sick message on immigration http://t.co/OOTpD9zmh5 Moral foundation expressed in the tweet: PURITY/DEGRADATION ### Tweet: Today’s decision '
    'by #SCOTUSs is huge victory for justice and equality for the #LGBT community and our nation Moral foundation expressed in the tweet: '
    'FAIRNESS/CHEATING ### Tweet: We can and must reduce #GunViolence by closing gaps in our gun laws. You can help: get engaged and be part '
    'of the conversation. Moral foundation expressed in the tweet: CARE/HARM ### Tweet: Sit or stand but we cannot be silent for victims of gun '
    'violence - we need to take action. #NoBillNoBreak Moral foundation expressed in the tweet: LOYALTY/BETRAYAL ### Tweet: At @ChiUrbanLeague today '
    'calling for Congressional action on gun violence. It\'s past time to act. #Enough Moral foundation expressed in the tweet: AUTHORITY/SUBVERSION '
    '### Tweet: {0} Moral foundation '
    'expressed in the tweet: ')

MORAL_FOUNDATION_IDENTIFICATION_ONE_PASS_TF = ('Moral Foundation Definitions: CARE/HARM: Care for others, generosity, compassion, ability to feel pain of others, sensitivity '
    'to suffering of others, prohibiting actions that harm others. FAIRNESS/CHEATING: Demand for Fairness, rights, equality, justice, '
    'reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. LOYALTY/BETRAYAL: '
    'Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. '
    'AUTHORITY/SUBVERSION: Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, '
    'prohibiting rebellion against authority. PURITY/DEGRADATION: Associations with the sacred and holy, disgust, contamination, religious'
    'notions which guide how to live, prohibiting violating the sacred. {0}'
    '### Tweet: {Tweet}'
    'Q. "The moral foundation expressed in the tweet is {label}." - True or False?'
    'A. ')

MORAL_FOUNDATION_IDENTIFICATION_EXAMPLE_FORMAT = (
    '### Tweet: {0} Q. "The moral foundation expressed in the tweet is {1}." - True or False? A. {2}'
)

## One Vs All

# Definitions
CARE_HARM_DEFINITON = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others.'
FAIRNESS_CHEATING_DEFINITION = 'Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating.'
AUTHORITY_SUBVERSION_DEFINITION = 'Definition of the moral foundation "AUTHORITY/SUBVERSION": Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, prohibiting rebellion against authority.'
PURITY_DEGRADATION_DEFINITION = 'Definition of the moral foundation "PURITY/DEGRADATION": Associations with the sacred and holy, disgust, contamination, religious notions which guide how to live, prohibiting violating the sacred.'
LOYALTY_BETRAYAL_DEFINITION = 'Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group.'

MORAL_FOUNDATION_DEFINITIONS_MAP = {
    'CARE/HARM': CARE_HARM_DEFINITON,
    'FAIRNESS/CHEATING': FAIRNESS_CHEATING_DEFINITION,
    'AUTHORITY/SUBVERSION': AUTHORITY_SUBVERSION_DEFINITION,
    'PURITY/DEGRADATION': PURITY_DEGRADATION_DEFINITION,
    'LOYALTY/BETRAYAL': LOYALTY_BETRAYAL_DEFINITION
}
# Positive Examples
CARE_HARM_POSITIVE_EXAMPLES = [
    'Recent actions in Indiana and Arkansas made clear that Congress must act to protect #LGBT Americans from discrimination'        
]
FAIRNESS_CHEATING_POSITIVE_EXAMPLES = [
    'Today’s decision by #SCOTUSs is huge victory for justice and equality for the #LGBT community and our nation'
]
AUTHORITY_SUBVERSION_POSITIVE_EXAMPLES = [
    'At @ChiUrbanLeague today calling for Congressional action on gun violence. It\'s past time to act. #Enough'
]
PURITY_DEGRADATION_POSITIVE_EXAMPLES = [
    'RT @LatinoVoices: Joe Biden slams Donald Trump for selling sick message on immigration http://t.co/OOTpD9zmh5'
]
LOYALTY_BETRAYAL_POSITIVE_EXAMPLES = [
    'Sit or stand but we cannot be silent for victims of gun violence - we need to take action. #NoBillNoBreak'
]

MORAL_FOUNDATION_POSITIVE_EXAMPLES_MAP = {
    'CARE/HARM': CARE_HARM_POSITIVE_EXAMPLES,
    'FAIRNESS/CHEATING': FAIRNESS_CHEATING_POSITIVE_EXAMPLES,
    'AUTHORITY/SUBVERSION': AUTHORITY_SUBVERSION_POSITIVE_EXAMPLES,
    'PURITY/DEGRADATION': PURITY_DEGRADATION_POSITIVE_EXAMPLES,
    'LOYALTY/BETRAYAL': LOYALTY_BETRAYAL_POSITIVE_EXAMPLES
}

# Negative Examples
CARE_HARM_NEGATIVE_EXAMPLES = [
    'Today’s decision by #SCOTUSs is huge victory for justice and equality for the #LGBT community and our nation'      
]
FAIRNESS_CHEATING_NEGATIVE_EXAMPLES = [
    'At @ChiUrbanLeague today calling for Congressional action on gun violence. It\'s past time to act. #Enough'
]
AUTHORITY_SUBVERSION_NEGATIVE_EXAMPLES = [
    'RT @LatinoVoices: Joe Biden slams Donald Trump for selling sick message on immigration http://t.co/OOTpD9zmh5'
]
PURITY_DEGRADATION_NEGATIVE_EXAMPLES = [
    'Sit or stand but we cannot be silent for victims of gun violence - we need to take action. #NoBillNoBreak'
]
LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES = [
    'Recent actions in Indiana and Arkansas made clear that Congress must act to protect #LGBT Americans from discrimination'
]

MORAL_FOUNDATION_NEGATIVE_EXAMPLES_MAP = {
    'CARE/HARM': CARE_HARM_NEGATIVE_EXAMPLES,
    'FAIRNESS/CHEATING': FAIRNESS_CHEATING_NEGATIVE_EXAMPLES,
    'AUTHORITY/SUBVERSION': AUTHORITY_SUBVERSION_NEGATIVE_EXAMPLES,
    'PURITY/DEGRADATION': PURITY_DEGRADATION_NEGATIVE_EXAMPLES,
    'LOYALTY/BETRAYAL': LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES
}

MORAL_FOUNDATION_ROLE = [
    'Target of care/harm',
    'Entity causing harm',
    'Entity providing care',
    'Target of fairness/cheating',
    'Entity ensuring fairness',
    'Entity doing cheating',
    'Target of loyalty/betrayal',
    'Entity being loyal',
    'Entity doing betrayal',
    'Justified authority over',
    'Failing authority',
    'Failing authority over',
    'Target of purity/degradation',
    'Entity preserving purity',
    'Entity causing degradation'
]

# 1 positive, 0 negative
POLARITY_MAP = {
    'Entity causing harm': 0,
    'Entity providing care': 1,
    'Entity ensuring fairness': 1,
    'Entity doing cheating': 0,
    'Entity being loyal': 1,
    'Entity doing betrayal': 0,
    'Entity preserving purity': 1,
    'Entity causing degradation': 0
}

MORAL_FOUNDATION_ROLE_TO_MF = {
    'Target of care/harm': 'CARE/HARM',
    'Entity causing harm': 'CARE/HARM',
    'Entity providing care': 'CARE/HARM',
    'Target of fairness/cheating': 'FAIRNESS/CHEATING',
    'Entity ensuring fairness': 'FAIRNESS/CHEATING',
    'Entity doing cheating': 'FAIRNESS/CHEATING',
    'Target of loyalty/betrayal': 'LOYALTY/BETRAYAL',
    'Entity being loyal': 'LOYALTY/BETRAYAL',
    'Entity doing betrayal': 'LOYALTY/BETRAYAL',
    'Justified authority over': 'AUTHORITY/SUBVERSION',
    'Failing authority': 'AUTHORITY/SUBVERSION',
    'Failing authority over': 'AUTHORITY/SUBVERSION',
    'Target of purity/degradation': 'PURITY/DEGRADATION',
    'Entity preserving purity': 'PURITY/DEGRADATION',
    'Entity causing degradation': 'PURITY/DEGRADATION'
}

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [

]

MORAL_FOUNDATION_ROLE_POSITIVE_EXAMPLES = {

}


# One Vs All Format Strings
MORAL_FOUNDATION_IDENTIFICATION_EXAMPLE_FORMAT = '### Tweet: {0} Q."The moral foundation expressed in the tweet is {1}." - True or False? A. {2}'
MORAL_FOUNDATION_IDENTIFICATION_QUESTION_FORMAT = '### Tweet: {0} Q."The moral foundation expressed in the tweet is {1}." - True or False? A. '
MORAL_FOUNDATION_IDENTIFICATION_TIE_EXAMPLE_FORMAT = '### Tweet: {0} The moral foundation expressed in the tweet is: {1}.'
MORAL_FOUNDATION_IDENTIFICATION_TIE_QUESTION_FORMAT = '### Tweet: {0} The moral foundation expressed in the tweet is: '