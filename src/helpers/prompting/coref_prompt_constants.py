COREF_PROMPT_INSTRUCTIONS_ZERO_SHOT = 'Given two entity mentions and their representative sentences, decide whether the entity mentions refer to the same entity or not.'
COREF_PROMPT_INSTRUCTIONS_FEW_SHOT = 'Given two entity mentions and their representative sentences, decide whether the entity mentions refer to the same entity or not. For Example:'

COREF_PROMPT_EXAMPLE = '### Entity 1: {entity1} Sentence 1: {sent1} Entity 2: {entity2} Sentence 2: {sent2} Q. {entity1} refers to {entity2}" - True or False? A. {answer}'
COREF_PROMPT_QUESTION = '### Entity 1: {entity1} Sentence 1: {sent1} Entity 2: {entity2} Sentence 2: {sent2} Q. {entity1} refers to {entity2}" - True or False? A. '

GEN_Z_COREF_PARAPHRASE_PROMPT_POSITIVE = 'Write 10 paraphrases of this sentence as a Python list. “The entity mention {entity1} in the first sentence refers to the same entity as the entity mention of {entity2} in the second sentence."'
GEN_Z_COREF_PARAPHRASE_PROMPT_NEGATIVE = 'Write 10 paraphrases of this sentence as a Python list. “The entity mention {entity1} in the first sentence refers to a different entity as the entity mention of {entity2} in the second sentence."'

GEN_Z_COREF_FORMAT = 'Sentence 1: {sent1} Sentence 2: {sent2}'
GEN_Z_COREF_EXAMPLE_FORMAT = '### Generation Description: {0} '
GEN_Z_COREF_INTRO_ZERO_SHOT = 'Given a description of two entity mentions that each belong to a sentence. Generate the sentences that contain these entity mentions.'
GEN_Z_COREF_INTRO_FEW_SHOT = 'Given a description of two entity mentions that each belong to a sentence. Generate the sentences that contain these entity mentions. For Example:'


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


