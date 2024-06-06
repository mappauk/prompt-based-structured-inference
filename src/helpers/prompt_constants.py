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

MORAL_FOUNDATION_PROMPT_EXAMPLE_FORMAT = '### Tweet: {Tweet} Q. "The moral foundation expressed in the tweet is {label}." - True or False? A. {answer}'
MORAL_FOUNDATION_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT = '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} Q. "The moral foundation expressed in the tweet is {label}." - True or False? A. {answer}'
MORAL_ROLE_PROMPT_EXAMPLE_FORMAT = '### Tweet: {Tweet} Q. "The moral role of {Entity} expressed in the tweet is {label}." - True or False? A. {answer}'
MORAL_ROLE_PROMPT_WITH_FEATURES_EXAMPLE_FORMAT = '### Tweet: {Tweet} Tweet Author Political Ideology: {Ideology} Topic of Tweet: {Topic} Q. "The moral role of {Entity} expressed in the tweet is {label}." - True or False? A. {answer}'

# Definitions

CARE_HARM_DEFINITON = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others.'
FAIRNESS_CHEATING_DEFINITION = 'Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating.'
AUTHORITY_SUBVERSION_DEFINITION = 'Definition of the moral foundation "AUTHORITY/SUBVERSION": Fulfilling social roles, submitting to authority, respect for social hierarchy/traditions, leadership, prohibiting rebellion against authority.'
PURITY_DEGRADATION_DEFINITION = 'Definition of the moral foundation "PURITY/DEGRADATION": Associations with the sacred and holy, disgust, contamination, religious notions which guide how to live, prohibiting violating the sacred.'
LOYALTY_BETRAYAL_DEFINITION = 'Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group.'

CARE_HARM_ROLES_DEFINITION = ' Definitions of moral roles: Entity target of care/harm: Entity that is harmed by someone/something or entity someone/something is providing/offering care to. Entity providing care: Entity that is providing or offering care or expressing the need for care for someone/something. Entity causing harm: Entity that is harming/hurting or doing something bad to someone/something.'
FAIRNESS_CHEATING_ROLES_DEFINITION = 'Definitions of moral roles: Entity target of fairness/cheating: Entity that someone/something is cheating or entity someone/something is being fair to. Entity ensuring fairness: Entity that is ensuring fairness for someone/something. Entity doing cheating: Entity that is cheating someone/something.'
AUTHORITY_SUBVERSION_ROLES_DEFINITION = 'Definitions of moral roles: Entity justified authority: Entity that is the appropriate authority. Entity justified authority over: Entity that someone/something is the authority over. Entity failing authority: Entity that is not an appropriate authority. Entity failing authority over: Entity that someone/something which is not an appropriate authority is expressing authority over.'
PURITY_DEGRADATION_ROLES_DEFINITION = 'Definitions of moral roles: Entity target of purity/degradation: Entity that someone/something is associating with being pure/sacred or entity someone/something is associating with being contaminated/unsanctified. Entity preserving purity: Entity that is being pure/sacred. Entity causing degradation: Entity that is contaminated/unsanctified.'
LOYALTY_BETRAYAL_ROLES_DEFINITION = 'Definitions of moral roles: Entity target of loyalty/betrayal: Entity that someone/something is being loyal to or entity someone/something is betraying. Entity being loyal: Entity that is being loyal to someone/something. Entity doing betrayal: Entity that is betrayings someone/something.'

TARGET_CARE_HARM_ROLE_DEFINITION = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others. Definition of the moral role "Target of care/harm": Entity that is harmed by someone/something or entity someone/something is providing/offering care to.'
ENTITY_PROVIDING_CARE_ROLE_DEFINITION = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others. Definition of the moral role "Entity providing care": Entity that is providing or offering care or expressing the need for care for someone/something.'
ENTITY_CAUSING_HARM_ROLE_DEFINITION = 'Definition of the moral foundation "CARE/HARM": Care for others, generosity, compassion, ability to feel pain of others, sensitivity to suffering of others, prohibiting actions that harm others. Definition of the moral role "Entity causing harm": Entity that is harming/hurting or doing something bad to someone/something.'

TARGET_FAIRNESS_CHEATING_ROLE_DEFINITION = 'Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. Definition of the moral role "Target of fairness/cheating":  Entity that someone/something is cheating or entity someone/something is being fair to.'
ENTITY_ENSURING_FAIRNESS_ROLE_DEFINITION = 'Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. Definition of the moral role "Entity ensuring fairness": Entity that is ensuring fairness for someone/something.'
ENTITY_DOING_CHEATING_ROLE_DEFINITION = 'Definition of the moral foundation "FAIRNESS/CHEATING": Demand for Fairness, rights, equality, justice, reciprocity, reciprocal altruism, autonomy, proportionality and violation of these. Also, prohibiting cheating. Definition of the moral role "Entity doing cheating": Entity that is cheating someone/something.'

TARGET_LOYALTY_BETRAYAL_ROLE_DEFINITION = 'Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. Definition of the moral role "Target of loyalty/betrayal": Entity that someone/something is being loyal to or entity someone/something is betraying.'
ENTITY_BEING_LOYAL_ROLE_DEFINITION = 'Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. Definition of the moral role "Entity being loyal": Entity that is being loyal to someone/something.'
ENTITY_DOING_BETRAYAL_ROLE_DEFINITION = 'Definition of the moral foundation "LOYALTY/BETRAYAL": Group affiliation and solidarity, virtues of patriotism, self-sacrifice for the group, prohibiting betrayal of one’s group. Definition of the moral role "Entity doing betrayal": Entity that is betrayings someone/something.'

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

# Moral foundation examples

# care/harm examples

CARE_HARM_POSITIVE_EXAMPLES = [
    '### Tweet: Recent actions in Indiana and Arkansas made clear that Congress must act to protect #LGBT Americans from discrimination Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True',
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True',
    '### Tweet: How can a 2 min vote become an 8 min vote? When you need to work for 6 mins to keep discriminating vs #LGBT. Watch: Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True',
    '### Tweet: Days after @AmerMedicalAssn declared gun violence a public health crisis @AmerAcadPeds calls for end to gun violence Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True',
    '### Tweet: .@RepRobinKellyand  I wrote an op-ed calling for Congress to keep guns out of the hands of dangerous people\u2013read here:  Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True'
]

CARE_HARM_NEGATIVE_EXAMPLES = [
    '### Tweet: Today’s decision by #SCOTUSs is huge victory for justice and equality for the #LGBT community and our nation Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False',
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False',
    '### Tweet: I am pleased to vote to repeal #Obamacare. It has caused job loss  higher costs  and less patient choice Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False',
    '### Tweet: In 2008 Hillary described herself as a  pro-gun churchgoer.  https://t.co/PirtD0BBct Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False',
    '### Tweet: Today we stand united against bullying and  show our support for #LGBT youth. #SpiritDay @GLAAD  Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False'
]

# fairness/cheating examples

FAIRNESS_CHEATING_POSITIVE_EXAMPLES = [
    '### Tweet: Today’s decision by #SCOTUSs is huge victory for justice and equality for the #LGBT community and our nation Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True',
    '### Tweet: Races don\'t fall in love  genders don\'t fall in love--people fall in love. #SCOTUSMarriage Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True',
    '### Tweet: #Medicare and  #Medicaid have helped kids  seniors and  others get quality #healthcare for 50 yrs. Let\'s keep them strong 4 NM! #KeepingUSHealthy Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True',
    '### Tweet: Cosponsored a bill allowing #military spouses to purchase handguns where their partner is stationed. #2ndAmendment Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True',
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood  Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True'
]

FAIRNESS_CHEATING_NEGATIVE_EXAMPLES = [
    '### Tweet: At @ChiUrbanLeague today calling for Congressional action on gun violence. It\'s past time to act. #Enough Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False',
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False',
    '### Tweet: I joined other senators to request an investigation into Planned Parenthood.  This and more in the Enzi Insider. Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False',
    '### Tweet: RT @RepBobbyRush: .@SpeakerRyan failed Americans\u2013he and  @HouseGOP left town w/o protecting them from suspected terrorists #NoBillNoBreak Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False',
    '### Tweet: RT @RepublicanStudy: #RSC Chair @RepBillFlores:  I believe that marriage is a sacred institution  which must be preserved and protected.  h\u2026  Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False'
]

# authority/subversion examples

AUTHORITY_SUBVERSION_POSITIVE_EXAMPLES = [
    '### Tweet: At @ChiUrbanLeague today calling for Congressional action on gun violence. It\'s past time to act. #Enough Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True',
    '### Tweet: Simply put  the President\'s health care law is the WRONG prescription for America!  #SCOTUS Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True',
    '### Tweet: I am pleased to vote to repeal #Obamacare. It has caused job loss  higher costs  and less patient choice Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True',
    '### Tweet: Hard to fathom  or excuse  the Senate GOP\'s lack of courage on sensible steps on gun safety  OVERWHELMINGLY backed by the people. #Enough Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True',
    '### Tweet: RT @RepBobbyRush: .@SpeakerRyan failed Americans\u2013he and  @HouseGOP left town w/o protecting them from suspected terrorists #NoBillNoBreak Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True'
]

AUTHORITY_SUBVERSION_NEGATIVE_EXAMPLES = [
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling sick message on immigration http://t.co/OOTpD9zmh5  Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False',
    '### Tweet: More on the sick trafficking of baby parts by Planned Parenthood and others. #PP #DefundPP #prolife https://t.co/tJvpNYp5zb Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False',
    '### Tweet: #Medicare and  #Medicaid have helped kids  seniors and  others get quality #healthcare for 50 yrs. Let\'s keep them strong 4 NM! #KeepingUSHealthy Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False',
    '### Tweet: How can a 2 min vote become an 8 min vote? When you need to work for 6 mins to keep discriminating vs #LGBT. Watch: Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False',
    '### Tweet: Races don\'t fall in love  genders don\'t fall in love--people fall in love. #SCOTUSMarriage  Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False'
]

# purity/degredation examples

PURITY_DEGRADATION_POSITIVE_EXAMPLES = [
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling sick message on immigration http://t.co/OOTpD9zmh5 Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True',
    '### Tweet: .@VP:  We will win simply on the decency of what we\u2019re fighting for.\u201d #ImmigrationReform #KeepFamiliesTogether http://t.co/0F1bdmisTd Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True',
    '### Tweet: More on the sick trafficking of baby parts by Planned Parenthood and others. #PP #DefundPP #prolife https://t.co/tJvpNYp5zb Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True',
    '### Tweet: In 2008 Hillary described herself as a  pro-gun churchgoer.  https://t.co/PirtD0BBct Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True',
    '### Tweet: RT @RepublicanStudy: #RSC Chair @RepBillFlores:  I believe that marriage is a sacred institution  which must be preserved and protected.  h\u2026  Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True'
]

PURITY_DEGRADATION_NEGATIVE_EXAMPLES = [
    '### Tweet: Sit or stand but we cannot be silent for victims of gun violence - we need to take action. #NoBillNoBreak Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False',
    '### Tweet: Races don\'t fall in love  genders don\'t fall in love--people fall in love. #SCOTUSMarriage Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False',
    '### Tweet: #Medicare and  #Medicaid have helped kids  seniors and  others get quality #healthcare for 50 yrs. Let\'s keep them strong 4 NM! #KeepingUSHealthy Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False',
    '### Tweet: How can a 2 min vote become an 8 min vote? When you need to work for 6 mins to keep discriminating vs #LGBT. Watch: Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False',
    '### Tweet: Simply put  the President\'s health care law is the WRONG prescription for America!  #SCOTUS Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False'
]

# loyalty/betrayal examples

LOYALTY_BETRAYAL_POSITIVE_EXAMPLES = [
    '### Tweet: Sit or stand but we cannot be silent for victims of gun violence - we need to take action. #NoBillNoBreak Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True',
    '### Tweet: American tax dollars must not be used to aid and abet any dictatorial regime that stands with terrorists! #NoAid2Egypt Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True',
    '### Tweet: Today we stand united against bullying and  show our support for #LGBT youth. #SpiritDay @GLAAD Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True',
    '### Tweet: RT @Jorge_Elorza: Thank you to @SenJackReed @RICAGV1 @MomsDemand and all who came out to #WearOrange today to address gun violence. Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True',
    '### Tweet: I joined other senators to request an investigation into Planned Parenthood.  This and more in the Enzi Insider. Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True'
]

LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES = [
    '### Tweet: Recent actions in Indiana and Arkansas made clear that Congress must act to protect #LGBT Americans from discrimination Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False',
    '### Tweet: More on the sick trafficking of baby parts by Planned Parenthood and others. #PP #DefundPP #prolife https://t.co/tJvpNYp5zb Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False',
    '### Tweet: #Medicare and  #Medicaid have helped kids  seniors and  others get quality #healthcare for 50 yrs. Let\'s keep them strong 4 NM! #KeepingUSHealthy Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False',
    '### Tweet: How can a 2 min vote become an 8 min vote? When you need to work for 6 mins to keep discriminating vs #LGBT. Watch: Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False',
    '### Tweet: Races don\'t fall in love  genders don\'t fall in love--people fall in love. #SCOTUSMarriage Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False'
]

# Entity Role examples

## care/harm role examples

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral role of young adults in the tweet is: Target of care/harm." - True or False? A. True',
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of health care providers and patients in need of home health services in the tweet is: Target of care/harm." - True or False? A. True',
    '### Tweet: RT @RepTomReed: Our patient-centered health care plan lays out a #BetterWay to ensure that Americans have access to affordable and high-qua\u2026 Q. "The moral role of Americans in the tweet is: Target of care/harm." - True or False? A. True'
]

TARGET_CARE_HARM_NEGATIVE_EXAMPLES = [
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral role of Georgia in the tweet is: Target of care/harm." - True or False? A. False',
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of bill in the tweet is: Target of care/harm." - True or False? A. False',
    '### Tweet: RT @RepTomReed: Our patient-centered health care plan lays out a #BetterWay to ensure that Americans have access to affordable and high-qua\u2026 Q. "The moral role of @RepTomReed in the tweet is: Target of care/harm." - True or False? A. False'
]

ENTITY_CAUSING_HARM_POSITIVE_EXAMPLES = [
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral role of repeal in the tweet is: Entity causing harm." - True or False? A. True',
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of unecessary and duplicative burdens in the tweet is: Entity causing harm." - True or False? A. True',
]

ENTITY_CAUSING_HARM_NEGATIVE_EXAMPLES = [
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral role of repeal in the tweet is: Entity causing harm." - True or False? A. False',
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of common-sense bill in the tweet is: Entity causing harm." - True or False? A. False',
]

ENTITY_PROVIDING_CARE_POSITIVE_EXAMPLES = [
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of common-sense bill in the tweet is: Entity providing care." - True or False? A. True',
    '### Tweet: RT @RepTomReed: Our patient-centered health care plan lays out a #BetterWay to ensure that Americans have access to affordable and high-qua\u2026 Q. "The moral role of Our patient-centered health care plan in the tweet is: Entity providing care." - True or False? A. True',
]

ENTITY_PROVIDING_CARE_NEGATIVE_EXAMPLES = [
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of health care providers in the tweet is: Entity providing care." - True or False? A. True',
    '### Tweet: RT @RepTomReed: Our patient-centered health care plan lays out a #BetterWay to ensure that Americans have access to affordable and high-qua\u2026 Q. "The moral role of @RepTomReed in the tweet is: Entity providing care." - True or False? A. True',
]

## fairness/cheating role examples 

TARGET_FAIRNESS_CHEATING_POSITIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of Planned Parenthood in the tweet is: Target of fairness/cheating." - True or False? A. True',
    '### Tweet: We must ensure all #LGBT Americans fell feel safe in school  at work  and out in the community. Q. "The moral role of #LGBT Americans in the tweet is: Target of fairness/cheating." - True or False? A. True',
    '### Tweet: RT @RepDLamborn: In Colorado  #Obamacare has raised premiums 13.4%. Our health deserves a #BetterWay Q. "The moral role of Colorado in the tweet is: Target of fairness/cheating." - True or False? A. True',
]

TARGET_FAIRNESS_CHEATING_NEGATIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of @RepCummings in the tweet is: Target of fairness/cheating." - True or False? A. False',
    '### Tweet: We must ensure all #LGBT Americans fell feel safe in school  at work  and out in the community. Q. "The moral role of We in the tweet is: Target of fairness/cheating." - True or False? A. False',
    '### Tweet: RT @RepDLamborn: In Colorado  #Obamacare has raised premiums 13.4%. Our health deserves a #BetterWay Q. "The moral role of #Obamacare in the tweet is: Target of fairness/cheating." - True or False? A. False',
]

ENTITY_ENSURING_FAIRNESS_POSITIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of .@RepCummings and  @repjohnconyers in the tweet is: Entity ensuring fairness." - True or False? A. True',
    '### Tweet: We must ensure all #LGBT Americans fell feel safe in school  at work  and out in the community. Q. "The moral role of We in the tweet is: Entity ensuring fairness." - True or False? A. True',
]

ENTITY_ENSURING_FAIRNESS_NEGATIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of Planned Parenthood in the tweet is: Entity ensuring fairness." - True or False? A. False',
    '### Tweet: We must ensure all #LGBT Americans fell feel safe in school  at work  and out in the community. Q. "The moral role of #LGBT Americans in the tweet is: Entity ensuring fairness." - True or False? A. False',
]

ENTITY_DOING_CHEATING_POSITIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of one-sided  investigations in the tweet is: Entity doing cheating." - True or False? A. True',
    '### Tweet: RT @RepDLamborn: In Colorado  #Obamacare has raised premiums 13.4%. Our health deserves a #BetterWay Q. "The moral role of #Obamacare in the tweet is: Entity doing cheating." - True or False? A. True',
]

ENTITY_DOING_CHEATING_NEGATIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of Planned Parenthood in the tweet is: Entity doing cheating." - True or False? A. False',
    '### Tweet: RT @RepDLamborn: In Colorado  #Obamacare has raised premiums 13.4%. Our health deserves a #BetterWay Q. "The moral role of @RepDLamborn in the tweet is: Entity doing cheating." - True or False? A. False',
]

## loyalty/betrayal role examples

TARGET_LOYALTY_BETRAYAL_POSITIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of LGBT youth in the tweet is: Target of loyalty/betrayal." - True or False? A. True',
    '### Tweet: I commend @Delta for their statement supporting the humane reforms made by President Obama to our immigration system. Q. "The moral role of President Obama in the tweet is: Target of loyalty/betrayal." - True or False? A. True',
    '### Tweet: At today\'s Foreign Relations hearing: my thoughts on standing strong with Israel and  protecting US from ISIL fighters Q. "The moral role of Israel in the tweet is: Target of loyalty/betrayal." - True or False? A. True',
]

TARGET_LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of My staff in the tweet is: Target of loyalty/betrayal." - True or False? A. False',
    '### Tweet: I commend @Delta for their statement supporting the humane reforms made by President Obama to our immigration system. Q. "The moral role of @Delta in the tweet is: Target of loyalty/betrayal." - True or False? A. False',
    '### Tweet: At today\'s Foreign Relations hearing: my thoughts on standing strong with Israel and  protecting US from ISIL fighters Q. "The moral role of ISIL Fighters in the tweet is: Target of loyalty/betrayal." - True or False? A. False',
]

ENTITY_BEING_LOYAL_POSITIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of My staff in the tweet is: Entity being loyal." - True or False? A. True',
    '### Tweet: I commend @Delta for their statement supporting the humane reforms made by President Obama to our immigration system. Q. "The moral role of Delta in the tweet is: Entity being loyal." - True or False? A. True',
]

ENTITY_BEING_LOYAL_NEGATIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of #SpiritDay in the tweet is: Entity being loyal." - True or False? A. False',
    '### Tweet: I commend @Delta for their statement supporting the humane reforms made by President Obama to our immigration system. Q. "The moral role of President Obama in the tweet is: Entity being loyal." - True or False? A. False',
]

ENTITY_DOING_BETRAYAL_POSITIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of bullying in the tweet is: Entity doing betrayal." - True or False? A. True',
    '### Tweet: At today\'s Foreign Relations hearing: my thoughts on standing strong with Israel and  protecting US from ISIL fighters Q. "The moral role of ISIL Fighters in the tweet is: Entity doing betrayal." - True or False? A. True',
]

ENTITY_DOING_BETRAYAL_NEGATIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of My staff in the tweet is: Entity doing betrayal." - True or False? A. False',
    '### Tweet: At today\'s Foreign Relations hearing: my thoughts on standing strong with Israel and  protecting US from ISIL fighters Q. "The moral role of Israel in the tweet is: Entity doing betrayal." - True or False? A. False',
]

## authority/subversion role examples

FAILING_AUTHORITY_POSITIVE_EXAMPLES = [
    '### Tweet: At 10AM I will speak on the House Floor about Senate\u2019s failure yesterday to pass common sense gun safety legislation. Q. "The moral role of Senate in the tweet is: Failing authority." - True or False? A. True',
    '### Tweet: President Obama never respected #2ndAmendent right or what it means for lawful gun owners in #Wyoming and America. Q. "The moral role of President Obama in the tweet is: Failing authority." - True or False? A. True',
]

FAILING_AUTHORITY_NEGATIVE_EXAMPLES = [
    '### Tweet: At 10AM I will speak on the House Floor about Senate\u2019s failure yesterday to pass common sense gun safety legislation. Q. "The moral role of gun safety legislation in the tweet is: Failing authority." - True or False? A. False',
    '### Tweet: President Obama never respected #2ndAmendent right or what it means for lawful gun owners in #Wyoming and America. Q. "The moral role of lawful gun owners in the tweet is: Failing authority." - True or False? A. False',
]

FAILING_AUTHORITY_OVER_POSITIVE_EXAMPLES = [
    '### Tweet: At 10AM I will speak on the House Floor about Senate\u2019s failure yesterday to pass common sense gun safety legislation. Q. "The moral role of I in the tweet is: Failing authority over." - True or False? A. True',
    '### Tweet: President Obama never respected #2ndAmendent right or what it means for lawful gun owners in #Wyoming and America. Q. "The moral role of lawful gun owners in the tweet is: Failing authority over." - True or False? A. True',
]

FAILING_AUTHORITY_OVER_NEGATIVE_EXAMPLES = [
    '### Tweet: At 10AM I will speak on the House Floor about Senate\u2019s failure yesterday to pass common sense gun safety legislation. Q. "The moral role of Senate in the tweet is: Failing authority over." - True or False? A. False',
    '### Tweet: President Obama never respected #2ndAmendent right or what it means for lawful gun owners in #Wyoming and America. Q. "The moral role of President Obama in the tweet is: Failing authority over." - True or False? A. False',
]

JUSTIFIED_AUTHORITY_POSITIVE_EXAMPLES = [
    '### Tweet: .@SenThadCochran and  I signed amicus brief supporting religious liberty in #SCOTUS case challenging #Obamacare mandate Q. "The moral role of SCOTUS in the tweet is: Justified authority." - True or False? A. True',
    '### Tweet: Tonight  POTUS will give final State of the Union. Hope he\u2019ll offer clear plan to defeat ISIS  keep us safe. What are you hoping to hear? Q. "The moral role of POTUS in the tweet is: Justified authority." - True or False? A. True',
]

JUSTIFIED_AUTHORITY_NEGATIVE_EXAMPLES = [
    '### Tweet: .@SenThadCochran and  I signed amicus brief supporting religious liberty in #SCOTUS case challenging #Obamacare mandate Q. "The moral role of I in the tweet is: Justified authority." - True or False? A. False',
    '### Tweet: Tonight  POTUS will give final State of the Union. Hope he\u2019ll offer clear plan to defeat ISIS  keep us safe. What are you hoping to hear? Q. "The moral role of us in the tweet is: Justified authority." - True or False? A. False',
]

JUSTIFIED_AUTHORITY_OVER_POSITIVE_EXAMPLES = [
    '### Tweet: .@SenThadCochran and  I signed amicus brief supporting religious liberty in #SCOTUS case challenging #Obamacare mandate Q. "The moral role of I in the tweet is: Justified authority over." - True or False? A. True',
    '### Tweet: Tonight  POTUS will give final State of the Union. Hope he\u2019ll offer clear plan to defeat ISIS  keep us safe. What are you hoping to hear? Q. "The moral role of us in the tweet is: Justified authority over." - True or False? A. True',
]

JUSTIFIED_AUTHORITY_OVER_NEGATIVE_EXAMPLES = [
    '### Tweet: .@SenThadCochran and  I signed amicus brief supporting religious liberty in #SCOTUS case challenging #Obamacare mandate Q. "The moral role of SCOTUS in the tweet is: Justified authority over." - True or False? A. False',
    '### Tweet: Tonight  POTUS will give final State of the Union. Hope he\u2019ll offer clear plan to defeat ISIS  keep us safe. What are you hoping to hear? Q. "The moral role of POTUS in the tweet is: Justified authority over." - True or False? A. False',
]

## sanctity/degredation role examples

TARGET_PURITY_DEGREDATION_POSITIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of babies in the tweet is: Target of purity/degredation." - True or False? A. True',
    '### Tweet: Absolutely disgusting: Planned Parenthood caught on tape trying to sell fetal body parts. #prolife http://t.co/zI6fhqaH4T Q. "The moral role of fetal body parts in the tweet is: Target of purity/degradation." - True or False? A. True',
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling  sick message  on immigration http://t.co/OOTpD9zmh5 Q. "The moral role of immigration in the tweet is: Target of purity/degradation." - True or False? A. True',
]

TARGET_PURITY_DEGREDATION_NEGATIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of @PPact in the tweet is: Target of purity/degredation." - True or False? A. False',
    '### Tweet: Absolutely disgusting: Planned Parenthood caught on tape trying to sell fetal body parts. #prolife http://t.co/zI6fhqaH4T Q. "The moral role of Planned Parenthood in the tweet is: Target of purity/degradation." - True or False? A. False',
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling  sick message  on immigration http://t.co/OOTpD9zmh5 Q. "The moral role of Joe Biden in the tweet is: Target of purity/degradation." - True or False? A. False',
]

ENTITY_PRESERVING_PURITY_POSITIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of Congress in the tweet is: Entity preserving purity." - True or False? A. True',
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling  sick message  on immigration http://t.co/OOTpD9zmh5 Q. "The moral role of Joe Biden in the tweet is: Entity preserving purity." - True or False? A. True',
]

ENTITY_PRESERVING_PURITY_NEGATIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of babies in the tweet is: Entity preserving purity." - True or False? A. False',
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling  sick message  on immigration http://t.co/OOTpD9zmh5 Q. "The moral role of Donald Trump in the tweet is: Entity preserving purity." - True or False? A. False',
]

ENTITY_CAUSING_DEGRADATION_POSITIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of @PPact in the tweet is: Entity causing degredation." - True or False? A. True',
    '### Tweet: Absolutely disgusting: Planned Parenthood caught on tape trying to sell fetal body parts. #prolife http://t.co/zI6fhqaH4T Q. "The moral role of Planned Parenthood in the tweet is: Entity causing degredation." - True or False? A. True',
]

ENTITY_CAUSING_DEGRADATION_NEGATIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of Congress in the tweet is: Entity causing degredation." - True or False? A. False',
    '### Tweet: Absolutely disgusting: Planned Parenthood caught on tape trying to sell fetal body parts. #prolife http://t.co/zI6fhqaH4T Q. "The moral role of fetal body parts in the tweet is: Entity causing degredation." - True or False? A. False',
]

MORAL_FOUNDATION_POSITIVE_EXAMPLES_MAP = {
    # frames
    CARE_HARM: CARE_HARM_POSITIVE_EXAMPLES,
    FAIRNESS_CHEATING: FAIRNESS_CHEATING_POSITIVE_EXAMPLES,
    AUTHORITY_SUBVERSION: AUTHORITY_SUBVERSION_POSITIVE_EXAMPLES,
    PURITY_DEGREDATION: PURITY_DEGRADATION_POSITIVE_EXAMPLES,
    LOYALTY_BETRAYAL: LOYALTY_BETRAYAL_POSITIVE_EXAMPLES,
    # roles
    TARGET_CARE_HARM: TARGET_CARE_HARM_POSITIVE_EXAMPLES,
    ENTITY_CAUSING_HARM: ENTITY_CAUSING_HARM_POSITIVE_EXAMPLES,
    ENTITY_PROVIDING_CARE: ENTITY_PROVIDING_CARE_POSITIVE_EXAMPLES,
    TARGET_FAIRNESS_CHEATING: TARGET_FAIRNESS_CHEATING_POSITIVE_EXAMPLES,
    ENTITY_ENSURING_FAIRNESS: ENTITY_ENSURING_FAIRNESS_POSITIVE_EXAMPLES,
    ENTITY_DOING_CHEATING: ENTITY_DOING_CHEATING_POSITIVE_EXAMPLES,
    TARGET_LOYALTY_BETRAYAL: TARGET_LOYALTY_BETRAYAL_POSITIVE_EXAMPLES,
    ENTITY_BEING_LOYAL: ENTITY_BEING_LOYAL_POSITIVE_EXAMPLES,
    ENTITY_DOING_BETRAYAL: ENTITY_DOING_BETRAYAL_POSITIVE_EXAMPLES,
    JUSTIFIED_AUTHORITY: JUSTIFIED_AUTHORITY_POSITIVE_EXAMPLES,
    JUSTIFIED_AUTHORITY_OVER: JUSTIFIED_AUTHORITY_OVER_POSITIVE_EXAMPLES,
    FAILING_AUTHORITY: FAILING_AUTHORITY,
    FAILING_AUTHORITY_OVER: FAILING_AUTHORITY_OVER_POSITIVE_EXAMPLES,
    TARGET_PURITY_DEGREDATION: TARGET_PURITY_DEGREDATION_POSITIVE_EXAMPLES,
    ENTITY_PRESERVING_PURITY: ENTITY_PRESERVING_PURITY_POSITIVE_EXAMPLES,
    ENTITY_CAUSING_DEGRADATION: ENTITY_CAUSING_DEGRADATION_POSITIVE_EXAMPLES
}

MORAL_FOUNDATION_NEGATIVE_EXAMPLES_MAP = {
    # frames
    CARE_HARM: CARE_HARM_NEGATIVE_EXAMPLES,
    FAIRNESS_CHEATING: FAIRNESS_CHEATING_NEGATIVE_EXAMPLES,
    AUTHORITY_SUBVERSION: AUTHORITY_SUBVERSION_NEGATIVE_EXAMPLES,
    PURITY_DEGREDATION: PURITY_DEGRADATION_NEGATIVE_EXAMPLES,
    LOYALTY_BETRAYAL: LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES,
    # roles
    TARGET_CARE_HARM: TARGET_CARE_HARM_NEGATIVE_EXAMPLES,
    ENTITY_CAUSING_HARM: ENTITY_CAUSING_HARM_NEGATIVE_EXAMPLES,
    ENTITY_PROVIDING_CARE: ENTITY_PRESERVING_PURITY_NEGATIVE_EXAMPLES,
    TARGET_FAIRNESS_CHEATING: TARGET_FAIRNESS_CHEATING_NEGATIVE_EXAMPLES,
    ENTITY_ENSURING_FAIRNESS: ENTITY_ENSURING_FAIRNESS_NEGATIVE_EXAMPLES,
    ENTITY_DOING_CHEATING: ENTITY_DOING_CHEATING_NEGATIVE_EXAMPLES,
    TARGET_LOYALTY_BETRAYAL: TARGET_LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES,
    ENTITY_BEING_LOYAL: ENTITY_BEING_LOYAL_NEGATIVE_EXAMPLES,
    ENTITY_DOING_BETRAYAL: ENTITY_DOING_BETRAYAL_NEGATIVE_EXAMPLES,
    JUSTIFIED_AUTHORITY: JUSTIFIED_AUTHORITY_NEGATIVE_EXAMPLES,
    JUSTIFIED_AUTHORITY_OVER: JUSTIFIED_AUTHORITY_OVER_NEGATIVE_EXAMPLES,
    FAILING_AUTHORITY: FAILING_AUTHORITY_NEGATIVE_EXAMPLES,
    FAILING_AUTHORITY_OVER: FAILING_AUTHORITY_OVER_NEGATIVE_EXAMPLES,
    TARGET_PURITY_DEGREDATION: TARGET_PURITY_DEGREDATION_NEGATIVE_EXAMPLES,
    ENTITY_PRESERVING_PURITY: ENTITY_PRESERVING_PURITY_NEGATIVE_EXAMPLES,
    ENTITY_CAUSING_DEGRADATION: ENTITY_CAUSING_DEGRADATION_NEGATIVE_EXAMPLES
}


#MORAL_FOUNDATION_IDENTIFICATION_EXAMPLE_FORMAT = (
#    '### Tweet: {0} Q. "The moral role of {1} in the tweet is: {1}." - True or False? A. True'
#)

CARE_HARM_POSITIVE_EXAMPLES = [
    '### Tweet: Recent actions in Indiana and Arkansas made clear that Congress must act to protect #LGBT Americans from discrimination Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True',
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True',
    '### Tweet: How can a 2 min vote become an 8 min vote? When you need to work for 6 mins to keep discriminating vs #LGBT. Watch: Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True',
    '### Tweet: Days after @AmerMedicalAssn declared gun violence a public health crisis @AmerAcadPeds calls for end to gun violence Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True',
    '### Tweet: .@RepRobinKellyand  I wrote an op-ed calling for Congress to keep guns out of the hands of dangerous people\u2013read here:  Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. True'
]

CARE_HARM_NEGATIVE_EXAMPLES = [
    '### Tweet: Today’s decision by #SCOTUSs is huge victory for justice and equality for the #LGBT community and our nation Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False',
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False',
    '### Tweet: I am pleased to vote to repeal #Obamacare. It has caused job loss  higher costs  and less patient choice Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False',
    '### Tweet: In 2008 Hillary described herself as a  pro-gun churchgoer.  https://t.co/PirtD0BBct Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False',
    '### Tweet: Today we stand united against bullying and  show our support for #LGBT youth. #SpiritDay @GLAAD  Q. "The moral foundation expressed in the tweet is CARE/HARM." - True or False? A. False'
]

# fairness/cheating examples

FAIRNESS_CHEATING_POSITIVE_EXAMPLES = [
    '### Tweet: Today’s decision by #SCOTUSs is huge victory for justice and equality for the #LGBT community and our nation Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True',
    '### Tweet: Races don\'t fall in love  genders don\'t fall in love--people fall in love. #SCOTUSMarriage Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True',
    '### Tweet: #Medicare and  #Medicaid have helped kids  seniors and  others get quality #healthcare for 50 yrs. Let\'s keep them strong 4 NM! #KeepingUSHealthy Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True',
    '### Tweet: Cosponsored a bill allowing #military spouses to purchase handguns where their partner is stationed. #2ndAmendment Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True',
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood  Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. True'
]

FAIRNESS_CHEATING_NEGATIVE_EXAMPLES = [
    '### Tweet: At @ChiUrbanLeague today calling for Congressional action on gun violence. It\'s past time to act. #Enough Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False',
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False',
    '### Tweet: I joined other senators to request an investigation into Planned Parenthood.  This and more in the Enzi Insider. Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False',
    '### Tweet: RT @RepBobbyRush: .@SpeakerRyan failed Americans\u2013he and  @HouseGOP left town w/o protecting them from suspected terrorists #NoBillNoBreak Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False',
    '### Tweet: RT @RepublicanStudy: #RSC Chair @RepBillFlores:  I believe that marriage is a sacred institution  which must be preserved and protected.  h\u2026  Q. "The moral foundation expressed in the tweet is FAIRNESS/CHEATING." - True or False? A. False'
]

# authority/subversion examples

AUTHORITY_SUBVERSION_POSITIVE_EXAMPLES = [
    '### Tweet: At @ChiUrbanLeague today calling for Congressional action on gun violence. It\'s past time to act. #Enough Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True',
    '### Tweet: Simply put  the President\'s health care law is the WRONG prescription for America!  #SCOTUS Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True',
    '### Tweet: I am pleased to vote to repeal #Obamacare. It has caused job loss  higher costs  and less patient choice Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True',
    '### Tweet: Hard to fathom  or excuse  the Senate GOP\'s lack of courage on sensible steps on gun safety  OVERWHELMINGLY backed by the people. #Enough Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True',
    '### Tweet: RT @RepBobbyRush: .@SpeakerRyan failed Americans\u2013he and  @HouseGOP left town w/o protecting them from suspected terrorists #NoBillNoBreak Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. True'
]

AUTHORITY_SUBVERSION_NEGATIVE_EXAMPLES = [
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling sick message on immigration http://t.co/OOTpD9zmh5  Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False',
    '### Tweet: More on the sick trafficking of baby parts by Planned Parenthood and others. #PP #DefundPP #prolife https://t.co/tJvpNYp5zb Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False',
    '### Tweet: #Medicare and  #Medicaid have helped kids  seniors and  others get quality #healthcare for 50 yrs. Let\'s keep them strong 4 NM! #KeepingUSHealthy Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False',
    '### Tweet: How can a 2 min vote become an 8 min vote? When you need to work for 6 mins to keep discriminating vs #LGBT. Watch: Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False',
    '### Tweet: Races don\'t fall in love  genders don\'t fall in love--people fall in love. #SCOTUSMarriage  Q. "The moral foundation expressed in the tweet is AUTHORITY/SUBVERSION." - True or False? A. False'
]

# purity/degredation examples

PURITY_DEGRADATION_POSITIVE_EXAMPLES = [
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling sick message on immigration http://t.co/OOTpD9zmh5 Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True',
    '### Tweet: .@VP:  We will win simply on the decency of what we\u2019re fighting for.\u201d #ImmigrationReform #KeepFamiliesTogether http://t.co/0F1bdmisTd Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True',
    '### Tweet: More on the sick trafficking of baby parts by Planned Parenthood and others. #PP #DefundPP #prolife https://t.co/tJvpNYp5zb Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True',
    '### Tweet: In 2008 Hillary described herself as a  pro-gun churchgoer.  https://t.co/PirtD0BBct Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True',
    '### Tweet: RT @RepublicanStudy: #RSC Chair @RepBillFlores:  I believe that marriage is a sacred institution  which must be preserved and protected.  h\u2026  Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. True'
]

PURITY_DEGRADATION_NEGATIVE_EXAMPLES = [
    '### Tweet: Sit or stand but we cannot be silent for victims of gun violence - we need to take action. #NoBillNoBreak Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False',
    '### Tweet: Races don\'t fall in love  genders don\'t fall in love--people fall in love. #SCOTUSMarriage Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False',
    '### Tweet: #Medicare and  #Medicaid have helped kids  seniors and  others get quality #healthcare for 50 yrs. Let\'s keep them strong 4 NM! #KeepingUSHealthy Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False',
    '### Tweet: How can a 2 min vote become an 8 min vote? When you need to work for 6 mins to keep discriminating vs #LGBT. Watch: Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False',
    '### Tweet: Simply put  the President\'s health care law is the WRONG prescription for America!  #SCOTUS Q. "The moral foundation expressed in the tweet is PURITY/DEGRADATION." - True or False? A. False'
]

# loyalty/betrayal examples

LOYALTY_BETRAYAL_POSITIVE_EXAMPLES = [
    '### Tweet: Sit or stand but we cannot be silent for victims of gun violence - we need to take action. #NoBillNoBreak Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True',
    '### Tweet: American tax dollars must not be used to aid and abet any dictatorial regime that stands with terrorists! #NoAid2Egypt Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True',
    '### Tweet: Today we stand united against bullying and  show our support for #LGBT youth. #SpiritDay @GLAAD Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True',
    '### Tweet: RT @Jorge_Elorza: Thank you to @SenJackReed @RICAGV1 @MomsDemand and all who came out to #WearOrange today to address gun violence. Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True',
    '### Tweet: I joined other senators to request an investigation into Planned Parenthood.  This and more in the Enzi Insider. Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. True'
]

LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES = [
    '### Tweet: Recent actions in Indiana and Arkansas made clear that Congress must act to protect #LGBT Americans from discrimination Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False',
    '### Tweet: More on the sick trafficking of baby parts by Planned Parenthood and others. #PP #DefundPP #prolife https://t.co/tJvpNYp5zb Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False',
    '### Tweet: #Medicare and  #Medicaid have helped kids  seniors and  others get quality #healthcare for 50 yrs. Let\'s keep them strong 4 NM! #KeepingUSHealthy Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False',
    '### Tweet: How can a 2 min vote become an 8 min vote? When you need to work for 6 mins to keep discriminating vs #LGBT. Watch: Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False',
    '### Tweet: Races don\'t fall in love  genders don\'t fall in love--people fall in love. #SCOTUSMarriage Q. "The moral foundation expressed in the tweet is LOYALTY/BETRAYAL." - True or False? A. False'
]

# Entity Role examples

## care/harm role examples

TARGET_CARE_HARM_POSITIVE_EXAMPLES = [
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral role of young adults in the tweet is: Target of care/harm." - True or False? A. True',
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of health care providers and patients in need of home health services in the tweet is: Target of care/harm." - True or False? A. True',
    '### Tweet: RT @RepTomReed: Our patient-centered health care plan lays out a #BetterWay to ensure that Americans have access to affordable and high-qua\u2026 Q. "The moral role of Americans in the tweet is: Target of care/harm." - True or False? A. True'
]

TARGET_CARE_HARM_NEGATIVE_EXAMPLES = [
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral role of Georgia in the tweet is: Target of care/harm." - True or False? A. False',
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of bill in the tweet is: Target of care/harm." - True or False? A. False',
    '### Tweet: RT @RepTomReed: Our patient-centered health care plan lays out a #BetterWay to ensure that Americans have access to affordable and high-qua\u2026 Q. "The moral role of @RepTomReed in the tweet is: Target of care/harm." - True or False? A. False'
]

ENTITY_CAUSING_HARM_POSITIVE_EXAMPLES = [
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral role of repeal in the tweet is: Entity causing harm." - True or False? A. True',
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of unecessary and duplicative burdens in the tweet is: Entity causing harm." - True or False? A. True',
]

ENTITY_CAUSING_HARM_NEGATIVE_EXAMPLES = [
    '### Tweet: In Georgia  repeal would mean that more than 100K young adults would not have coverage through their parents\u2019 healthcare plans. Q. "The moral role of repeal in the tweet is: Entity causing harm." - True or False? A. False',
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of common-sense bill in the tweet is: Entity causing harm." - True or False? A. False',
]

ENTITY_PROVIDING_CARE_POSITIVE_EXAMPLES = [
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of common-sense bill in the tweet is: Entity providing care." - True or False? A. True',
    '### Tweet: RT @RepTomReed: Our patient-centered health care plan lays out a #BetterWay to ensure that Americans have access to affordable and high-qua\u2026 Q. "The moral role of Our patient-centered health care plan in the tweet is: Entity providing care." - True or False? A. True',
]

ENTITY_PROVIDING_CARE_NEGATIVE_EXAMPLES = [
    '### Tweet: This common-sense bill will reduce unnecessary and duplicative burdens on health care providers and patients in need of home health services Q. "The moral role of health care providers in the tweet is: Entity providing care." - True or False? A. True',
    '### Tweet: RT @RepTomReed: Our patient-centered health care plan lays out a #BetterWay to ensure that Americans have access to affordable and high-qua\u2026 Q. "The moral role of @RepTomReed in the tweet is: Entity providing care." - True or False? A. True',
]

## fairness/cheating role examples 

TARGET_FAIRNESS_CHEATING_POSITIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of Planned Parenthood in the tweet is: Target of fairness/cheating." - True or False? A. True',
    '### Tweet: We must ensure all #LGBT Americans fell feel safe in school  at work  and out in the community. Q. "The moral role of #LGBT Americans in the tweet is: Target of fairness/cheating." - True or False? A. True',
    '### Tweet: RT @RepDLamborn: In Colorado  #Obamacare has raised premiums 13.4%. Our health deserves a #BetterWay Q. "The moral role of Colorado in the tweet is: Target of fairness/cheating." - True or False? A. True',
]

TARGET_FAIRNESS_CHEATING_NEGATIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of @RepCummings in the tweet is: Target of fairness/cheating." - True or False? A. False',
    '### Tweet: We must ensure all #LGBT Americans fell feel safe in school  at work  and out in the community. Q. "The moral role of We in the tweet is: Target of fairness/cheating." - True or False? A. False',
    '### Tweet: RT @RepDLamborn: In Colorado  #Obamacare has raised premiums 13.4%. Our health deserves a #BetterWay Q. "The moral role of #Obamacare in the tweet is: Target of fairness/cheating." - True or False? A. False',
]

ENTITY_ENSURING_FAIRNESS_POSITIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of .@RepCummings and  @repjohnconyers in the tweet is: Entity ensuring fairness." - True or False? A. True',
    '### Tweet: We must ensure all #LGBT Americans fell feel safe in school  at work  and out in the community. Q. "The moral role of We in the tweet is: Entity ensuring fairness." - True or False? A. True',
]

ENTITY_ENSURING_FAIRNESS_NEGATIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of Planned Parenthood in the tweet is: Entity ensuring fairness." - True or False? A. False',
    '### Tweet: We must ensure all #LGBT Americans fell feel safe in school  at work  and out in the community. Q. "The moral role of #LGBT Americans in the tweet is: Entity ensuring fairness." - True or False? A. False',
]

ENTITY_DOING_CHEATING_POSITIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of one-sided  investigations in the tweet is: Entity doing cheating." - True or False? A. True',
    '### Tweet: RT @RepDLamborn: In Colorado  #Obamacare has raised premiums 13.4%. Our health deserves a #BetterWay Q. "The moral role of #Obamacare in the tweet is: Entity doing cheating." - True or False? A. True',
]

ENTITY_DOING_CHEATING_NEGATIVE_EXAMPLES = [
    '### Tweet: RT @OversightDems: .@RepCummings and  @repjohnconyers call on Chrm to suspend  one-sided  investigations of Planned Parenthood Q. "The moral role of Planned Parenthood in the tweet is: Entity doing cheating." - True or False? A. False',
    '### Tweet: RT @RepDLamborn: In Colorado  #Obamacare has raised premiums 13.4%. Our health deserves a #BetterWay Q. "The moral role of @RepDLamborn in the tweet is: Entity doing cheating." - True or False? A. False',
]

## loyalty/betrayal role examples

TARGET_LOYALTY_BETRAYAL_POSITIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of LGBT youth in the tweet is: Target of loyalty/betrayal." - True or False? A. True',
    '### Tweet: I commend @Delta for their statement supporting the humane reforms made by President Obama to our immigration system. Q. "The moral role of President Obama in the tweet is: Target of loyalty/betrayal." - True or False? A. True',
    '### Tweet: At today\'s Foreign Relations hearing: my thoughts on standing strong with Israel and  protecting US from ISIL fighters Q. "The moral role of Israel in the tweet is: Target of loyalty/betrayal." - True or False? A. True',
]

TARGET_LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of My staff in the tweet is: Target of loyalty/betrayal." - True or False? A. False',
    '### Tweet: I commend @Delta for their statement supporting the humane reforms made by President Obama to our immigration system. Q. "The moral role of @Delta in the tweet is: Target of loyalty/betrayal." - True or False? A. False',
    '### Tweet: At today\'s Foreign Relations hearing: my thoughts on standing strong with Israel and  protecting US from ISIL fighters Q. "The moral role of ISIL Fighters in the tweet is: Target of loyalty/betrayal." - True or False? A. False',
]

ENTITY_BEING_LOYAL_POSITIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of My staff in the tweet is: Entity being loyal." - True or False? A. True',
    '### Tweet: I commend @Delta for their statement supporting the humane reforms made by President Obama to our immigration system. Q. "The moral role of Delta in the tweet is: Entity being loyal." - True or False? A. True',
]

ENTITY_BEING_LOYAL_NEGATIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of #SpiritDay in the tweet is: Entity being loyal." - True or False? A. False',
    '### Tweet: I commend @Delta for their statement supporting the humane reforms made by President Obama to our immigration system. Q. "The moral role of President Obama in the tweet is: Entity being loyal." - True or False? A. False',
]

ENTITY_DOING_BETRAYAL_POSITIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of bullying in the tweet is: Entity doing betrayal." - True or False? A. True',
    '### Tweet: At today\'s Foreign Relations hearing: my thoughts on standing strong with Israel and  protecting US from ISIL fighters Q. "The moral role of ISIL Fighters in the tweet is: Entity doing betrayal." - True or False? A. True',
]

ENTITY_DOING_BETRAYAL_NEGATIVE_EXAMPLES = [
    '### Tweet: My staff celebrated #SpiritDay by wearing purple to stand in support of #LGBT youth and  to take a stand against bullying Q. "The moral role of My staff in the tweet is: Entity doing betrayal." - True or False? A. False',
    '### Tweet: At today\'s Foreign Relations hearing: my thoughts on standing strong with Israel and  protecting US from ISIL fighters Q. "The moral role of Israel in the tweet is: Entity doing betrayal." - True or False? A. False',
]

## authority/subversion role examples

FAILING_AUTHORITY_POSITIVE_EXAMPLES = [
    '### Tweet: At 10AM I will speak on the House Floor about Senate\u2019s failure yesterday to pass common sense gun safety legislation. Q. "The moral role of Senate in the tweet is: Failing authority." - True or False? A. True',
    '### Tweet: President Obama never respected #2ndAmendent right or what it means for lawful gun owners in #Wyoming and America. Q. "The moral role of President Obama in the tweet is: Failing authority." - True or False? A. True',
]

FAILING_AUTHORITY_NEGATIVE_EXAMPLES = [
    '### Tweet: At 10AM I will speak on the House Floor about Senate\u2019s failure yesterday to pass common sense gun safety legislation. Q. "The moral role of gun safety legislation in the tweet is: Failing authority." - True or False? A. False',
    '### Tweet: President Obama never respected #2ndAmendent right or what it means for lawful gun owners in #Wyoming and America. Q. "The moral role of lawful gun owners in the tweet is: Failing authority." - True or False? A. False',
]

FAILING_AUTHORITY_OVER_POSITIVE_EXAMPLES = [
    '### Tweet: At 10AM I will speak on the House Floor about Senate\u2019s failure yesterday to pass common sense gun safety legislation. Q. "The moral role of I in the tweet is: Failing authority over." - True or False? A. True',
    '### Tweet: President Obama never respected #2ndAmendent right or what it means for lawful gun owners in #Wyoming and America. Q. "The moral role of lawful gun owners in the tweet is: Failing authority over." - True or False? A. True',
]

FAILING_AUTHORITY_OVER_NEGATIVE_EXAMPLES = [
    '### Tweet: At 10AM I will speak on the House Floor about Senate\u2019s failure yesterday to pass common sense gun safety legislation. Q. "The moral role of Senate in the tweet is: Failing authority over." - True or False? A. False',
    '### Tweet: President Obama never respected #2ndAmendent right or what it means for lawful gun owners in #Wyoming and America. Q. "The moral role of President Obama in the tweet is: Failing authority over." - True or False? A. False',
]

JUSTIFIED_AUTHORITY_POSITIVE_EXAMPLES = [
    '### Tweet: .@SenThadCochran and  I signed amicus brief supporting religious liberty in #SCOTUS case challenging #Obamacare mandate Q. "The moral role of SCOTUS in the tweet is: Justified authority." - True or False? A. True',
    '### Tweet: Tonight  POTUS will give final State of the Union. Hope he\u2019ll offer clear plan to defeat ISIS  keep us safe. What are you hoping to hear? Q. "The moral role of POTUS in the tweet is: Justified authority." - True or False? A. True',
]

JUSTIFIED_AUTHORITY_NEGATIVE_EXAMPLES = [
    '### Tweet: .@SenThadCochran and  I signed amicus brief supporting religious liberty in #SCOTUS case challenging #Obamacare mandate Q. "The moral role of I in the tweet is: Justified authority." - True or False? A. False',
    '### Tweet: Tonight  POTUS will give final State of the Union. Hope he\u2019ll offer clear plan to defeat ISIS  keep us safe. What are you hoping to hear? Q. "The moral role of us in the tweet is: Justified authority." - True or False? A. False',
]

JUSTIFIED_AUTHORITY_OVER_POSITIVE_EXAMPLES = [
    '### Tweet: .@SenThadCochran and  I signed amicus brief supporting religious liberty in #SCOTUS case challenging #Obamacare mandate Q. "The moral role of I in the tweet is: Justified authority over." - True or False? A. True',
    '### Tweet: Tonight  POTUS will give final State of the Union. Hope he\u2019ll offer clear plan to defeat ISIS  keep us safe. What are you hoping to hear? Q. "The moral role of us in the tweet is: Justified authority over." - True or False? A. True',
]

JUSTIFIED_AUTHORITY_OVER_NEGATIVE_EXAMPLES = [
    '### Tweet: .@SenThadCochran and  I signed amicus brief supporting religious liberty in #SCOTUS case challenging #Obamacare mandate Q. "The moral role of SCOTUS in the tweet is: Justified authority over." - True or False? A. False',
    '### Tweet: Tonight  POTUS will give final State of the Union. Hope he\u2019ll offer clear plan to defeat ISIS  keep us safe. What are you hoping to hear? Q. "The moral role of POTUS in the tweet is: Justified authority over." - True or False? A. False',
]

## sanctity/degredation role examples

TARGET_PURITY_DEGREDATION_POSITIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of babies in the tweet is: Target of purity/degredation." - True or False? A. True',
    '### Tweet: Absolutely disgusting: Planned Parenthood caught on tape trying to sell fetal body parts. #prolife http://t.co/zI6fhqaH4T Q. "The moral role of fetal body parts in the tweet is: Target of purity/degradation." - True or False? A. True',
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling  sick message  on immigration http://t.co/OOTpD9zmh5 Q. "The moral role of immigration in the tweet is: Target of purity/degradation." - True or False? A. True',
]

TARGET_PURITY_DEGREDATION_NEGATIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of @PPact in the tweet is: Target of purity/degredation." - True or False? A. False',
    '### Tweet: Absolutely disgusting: Planned Parenthood caught on tape trying to sell fetal body parts. #prolife http://t.co/zI6fhqaH4T Q. "The moral role of Planned Parenthood in the tweet is: Target of purity/degradation." - True or False? A. False',
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling  sick message  on immigration http://t.co/OOTpD9zmh5 Q. "The moral role of Joe Biden in the tweet is: Target of purity/degradation." - True or False? A. False',
]

ENTITY_PRESERVING_PURITY_POSITIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of Congress in the tweet is: Entity preserving purity." - True or False? A. True',
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling  sick message  on immigration http://t.co/OOTpD9zmh5 Q. "The moral role of Joe Biden in the tweet is: Entity preserving purity." - True or False? A. True',
]

ENTITY_PRESERVING_PURITY_NEGATIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of babies in the tweet is: Entity preserving purity." - True or False? A. False',
    '### Tweet: RT @LatinoVoices: Joe Biden slams Donald Trump for selling  sick message  on immigration http://t.co/OOTpD9zmh5 Q. "The moral role of Donald Trump in the tweet is: Entity preserving purity." - True or False? A. False',
]

ENTITY_CAUSING_DEGRADATION_POSITIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of @PPact in the tweet is: Entity causing degredation." - True or False? A. True',
    '### Tweet: Absolutely disgusting: Planned Parenthood caught on tape trying to sell fetal body parts. #prolife http://t.co/zI6fhqaH4T Q. "The moral role of Planned Parenthood in the tweet is: Entity causing degredation." - True or False? A. True',
]

ENTITY_CAUSING_DEGRADATION_NEGATIVE_EXAMPLES = [
    '### Tweet: Allegations @PPact is possibly selling the body parts of the babies it has aborted is sickening. Congress should investigate and  defund them. Q. "The moral role of Congress in the tweet is: Entity causing degredation." - True or False? A. False',
    '### Tweet: Absolutely disgusting: Planned Parenthood caught on tape trying to sell fetal body parts. #prolife http://t.co/zI6fhqaH4T Q. "The moral role of fetal body parts in the tweet is: Entity causing degredation." - True or False? A. False',
]

MORAL_FOUNDATION_POSITIVE_EXAMPLES_MAP = {
    # frames
    CARE_HARM: CARE_HARM_POSITIVE_EXAMPLES,
    FAIRNESS_CHEATING: FAIRNESS_CHEATING_POSITIVE_EXAMPLES,
    AUTHORITY_SUBVERSION: AUTHORITY_SUBVERSION_POSITIVE_EXAMPLES,
    PURITY_DEGREDATION: PURITY_DEGRADATION_POSITIVE_EXAMPLES,
    LOYALTY_BETRAYAL: LOYALTY_BETRAYAL_POSITIVE_EXAMPLES,
    # roles
    TARGET_CARE_HARM: TARGET_CARE_HARM_POSITIVE_EXAMPLES,
    ENTITY_CAUSING_HARM: ENTITY_CAUSING_HARM_POSITIVE_EXAMPLES,
    ENTITY_PROVIDING_CARE: ENTITY_PROVIDING_CARE_POSITIVE_EXAMPLES,
    TARGET_FAIRNESS_CHEATING: TARGET_FAIRNESS_CHEATING_POSITIVE_EXAMPLES,
    ENTITY_ENSURING_FAIRNESS: ENTITY_ENSURING_FAIRNESS_POSITIVE_EXAMPLES,
    ENTITY_DOING_CHEATING: ENTITY_DOING_CHEATING_POSITIVE_EXAMPLES,
    TARGET_LOYALTY_BETRAYAL: TARGET_LOYALTY_BETRAYAL_POSITIVE_EXAMPLES,
    ENTITY_BEING_LOYAL: ENTITY_BEING_LOYAL_POSITIVE_EXAMPLES,
    ENTITY_DOING_BETRAYAL: ENTITY_DOING_BETRAYAL_POSITIVE_EXAMPLES,
    JUSTIFIED_AUTHORITY: JUSTIFIED_AUTHORITY_POSITIVE_EXAMPLES,
    JUSTIFIED_AUTHORITY_OVER: JUSTIFIED_AUTHORITY_OVER_POSITIVE_EXAMPLES,
    FAILING_AUTHORITY: FAILING_AUTHORITY,
    FAILING_AUTHORITY_OVER: FAILING_AUTHORITY_OVER_POSITIVE_EXAMPLES,
    TARGET_PURITY_DEGREDATION: TARGET_PURITY_DEGREDATION_POSITIVE_EXAMPLES,
    ENTITY_PRESERVING_PURITY: ENTITY_PRESERVING_PURITY_POSITIVE_EXAMPLES,
    ENTITY_CAUSING_DEGRADATION: ENTITY_CAUSING_DEGRADATION_POSITIVE_EXAMPLES
}

MORAL_FOUNDATION_NEGATIVE_EXAMPLES_MAP = {
    # frames
    CARE_HARM: CARE_HARM_NEGATIVE_EXAMPLES,
    FAIRNESS_CHEATING: FAIRNESS_CHEATING_NEGATIVE_EXAMPLES,
    AUTHORITY_SUBVERSION: AUTHORITY_SUBVERSION_NEGATIVE_EXAMPLES,
    PURITY_DEGREDATION: PURITY_DEGRADATION_NEGATIVE_EXAMPLES,
    LOYALTY_BETRAYAL: LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES,
    # roles
    TARGET_CARE_HARM: TARGET_CARE_HARM_NEGATIVE_EXAMPLES,
    ENTITY_CAUSING_HARM: ENTITY_CAUSING_HARM_NEGATIVE_EXAMPLES,
    ENTITY_PROVIDING_CARE: ENTITY_PRESERVING_PURITY_NEGATIVE_EXAMPLES,
    TARGET_FAIRNESS_CHEATING: TARGET_FAIRNESS_CHEATING_NEGATIVE_EXAMPLES,
    ENTITY_ENSURING_FAIRNESS: ENTITY_ENSURING_FAIRNESS_NEGATIVE_EXAMPLES,
    ENTITY_DOING_CHEATING: ENTITY_DOING_CHEATING_NEGATIVE_EXAMPLES,
    TARGET_LOYALTY_BETRAYAL: TARGET_LOYALTY_BETRAYAL_NEGATIVE_EXAMPLES,
    ENTITY_BEING_LOYAL: ENTITY_BEING_LOYAL_NEGATIVE_EXAMPLES,
    ENTITY_DOING_BETRAYAL: ENTITY_DOING_BETRAYAL_NEGATIVE_EXAMPLES,
    JUSTIFIED_AUTHORITY: JUSTIFIED_AUTHORITY_NEGATIVE_EXAMPLES,
    JUSTIFIED_AUTHORITY_OVER: JUSTIFIED_AUTHORITY_OVER_NEGATIVE_EXAMPLES,
    FAILING_AUTHORITY: FAILING_AUTHORITY_NEGATIVE_EXAMPLES,
    FAILING_AUTHORITY_OVER: FAILING_AUTHORITY_OVER_NEGATIVE_EXAMPLES,
    TARGET_PURITY_DEGREDATION: TARGET_PURITY_DEGREDATION_NEGATIVE_EXAMPLES,
    ENTITY_PRESERVING_PURITY: ENTITY_PRESERVING_PURITY_NEGATIVE_EXAMPLES,
    ENTITY_CAUSING_DEGRADATION: ENTITY_CAUSING_DEGRADATION_NEGATIVE_EXAMPLES
}

