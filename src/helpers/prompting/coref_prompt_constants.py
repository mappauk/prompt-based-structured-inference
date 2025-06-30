COREF_PROMPT_INSTRUCTIONS_ZERO_SHOT = 'Given two entity mentions and their representative sentences, decide whether the entity mentions refer to the same entity or not.'
COREF_PROMPT_INSTRUCTIONS_FEW_SHOT = 'Given two entity mentions and their representative sentences, decide whether the entity mentions refer to the same entity or not. For Example:'
COREF_PROMPT_INSTRUCTIONS_ZERO_SHOT_NONCOREF = 'Given two entity mentions and their representative sentences, decide whether the entity mentions refer to different entities or not.'
COREF_PROMPT_INSTRUCTIONS_FEW_SHOT_NONCOREF = 'Given two entity mentions and their representative sentences, decide whether the entity mentions refer to different entities or not. For Example:'

COREF_PROMPT_EXAMPLE = '### Entity 1: {entity1} Sentence 1: {sent1} Entity 2: {entity2} Sentence 2: {sent2} Q. {entity1} refers to {entity2}" - true or false? A. {answer}'
COREF_PROMPT_QUESTION = '### Entity 1: {entity1} Sentence 1: {sent1} Entity 2: {entity2} Sentence 2: {sent2} Q. {entity1} refers to {entity2}" - true or false? A. '
COREF_PROMPT_EXAMPLE_NONCOREF = '### Entity 1: {entity1} Sentence 1: {sent1} Entity 2: {entity2} Sentence 2: {sent2} Q. {entity1} does not refer to {entity2}" - true or false? A. {answer}'
COREF_PROMPT_QUESTION_NONCOREF = '### Entity 1: {entity1} Sentence 1: {sent1} Entity 2: {entity2} Sentence 2: {sent2} Q. {entity1} does not refer to {entity2}" - true or false? A. '

GEN_Z_COREF_PARAPHRASE_PROMPT_POSITIVE = 'Write 10 paraphrases of this sentence as a Python list. “The entity mention {entity1} in the first sentence and the entity mention of {entity2} in the second sentence are {label}"'
GEN_Z_COREF_PARAPHRASE_PROMPT_NEGATIVE = 'Write 10 paraphrases of this sentence as a Python list. “The entity mention {entity1} in the first sentence refers to a different entity as the entity mention of {entity2} in the second sentence."'

GEN_Z_COREF_FORMAT = 'Sentence 1: {sent1} Sentence 2: {sent2}'
GEN_Z_COREF_EXAMPLE_FORMAT = '### Generation Description: {0} '
GEN_Z_COREF_INTRO_ZERO_SHOT = 'Given a description of two entity mentions that each belong to a sentence. Generate the sentences that contain these entity mentions.'
GEN_Z_COREF_INTRO_FEW_SHOT = 'Given a description of two entity mentions that each belong to a sentence. Generate the sentences that contain these entity mentions. For Example:'

COREF_CHOICES = ["A", "B"]

COREF_LABEL_TO_CHOICE_INDEX = {
    "coreferent": 0,
    "distinct": 1
}

COREF_LABEL_TO_CHOICE = {
    "coreferent": "A",
    "distinct": "B"
}

SYSTEM_PROMPT_EXAMPLE_LEAD_IN = 'Consider the following examples:\n'

COREF_TF_SYSTEM_PROMPT = '''
Consider the task of coreference resolution, where the goal is to identify whether or not two different entity mentions refer to the same underlying entity. Given two entity mentions and their representative sentences, answer the following true/false question regarding whether the two entity mentions refer to the same entity.
'''

COREF_TF_PROMPT_EXAMPLE = '''
Entity 1: {entity1}
Sentence 1: {sent1}
Entity 2: {entity2}
Sentence 2: {sent2}

Q. "The entity "{entity1}" mentioned in Sentence 1 and the entity "{entity2}" mentioned in Sentence 2 are {label} entities." - true or false? A.'''



COREF_MC_SYSTEM_PROMPT = '''
Consider the task of coreference resolution, where the goal is to identify whether or not two different entity mentions refer to the same underlying entity. Given two entity mentions and their representative sentences, answer the following multiple choice question regarding whether or not the two entity mentions are coreferent or not. Answer only with the letter corresponding to the correct answer.
'''

COREF_MC_PROMPT_EXAMPLE = '''
Entity 1: {entity1}
Sentence 1: {sent1}
Entity 2: {entity2}
Sentence 2: {sent2}

Q. What is the relationship between the entity "{entity1}" mentioned in Sentence 1 and "{entity2}" mentioned in Sentence 2? 
(A) Coreferent
(B) Distinct
'''

COREF_GS_SYSTEM_PROMPT = '''
Consider the task of coreference resolution, where the goal is to identify whether or not two different entity mentions refer to the same underlying entity. Given two entity mentions and their representative sentences, identify whether the entity mentions are coreferent or distinct. Answer only with "coreferent" or "distinct" and do not provide any justification or explanation.
'''

COREF_GS_PROMPT_EXAMPLE = '''
Entity 1: {entity1}
Sentence 1: {sent1}
Entity 2: {entity2}
Sentence 2: {sent2}

Q. What is the relationship between the entity "{entity1}" mentioned in Sentence 1 and "{entity2}" mentioned in Sentence 2? Answer only with "coreferent" or "distinct" and do not provide any justification or explanation.
'''

COREF_VC_SYSTEM_PROMPT = '''
Consider the task of coreference resolution, where the goal is to identify whether or not two different entity mentions refer to the same underlying entity. Given two entity mentions and their representative sentences, identify whether the entity mentions are coreferent or distinct. Please answer with the following format:
“Confidence: [the probability that the two entity mentions are {label} (0-100), please only include the numerical number in the range of 0-100]”
'''

COREF_VC_EXAMPLE_PROMPT = '''
Entity 1: {entity1}
Sentence 1: {sent1}
Entity 2: {entity2}
Sentence 2: {sent2}

Q: How likely is it that the two entitiy mentions are {label}. Do not elaborate on your answer or provide any explantion, answer only with the confidence value in the following format: 
 
“Confidence: [the probability that the two entity mentions are {label} (0-100), please only include the numerical number in the range of 0-100]”
'''

COREF_GC_SYSTEM_PROMPT = '''
Consider the task of coreference resolution. Given two entities mentions that are either coreferent or distinct, generate two sentences each containing one of the entity mentions.
'''

COREF_GC_EXAMPLE_FORMAT = '''
Generate two sentences based on the following description:
Generation Description: {0}'''

COREF_GENERATION_FORMAT = '''
Sentence 1: {sent1}
Sentence 2: {sent2}
'''

GEN_Z_COREF_LABEL_SENTENCES = [
    "The entity mention '{entity1}' in the first sentence and the entity mention of '{entity2}' in the second sentence are {label}",
    "The mention of '{entity1}' in sentence one and '{entity2}' in sentence two are considered {label}.",
    "'{entity1}' from the first sentence and '{entity2}' from the second sentence are labeled as {label}.",
    "In the first sentence, '{entity1}' is mentioned, and in the second sentence, '{entity2}' is mentioned — these are {label}.",
    "The entities '{entity1}' and '{entity2}', from the first and second sentences respectively, are {label}.",
    "We determine that '{entity1}' in sentence one and '{entity2}' in sentence two are {label}.",
    "There is a mention of '{entity1}' in the first sentence and of '{entity2}' in the second; they are {label}.",
    "According to the sentence context, '{entity1}' and '{entity2}' are identified as {label}.",
    "It is determined that the entity '{entity1}' in the first sentence and '{entity2}' in the second sentence are {label}.",
    "In the first sentence, the mention of '{entity1}', and in the second, the mention of '{entity2}', are considered {label}."
]

GEN_Z_COREF_LABEL_SENTENCES_POSITIVE = [
    "The entity mention '{entity1}' in the first sentence refers to the same entity as the entity mention of '{entity2}' in the second sentence.",
    "The entity mention '{entity1}' in the initial sentence refers to the same entity as the entity mention '{entity2}' in the second sentence.",
    "In the first sentence, the entity mention '{entity1}' is the same as the entity mention '{entity2}' in the second sentence.",
    "The mention of '{entity1}' in the opening sentence is identical to the mention of '{entity2}' in the following sentence.",
    "The entity referenced as '{entity1}' in the first sentence is the same as '{entity2}' in the second sentence.",
    "The initial sentence's entity mention '{entity1}' corresponds to the same entity as '{entity2}' mentioned in the second sentence.",
    "The entity '{entity1}' in the first sentence is identical to the entity '{entity2}' in the subsequent sentence.",
    "The entity mention '{entity1}' at the beginning of the first sentence refers to the same entity as '{entity2}' in the second sentence.",
    "The mention of '{entity1}' in the first sentence corresponds to the same entity as '{entity2}' in the second sentence.",
    "'{entity1}', appearing in the first sentence, denotes the same entity as '{entity2}', which appears in the second sentence."
]

GEN_Z_COREF_LABEL_SENTENCES_NEGATIVE = [
    "The entity mention '{entity1}' in the first sentence refers to a different entity as the entity mention of '{entity2}' in the second sentence.",
    "The entity mention '{entity1}' in the first sentence refers to a different entity than the entity mention '{entity2}' in the second sentence.",
    "In the first sentence, the entity mention '{entity1}' is distinct from the entity mention '{entity2}' in the second sentence.",
    "The mention of '{entity1}' in the opening sentence refers to a different entity than the mention of '{entity2}' in the following sentence.",
    "The entity referenced as '{entity1}' in the first sentence is different from '{entity2}' in the second sentence.",
    "The initial sentence's entity mention '{entity1}' does not refer to the same entity as '{entity2}' mentioned in the second sentence.",
    "The entity '{entity1}' in the first sentence is distinct from the entity '{entity2}' in the subsequent sentence.",
    "The entity mention '{entity1}' at the beginning of the first sentence refers to a different entity than '{entity2}' in the second sentence.",
    "The mention of '{entity1}' in the first sentence refers to a different entity than '{entity2}' in the second sentence.",
    "'{entity1}', appearing in the first sentence, denotes a different entity then '{entity2}', which appears in the second sentence.",
]


