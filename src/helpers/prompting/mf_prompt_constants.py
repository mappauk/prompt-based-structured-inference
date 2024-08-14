# Moral Foundation Identification

## Moral Frames

CARE_HARM = 'CARE/HARM'
FAIRNESS_CHEATING = 'FAIRNESS/CHEATING'
AUTHORITY_SUBVERSION = 'AUTHORITY/SUBVERSION'
PURITY_DEGREDATION = 'PURITY/DEGRADATION'
LOYALTY_BETRAYAL = 'LOYALTY/BETRAYAL'

MORAL_FOUNDATIONS = [
    CARE_HARM,
    FAIRNESS_CHEATING,
    AUTHORITY_SUBVERSION,
    PURITY_DEGREDATION,
    LOYALTY_BETRAYAL
]

## Moral Frame Roles

TARGET_CARE_HARM = 'Target of care/harm'
ENTITY_CAUSING_HARM = 'Entity causing harm'
ENTITY_PROVIDING_CARE = 'Entity providing care'
TARGET_FAIRNESS_CHEATING = 'Target of fairness/cheating'
ENTITY_ENSURING_FAIRNESS = 'Entity ensuring fairness'
ENTITY_DOING_CHEATING = 'Entity doing cheating'
TARGET_LOYALTY_BETRAYAL = 'Target of loyalty/betrayal'
ENTITY_BEING_LOYAL = 'Entity being loyal'
ENTITY_DOING_BETRAYAL = 'Entity doing betrayal'
JUSTIFIED_AUTHORITY = 'Justified authority'
JUSTIFIED_AUTHORITY_OVER = 'Justified authority over'
FAILING_AUTHORITY = 'Failing authority'
FAILING_AUTHORITY_OVER = 'Failing authority over'
TARGET_PURITY_DEGREDATION = 'Target of purity/degradation'
ENTITY_PRESERVING_PURITY = 'Entity preserving purity'
ENTITY_CAUSING_DEGRADATION = 'Entity causing degradation'

MORAL_FOUNDATION_ROLE = [
    TARGET_CARE_HARM,
    ENTITY_CAUSING_HARM,
    ENTITY_PROVIDING_CARE,
    TARGET_FAIRNESS_CHEATING,
    ENTITY_ENSURING_FAIRNESS,
    ENTITY_DOING_CHEATING,
    TARGET_LOYALTY_BETRAYAL,
    ENTITY_BEING_LOYAL,
    ENTITY_DOING_BETRAYAL,
    JUSTIFIED_AUTHORITY,
    JUSTIFIED_AUTHORITY_OVER,
    FAILING_AUTHORITY,
    FAILING_AUTHORITY_OVER,
    TARGET_PURITY_DEGREDATION,
    ENTITY_PRESERVING_PURITY,
    ENTITY_CAUSING_DEGRADATION
]

# Mapping Between Moral Foundations and Roles

MORAL_FOUNDATION_ROLE_TO_MF = {
    TARGET_CARE_HARM: CARE_HARM,
    ENTITY_CAUSING_HARM: CARE_HARM,
    ENTITY_PROVIDING_CARE: CARE_HARM,
    TARGET_FAIRNESS_CHEATING: FAIRNESS_CHEATING,
    ENTITY_ENSURING_FAIRNESS: FAIRNESS_CHEATING,
    ENTITY_DOING_CHEATING: FAIRNESS_CHEATING,
    TARGET_LOYALTY_BETRAYAL: LOYALTY_BETRAYAL,
    ENTITY_BEING_LOYAL: LOYALTY_BETRAYAL,
    ENTITY_DOING_BETRAYAL: LOYALTY_BETRAYAL,
    JUSTIFIED_AUTHORITY: AUTHORITY_SUBVERSION,
    JUSTIFIED_AUTHORITY_OVER: AUTHORITY_SUBVERSION,
    FAILING_AUTHORITY: AUTHORITY_SUBVERSION,
    FAILING_AUTHORITY_OVER: AUTHORITY_SUBVERSION,
    TARGET_PURITY_DEGREDATION: PURITY_DEGREDATION,
    ENTITY_PRESERVING_PURITY: PURITY_DEGREDATION,
    ENTITY_CAUSING_DEGRADATION: PURITY_DEGREDATION
}

# Moral Role Polarity map
# 1 positive, 0 negative
POLARITY_MAP = {
    ENTITY_CAUSING_HARM: 0,
    ENTITY_PROVIDING_CARE: 1,
    ENTITY_ENSURING_FAIRNESS: 1,
    ENTITY_DOING_CHEATING: 0,
    ENTITY_BEING_LOYAL: 1,
    ENTITY_DOING_BETRAYAL: 0,
    ENTITY_PRESERVING_PURITY: 1,
    ENTITY_CAUSING_DEGRADATION: 0
}

# Moral foundation/roles question map

MORAL_FOUNDATION_TO_QUESTIONS = {
    CARE_HARM: ['q1', 'q2', 'q3'],
    FAIRNESS_CHEATING: ['q2', 'q3', 'q4'],
    AUTHORITY_SUBVERSION: ['q2', 'q3', 'q4', 'q5'],
    PURITY_DEGREDATION: ['q1', 'q2', 'q3'],
    LOYALTY_BETRAYAL: ['q3', 'q4', 'q5']
}

QUESTION_TO_MORAL_FOUNDATION = {
    CARE_HARM: {
        'q1': TARGET_CARE_HARM,
        'q2': ENTITY_CAUSING_HARM,
        'q3': ENTITY_PROVIDING_CARE
    },
    FAIRNESS_CHEATING: {
        'q2': TARGET_FAIRNESS_CHEATING,
        'q3': ENTITY_ENSURING_FAIRNESS,
        'q4': ENTITY_DOING_CHEATING
    },
    AUTHORITY_SUBVERSION: {
        'q2': JUSTIFIED_AUTHORITY,
        'q3': JUSTIFIED_AUTHORITY_OVER,
        'q4': FAILING_AUTHORITY,
        'q5': FAILING_AUTHORITY_OVER,
    },
    PURITY_DEGREDATION: {
        'q1': TARGET_PURITY_DEGREDATION,
        'q2': ENTITY_PRESERVING_PURITY,
        'q3': ENTITY_CAUSING_DEGRADATION
    },
    LOYALTY_BETRAYAL: {
        'q3': TARGET_LOYALTY_BETRAYAL,
        'q4': ENTITY_BEING_LOYAL,
        'q5': ENTITY_DOING_BETRAYAL,
    }
}

MORAL_FOUNDATION_ROLE_TO_QUESTION = {
    'q1': TARGET_CARE_HARM,
    'q2': ENTITY_CAUSING_HARM,
    'q3': ENTITY_PROVIDING_CARE,
    'q2': TARGET_FAIRNESS_CHEATING,
    'q3': ENTITY_ENSURING_FAIRNESS,
    'q4': ENTITY_DOING_CHEATING,
    'q3': TARGET_LOYALTY_BETRAYAL,
    'q4': ENTITY_BEING_LOYAL,
    'q5': ENTITY_DOING_BETRAYAL,
    'q2': JUSTIFIED_AUTHORITY,
    'q3': JUSTIFIED_AUTHORITY_OVER,
    'q4': FAILING_AUTHORITY,
    'q5': FAILING_AUTHORITY_OVER,
    'q1': TARGET_PURITY_DEGREDATION,
    'q2': ENTITY_PRESERVING_PURITY,
    'q3': ENTITY_CAUSING_DEGRADATION
}

## One vs All
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

MORAL_FOUNDATION_IDENTIFICATION_ONE_VS_ALL_TF = ('Moral Foundation Definitions: CARE/HARM: Care for others, generosity, compassion, ability to feel pain of others, sensitivity '
    'to suffering of others, prohibiting actions that harm others. FAIRNESS/CHEATING: Demand for Fairness, rights, equality, justice, '
    'reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. LOYALTY/BETRAYAL: '
    'Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. '
    'AUTHORITY/SUBVERSION: Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, '
    'prohibiting rebellion against authority. PURITY/DEGRADATION: Associations with the sacred and holy, disgust, contamination, religious'
    'notions which guide how to live, prohibiting violating the sacred. {0}'
    '### Tweet: {Tweet}'
    'Q. "The moral foundation expressed in the tweet is {label}." - True or False?'
    'A. ')

## One Pass

MORAL_FOUNDATION_IDENTIFICATION_ONE_PASS_TF = (
    '### Tweet: {Tweet} '
    'Q. "The moral foundation expressed in the tweet is {label}." - True or False? '
    'A. ')

MORAL_FOUNDATION_IDENTIFICATION_ONE_PASS_WITH_FEATURES_TF = (
    '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} '
    'Q. "The moral foundation expressed in the tweet is {label}." - True or False? '
    'A. ')

MORAL_ROLE_IDENTIFICATION_ONE_PASS_TF = (
    '### Tweet: {Tweet} '
    'Q. "The moral role of {Entity} expressed in the tweet is {label}." - True or False? '
    'A. ')

MORAL_ROLE_IDENTIFICATION_ONE_PASS_WITH_FEATURES_TF = (
    '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} '
    'Q. "The moral role of {Entity} expressed in the tweet is {label}." - True or False? '
    'A. ')

MORAL_FOUNDATION_IDENTIFICATION_ALLVSONE = '### Tweet: {Tweet} Q. "What is the moral foundation expressed in the tweet?" A. '
MORAL_FOUNDATION_IDENTIFICATION_ALLVSONE_WITH_FEATURES = '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} Q. "What is the moral foundation expressed in the tweet?" A. '
MORAL_ROLE_IDENTIFICATION_ALLVSONE_PASS = '### Tweet: {Tweet} Q. "What is the moral role expressed by {Entity} in the tweet? A. '
MORAL_ROLE_IDENTIFICATION_ALLVSONE_WITH_FEATURES= '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} Q. "What is the moral role expressed by {Entity} in the tweet? A. '

MORAL_FOUNDATION_PROMPT_EXAMPLE_FORMAT = '### Tweet: {Tweet} Q. "The moral foundation expressed in the tweet is {label}." - True or False? A. {answer}'
MORAL_FOUNDATION_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT = '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} Q. "The moral foundation expressed in the tweet is {label}." - True or False? A. {answer}'
MORAL_ROLE_PROMPT_EXAMPLE_FORMAT = '### Tweet: {Tweet} Q. "The moral role of {Entity} expressed in the tweet is {label}." - True or False? A. {answer}'
MORAL_ROLE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT = '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} Q. "The moral role of {Entity} expressed in the tweet is {label}." - True or False? A. {answer}'


MORAL_FOUNDATION_ALLVONE_PROMPT_EXAMPLE_FORMAT = '### Tweet: {Tweet} Q. "What is the moral foundation expressed in the tweet?" A. {label}'
MORAL_FOUNDATION_ALLVONE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT = '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} Q. "What is the moral foundation expressed in the tweet?" A. {label}'
MORAL_ROLE_ALLVONE_PROMPT_EXAMPLE_FORMAT = '### Tweet: {Tweet} Q. "What is the moral role expressed by {Entity} in the tweet? A. {label}'
MORAL_ROLE_ALLVONE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT = '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} Q. "What is the moral role expressed by {Entity} in the tweet? A. {label}'

# Definitions

CARE_HARM_DEFINITON = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others.'
FAIRNESS_CHEATING_DEFINITION = 'Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating.'
AUTHORITY_SUBVERSION_DEFINITION = 'Definition of the moral foundation "AUTHORITY/SUBVERSION": Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, prohibiting rebellion against authority.'
PURITY_DEGRADATION_DEFINITION = 'Definition of the moral foundation "PURITY/DEGRADATION": Associations with the sacred and holy, disgust, contamination, religious notions which guide how to live, prohibiting violating the sacred.'
LOYALTY_BETRAYAL_DEFINITION = 'Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group.'

MORAL_FOUNDATION_ALL_DEFINITION = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others. Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. Definition of the moral foundation "AUTHORITY/SUBVERSION": Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, prohibiting rebellion against authority. Definition of the moral foundation "PURITY/DEGRADATION": Associations with the sacred and holy, disgust, contamination, religious notions which guide how to live, prohibiting violating the sacred. Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one\’s group.'
MORAL_ROLE_ALL_DEFINITION = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others. Definition of the moral role "Target of care/harm": Entity that is harmed by someone/something or entity someone/something is providing/offering care to. Definition of the moral role "Entity providing care": Entity that is providing or offering care or expressing the need for care for someone/something. Definition of the moral role "Entity causing harm": Entity that is harming/hurting or doing something bad to someone/something. Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. Definition of the moral role "Target of fairness/cheating":  Entity that someone/something is cheating or entity someone/something is being fair to. Definition of the moral role "Entity ensuring fairness": Entity that is ensuring fairness for someone/something. Definition of the moral role "Entity doing cheating": Entity that is cheating someone/something. Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. Definition of the moral role "Target of loyalty/betrayal": Entity that someone/something is being loyal to or entity someone/something is betraying. Definition of the moral role "Entity being loyal": Entity that is being loyal to someone/something. Definition of the moral role "Entity doing betrayal": Entity that is betrayings someone/something. Definition of the moral foundation "AUTHORITY/SUBVERSION": Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, prohibiting rebellion against authority. Definition of the moral role "Justified authority":  Entity that is the appropriate authority. Definition of the moral role "Justified authority over": Entity that someone/something is the authority over. Definition of the moral role "Failing authority": Entity that is not an appropriate authority. Definition of the moral role "Failing authority over": Entity that someone/something which is not an appropriate authority is expressing authority over. Definition of the moral foundation "PURITY/DEGRADATION": Associations with the sacred and holy, disgust, contamination, religious notions which guide how to live, prohibiting violating the sacred. Definition of the moral role "Target of purity/degredation": Entity that someone/something is associating with being pure/sacred or entity someone/something is associating with being contaminated/unsanctified. Definition of the moral role "Entity preserving purity": Entity that is being pure/sacred. Definition of the moral role "Entity causing degredation": Entity that is contaminated/unsanctified.'

#CARE_HARM_ROLES_DEFINITION = ' Definitions of moral roles: Entity target of care/harm: Entity that is harmed by someone/something or entity someone/something is providing/offering care to. Entity providing care: Entity that is providing or offering care or expressing the need for care for someone/something. Entity causing harm: Entity that is harming/hurting or doing something bad to someone/something.'
#FAIRNESS_CHEATING_ROLES_DEFINITION = 'Definitions of moral roles: Entity target of fairness/cheating: Entity that someone/something is cheating or entity someone/something is being fair to. Entity ensuring fairness: Entity that is ensuring fairness for someone/something. Entity doing cheating: Entity that is cheating someone/something.'
#AUTHORITY_SUBVERSION_ROLES_DEFINITION = 'Definitions of moral roles: Entity justified authority: Entity that is the appropriate authority. Entity justified authority over: Entity that someone/something is the authority over. Entity failing authority: Entity that is not an appropriate authority. Entity failing authority over: Entity that someone/something which is not an appropriate authority is expressing authority over.'
#PURITY_DEGRADATION_ROLES_DEFINITION = 'Definitions of moral roles: Entity target of purity/degradation: Entity that someone/something is associating with being pure/sacred or entity someone/something is associating with being contaminated/unsanctified. Entity preserving purity: Entity that is being pure/sacred. Entity causing degradation: Entity that is contaminated/unsanctified.'
#LOYALTY_BETRAYAL_ROLES_DEFINITION = 'Definitions of moral roles: Entity target of loyalty/betrayal: Entity that someone/something is being loyal to or entity someone/something is betraying. Entity being loyal: Entity that is being loyal to someone/something. Entity doing betrayal: Entity that is betrayings someone/something.'

TARGET_CARE_HARM_ROLE_DEFINITION = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others. Definition of the moral role "Target of care/harm": Entity that is harmed by someone/something or entity someone/something is providing/offering care to.'
ENTITY_PROVIDING_CARE_ROLE_DEFINITION = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others. Definition of the moral role "Entity providing care": Entity that is providing or offering care or expressing the need for care for someone/something.'
ENTITY_CAUSING_HARM_ROLE_DEFINITION = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others. Definition of the moral role "Entity causing harm": Entity that is harming/hurting or doing something bad to someone/something.'

TARGET_FAIRNESS_CHEATING_ROLE_DEFINITION = 'Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. Definition of the moral role "Target of fairness/cheating":  Entity that someone/something is cheating or entity someone/something is being fair to.'
ENTITY_ENSURING_FAIRNESS_ROLE_DEFINITION = 'Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. Definition of the moral role "Entity ensuring fairness": Entity that is ensuring fairness for someone/something.'
ENTITY_DOING_CHEATING_ROLE_DEFINITION = 'Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. Definition of the moral role "Entity doing cheating": Entity that is cheating someone/something.'

TARGET_LOYALTY_BETRAYAL_ROLE_DEFINITION = 'Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. Definition of the moral role "Target of loyalty/betrayal": Entity that someone/something is being loyal to or entity someone/something is betraying.'
ENTITY_BEING_LOYAL_ROLE_DEFINITION = 'Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. Definition of the moral role "Entity being loyal": Entity that is being loyal to someone/something.'
ENTITY_DOING_BETRAYAL_ROLE_DEFINITION = 'Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. Definition of the moral role "Entity doing betrayal": Entity that is betraying someone/something.'

JUSTIFIED_AUTHORITY_ROLE_DEFINITION = 'Definition of the moral foundation "AUTHORITY/SUBVERSION": Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, prohibiting rebellion against authority. Definition of the moral role "Justified authority":  Entity that is the appropriate authority.'
JUSTIFIED_AUTHORITY_OVER_ROLE_DEFINITION = 'Definition of the moral foundation "AUTHORITY/SUBVERSION": Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, prohibiting rebellion against authority. Definition of the moral role "Justified authority over": Entity that someone/something is the authority over.'
FAILING_AUTHORITY_ROLE_DEFINITION = 'Definition of the moral foundation "AUTHORITY/SUBVERSION": Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, prohibiting rebellion against authority. Definition of the moral role "Failing authority": Entity that is not an appropriate authority.'
FAILING_AUTHORITY_OVER_ROLE_DEFINITION = 'Definition of the moral foundation "AUTHORITY/SUBVERSION": Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, prohibiting rebellion against authority. Definition of the moral role "Failing authority over": Entity that someone/something which is not an appropriate authority is expressing authority over.'

TARGET_PURITY_DEGREDATION_ROLE_DEFINITION = 'Definition of the moral foundation "PURITY/DEGRADATION": Associations with the sacred and holy, disgust, contamination, religious notions which guide how to live, prohibiting violating the sacred. Definition of the moral role "Target of purity/degredation": Entity that someone/something is associating with being pure/sacred or entity someone/something is associating with being contaminated/unsanctified.'
ENTITY_PRESERVING_PURITY_ROLE_DEFINITION = 'Definition of the moral foundation "PURITY/DEGRADATION": Associations with the sacred and holy, disgust, contamination, religious notions which guide how to live, prohibiting violating the sacred. Definition of the moral role "Entity preserving purity": Entity that is being pure/sacred.'
ENTITY_CAUSING_DEGRADATION_ROLE_DEFINITION = 'Definition of the moral foundation "PURITY/DEGRADATION": Associations with the sacred and holy, disgust, contamination, religious notions which guide how to live, prohibiting violating the sacred. Definition of the moral role "Entity causing degredation": Entity that is contaminated/unsanctified.'



MORAL_FOUNDATION_DEFINITIONS_MAP = {
    # frames
    CARE_HARM: CARE_HARM_DEFINITON,
    FAIRNESS_CHEATING: FAIRNESS_CHEATING_DEFINITION,
    AUTHORITY_SUBVERSION: AUTHORITY_SUBVERSION_DEFINITION,
    PURITY_DEGREDATION: PURITY_DEGRADATION_DEFINITION,
    LOYALTY_BETRAYAL: LOYALTY_BETRAYAL_DEFINITION,
    # roles
    TARGET_CARE_HARM: TARGET_CARE_HARM_ROLE_DEFINITION,
    ENTITY_CAUSING_HARM: ENTITY_CAUSING_HARM_ROLE_DEFINITION,
    ENTITY_PROVIDING_CARE: ENTITY_PROVIDING_CARE_ROLE_DEFINITION,
    TARGET_FAIRNESS_CHEATING: TARGET_FAIRNESS_CHEATING_ROLE_DEFINITION,
    ENTITY_ENSURING_FAIRNESS: ENTITY_ENSURING_FAIRNESS_ROLE_DEFINITION,
    ENTITY_DOING_CHEATING: ENTITY_DOING_CHEATING_ROLE_DEFINITION,
    TARGET_LOYALTY_BETRAYAL: TARGET_CARE_HARM_ROLE_DEFINITION,
    ENTITY_BEING_LOYAL: ENTITY_BEING_LOYAL_ROLE_DEFINITION,
    ENTITY_DOING_BETRAYAL: ENTITY_DOING_BETRAYAL_ROLE_DEFINITION,
    JUSTIFIED_AUTHORITY: JUSTIFIED_AUTHORITY_ROLE_DEFINITION,
    JUSTIFIED_AUTHORITY_OVER: JUSTIFIED_AUTHORITY_OVER_ROLE_DEFINITION,
    FAILING_AUTHORITY: FAILING_AUTHORITY_ROLE_DEFINITION,
    FAILING_AUTHORITY_OVER: FAILING_AUTHORITY_OVER_ROLE_DEFINITION,
    TARGET_PURITY_DEGREDATION: TARGET_PURITY_DEGREDATION_ROLE_DEFINITION,
    ENTITY_PRESERVING_PURITY: ENTITY_PRESERVING_PURITY_ROLE_DEFINITION,
    ENTITY_CAUSING_DEGRADATION: ENTITY_CAUSING_DEGRADATION_ROLE_DEFINITION 
}

MORAL_FOUNDATION_CLUSTER = 'MoralFoundationCluster'
CARE_HARM_ROLE_CLUSTER = 'CareHarmCluster'
LOYALTY_BETRAYAL_ROLE_CLUSTER = 'LoyaltyBetrayalCluster'
FAIRNESS_CHEATING_ROLE_CLUSTER = 'FairnessCheatingCluster'
AUTHORITY_SUBVERSION_ROLE_CLUSTER = 'AuthoritySubversionCluster'
PURITY_DEGREDATION_ROLE_CLUSTER = 'PurityDegredationCluster'

FOUNDATION_CLUSTER_LABEL_MAP = {
    MORAL_FOUNDATION_CLUSTER: [CARE_HARM, LOYALTY_BETRAYAL, FAIRNESS_CHEATING, AUTHORITY_SUBVERSION, PURITY_DEGREDATION],
}

ROLE_CLUSTER_LABEL_MAP = {
    CARE_HARM_ROLE_CLUSTER: [TARGET_CARE_HARM, ENTITY_CAUSING_HARM, ENTITY_PROVIDING_CARE],
    LOYALTY_BETRAYAL_ROLE_CLUSTER: [TARGET_LOYALTY_BETRAYAL, ENTITY_DOING_BETRAYAL, ENTITY_BEING_LOYAL],
    FAIRNESS_CHEATING_ROLE_CLUSTER: [TARGET_FAIRNESS_CHEATING, ENTITY_DOING_CHEATING, ENTITY_ENSURING_FAIRNESS],
    AUTHORITY_SUBVERSION_ROLE_CLUSTER: [FAILING_AUTHORITY, FAILING_AUTHORITY_OVER, JUSTIFIED_AUTHORITY, JUSTIFIED_AUTHORITY_OVER],
    PURITY_DEGREDATION_ROLE_CLUSTER: [TARGET_PURITY_DEGREDATION, ENTITY_CAUSING_DEGRADATION, ENTITY_PRESERVING_PURITY]
}

GEN_Z_MF_PARAPHRASE_PROMPT = 'Write 10 paraphrases of this sentence as a Python list. “This tweet expresses the moral foundation [MORAL_FOUNDATION] which is defined as [MORAL_FOUNDATION_DEFINITION].”; MORAL_FOUNDATION∈{CARE/HARM, FAIRNESS/CHEATING, AUTHORITY/SUBVERSION, PURITY/DEGRADATION, LOYALTY/BETRAYAL}, MORAL_FOUNDATION_DEFINITION={definition of corresponding MORAL_FOUNDATION}. This is a multi label classification task for the moral foundation.'
GEN_Z_MF_PARAPHRASE_PROMPT_WITH_CONTEXT = 'Write 10 paraphrases of this sentence as a Python list. “This tweet about [TOPIC] whose author is a [POLITICAL_PARTY] expresses the moral foundation [MORAL_FOUNDATION] which is defined as [MORAL_FOUNDATION_DEFINITION].”; TOPIC∈{affordable care act, immigration, abortion, guns, terrorism, lgbtq}, POLITICAL_PARTY∈{democrat, republican}, MORAL_FOUNDATION∈{CARE/HARM, FAIRNESS/CHEATING, AUTHORITY/SUBVERSION, PURITY/DEGRADATION, LOYALTY/BETRAYAL}, MORAL_FOUNDATION_DEFINITION={definition of corresponding MORAL_FOUNDATION}. This is a multi label classification task for the moral foundation.'
GEN_Z_MF_ROLE_PARAPHRASE_PROMPT = 'Write 10 paraphrases of this sentence as a Python list. “This entity [ENTITY] in this tweet exhibits the moral role [MORAL_ROLE] defined as [MORAL_ROLE_DEFINITION]."'
GEN_Z_MF_ROLE_PARAPHRASE_PROMPT_WITH_CONTEXT = 'Write 10 paraphrases of this sentence as a Python list. “This entity [ENTITY] in this tweet about [TOPIC] and written by a [POLITICAL_PARTY] exhibits the moral role [MORAL_ROLE] defined as [MORAL_ROLE_DEFINITION]."'

GEN_Z_MF_TWEET_FORMAT = ' ### Tweet: {Tweet}'

GEN_Z_MF_INTRO_ZERO_SHOT = 'Generate a tweet based on the following description.'
GEN_Z_MF_FEW_SHOT_EXAMPLES = 'Generate a tweet based on the following description. For Example: '
GEN_Z_MF_PREFIX = '### Generation description:'
GEN_Z_MF_EXAMPLE_FORMAT = '### Generation description: {0} ### Tweet: {1}'
GEN_Z_MF_LABEL_SENTENCES = [
    "This tweet expresses the moral foundation {MORAL_FOUNDATION} which is defined as: {MORAL_FOUNDATION_DEFINITION}",
    "This tweet reflects the moral foundation {MORAL_FOUNDATION}, which is defined as: {MORAL_FOUNDATION_DEFINITION}",
    "The tweet showcases the moral foundation {MORAL_FOUNDATION}, described as: {MORAL_FOUNDATION_DEFINITION}",
    "In this tweet, the moral foundation {MORAL_FOUNDATION} is expressed, defined as: {MORAL_FOUNDATION_DEFINITION}",
    "This tweet highlights the moral foundation {MORAL_FOUNDATION}, which means: {MORAL_FOUNDATION_DEFINITION}",
    "The moral foundation {MORAL_FOUNDATION} is conveyed in this tweet, defined as: {MORAL_FOUNDATION_DEFINITION}",
    "This tweet demonstrates the moral foundation {MORAL_FOUNDATION}, described as: {MORAL_FOUNDATION_DEFINITION}",
    "In this tweet, the author expresses the moral foundation {MORAL_FOUNDATION}, which is defined as: {MORAL_FOUNDATION_DEFINITION}",
    "This tweet communicates the moral foundation {MORAL_FOUNDATION}, described as: {MORAL_FOUNDATION_DEFINITION}"
    "This tweet conveys the moral foundation {MORAL_FOUNDATION}, defined as: {MORAL_FOUNDATION_DEFINITION}"
]

GEN_Z_MF_LABEL_SENTENCES_WITH_CONTEXT = [
    "This tweet about {{Topic}} whose author is a {{Ideology}} expresses the moral foundation {MORAL_FOUNDATION} which is defined as: {MORAL_FOUNDATION_DEFINITION}",
    "This tweet on {{Topic}} by a {{Ideology}} reflects the moral foundation {MORAL_FOUNDATION}, defined as: {MORAL_FOUNDATION_DEFINITION}",
    "A {{Ideology}} wrote this tweet about {{Topic}} expressing the moral foundation {MORAL_FOUNDATION}, which means: {MORAL_FOUNDATION_DEFINITION}",
    "The tweet on {{Topic}} authored by a {{Ideology}} highlights the moral foundation {MORAL_FOUNDATION}, described as: {MORAL_FOUNDATION_DEFINITION}",
    "In this tweet about {{Topic}}, the {{Ideology}} author conveys the moral foundation {MORAL_FOUNDATION}, defined as: {MORAL_FOUNDATION_DEFINITION}",
    "This tweet regarding {{Topic}} by a {{Ideology}} showcases the moral foundation {MORAL_FOUNDATION}, which is: {MORAL_FOUNDATION_DEFINITION}",
    "The moral foundation {MORAL_FOUNDATION} is highlighted in this tweet about {{Topic}} by a {{Ideology}}, defined as: {MORAL_FOUNDATION_DEFINITION}",
    "Written by a {{Ideology}}, this tweet on {{Topic}} expresses the moral foundation {MORAL_FOUNDATION}, defined as: {MORAL_FOUNDATION_DEFINITION}",
    "This tweet about {{Topic}} by a {{Ideology}} illustrates the moral foundation {MORAL_FOUNDATION}, defined as: {MORAL_FOUNDATION_DEFINITION}",
    "In this tweet about {{Topic}}, written by a {{Ideology}}, the moral foundation {MORAL_FOUNDATION} is expressed, defined as: {MORAL_FOUNDATION_DEFINITION}",
]

GEN_Z_MF_ROLE_LABEL_SENTENCES = [
    "In this tweet, the entity {{Entity}} displays the moral role {MORAL_ROLE}, defined as: {MORAL_ROLE_DEFINITION}",
    "This tweet shows the entity {{Entity}} exhibiting the moral role {MORAL_ROLE}, which is defined as: {MORAL_ROLE_DEFINITION}",
    "The entity {{Entity}} in this tweet demonstrates the moral role {MORAL_ROLE}, described as: {MORAL_ROLE_DEFINITION}",
    "In this tweet, {{Entity}} reflects the moral role {MORAL_ROLE}, which is defined as: {MORAL_ROLE_DEFINITION}",
    "{{Entity}} in this tweet exemplifies the moral role {MORAL_ROLE}, defined as: {MORAL_ROLE_DEFINITION}",
    "This tweet portrays the entity {{Entity}} as embodying the moral role {MORAL_ROLE}, described as: {MORAL_ROLE_DEFINITION}",
    "The entity {{Entity}} in this tweet illustrates the moral role {MORAL_ROLE}, which is defined as: {MORAL_ROLE_DEFINITION}",
    "{{Entity}} shows the moral role {MORAL_ROLE} in this tweet, defined as: {MORAL_ROLE_DEFINITION}",
    "In this tweet, {{Entity}} reveals the moral role {MORAL_ROLE}, defined as: {MORAL_ROLE_DEFINITION}",
    "This tweet features {{Entity}} expressing the moral role {MORAL_ROLE}, which is defined as: {MORAL_ROLE_DEFINITION}"
]

GEN_Z_MF_ROLE_LABEL_SENTENCES_WITH_CONTEXT = [
    "In this tweet about {{Topic}}, written by a {{Ideology}}, the entity {{Entity}} exhibits the moral role {MORAL_ROLE}, defined as: {MORAL_ROLE_DEFINITION}",
    "This tweet about {{Topic}} by a {{Ideology}} shows the entity {{Entity}} demonstrating the moral role {MORAL_ROLE}, described as: {MORAL_ROLE_DEFINITION}",
    "The entity {{Entity}} in this tweet about {{Topic}} from a {{Ideology}} displays the moral role {MORAL_ROLE}, which is defined as: {MORAL_ROLE_DEFINITION}",
    "In this tweet about {{Topic}} by a {{Ideology}}, {{Entity}} reflects the moral role {MORAL_ROLE}, defined as: {MORAL_ROLE_DEFINITION}",
    "{{Entity}} in this tweet about {{Topic}}, authored by a {{Ideology}}, exemplifies the moral role {MORAL_ROLE}, which is described as: {MORAL_ROLE_DEFINITION}",
    "This tweet on {{Topic}} from a {{Ideology}} portrays {{Entity}} as embodying the moral role {MORAL_ROLE}, defined as: {MORAL_ROLE_DEFINITION}",
    "The entity {{Entity}} in this tweet about {{Topic}}, written by a {{Ideology}}, illustrates the moral role {MORAL_ROLE}, which is defined as: {MORAL_ROLE_DEFINITION}",
    "In this tweet on {{Topic}} by a {{Ideology}}, {{Entity}} shows the moral role {MORAL_ROLE}, defined as: {MORAL_ROLE_DEFINITION}",
    "This tweet, discussing {{Topic}} and authored by a {{Ideology}}, reveals {{Entity}} displaying the moral role {MORAL_ROLE}, defined as: {MORAL_ROLE_DEFINITION}",
    "The tweet about {{Topic}}, written by a {{Ideology}}, features {{Entity}} expressing the moral role {MORAL_ROLE}, described as: {MORAL_ROLE_DEFINITION}"
]

IDS_TO_EXCLUDE = [
    "639490970644574208", 
    "734383328514609152", 
    "672600766025175040", 
    "278938172317130753", 
    "654747457213980672", 
    "335110067760291840", 
    "733328409296789508",
    "743568102781239297",
    "744199467193278464",
    "745018014664392706",
    "626859975525203968",
    "633353359450206208",
    "647114074082381824",
    "649644591382138881",
    "738393245084962816",
    "624678653935374337",
    "745704659856199681",
    "673918700119064576",
    "740626588996411397",
    "746341176769388544",
    "747481932607422468",
    "662670042966847488",
    "593071595230523392",
    "611539529070178304",
    "618859074600456192",
    "349963499578990593",
    "349963637298958336",
    "362959744534724608",
    "370629716966789121",
    "450643204816535553",
    "745687515038769154",
    "453318153406545920",
    "743472279628189700",
    "482213416397185024",
    "486988440182202369",
    "487360833673244672",
    "746807657873313792",
    "523217926120538112",
    "536928881199312896",
    "646420711641321472",
    "652215162309603328",
    "652539760074969089",
    "619164384657473536",
    "324882503284428800",
    "686686787138228224",
    "215515769583308802",
    "299243997254262784",
    "686974385501159426",
    "687025771504910336",
    "472430720515072000",
    "494876368682115072",
    "511892892785606656",
    "621061478695759872",
    "621076656875282432",
    "293809181629235200",
    "339516688104042496",
    "349731080049401856",
    "644159017317740544",
    "657648086647480320",
    "738392656053710848",
    "542823659711102976",
    "672593578422587393",
    "745658527646093313",
    "742786277976592385",
    "652511798256631808",
    "743202014985879552"
]