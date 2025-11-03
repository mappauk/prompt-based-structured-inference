LEVEL_1_LABEL_TO_INDEX = {
    'None': 0,
    'Non-probing-deliberation': 1,
    'Probing': 2
}

LEVEL_1_LABELS = [
    'None',
    'Non-probing-deliberation',
    'Probing'
]

LEVEL_1_TO_CHOICE_MAP = {
    'None': 'A',
    'Non-probing-deliberation': 'B',
    'Probing': 'C'
}

LEVEL_2_TO_CHOICE_MAP = {
    'None': 'A',
    'Solution': 'B',
    'Reasoning': 'C',
    'Agree': 'D',
    'Disagree': 'E',
    'Moderation': 'F'
}

LEVEL_1_CHOICES = [
    "A",
    "B",
    "C"
]

LEVEL_2_LABEL_TO_INDEX = {
    'None': 0,
    'Solution': 1,
    'Reasoning': 2,
    'Agree': 3,
    'Disagree': 4,
    'Moderation': 5
}

LEVEL_2_LABELS = [
    'None',
    'Solution',
    'Reasoning',
    'Agree',
    'Disagree',
    'Moderation'
]

LEVEL_2_CHOICES = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F"
]

LEVEL_ONE_SYSTEM_PROMPT = '''
Consider the task of identifying the type of deliberation present in an utterance by a speaker within a broader group conversation. There are three possible deliberation types:

Probing deliberation: any utterance that provokes discussion, deliberation or argumentation without introducing novel information. Such utterances could be
considered conversational interventions that may change the flow of the conversation to induce further arguments or to moderate a conversation.

Non-probing deliberation: all discussions that are concerned with the task's solution and participants' reasoning. These utterances are useful to the conversation, but are not probing.

None: Any utterance that does not fall into the Probing or Non-probing categories. Often these utterances  are greetings or hesitation cues.

Given the possible deliberation types and their definitions, answer the following multiple choice question regarding what deliberation type is being expressed in an utterance. Answer only with the letter corresponding to the correct answer.
'''

LEVEL_TWO_SYSTEM_PROMPT = '''
Consider the task of identifying the deliberation role present in an utterance by a speaker within a broader group conversation. There are six possible deliberation roles:

Moderation: Moderation utterances are not concerned directly with the task at hand, but rather with how participants converse about it.

Reasoning: Utterances focusing on argumentation.

Solution: Utterances that are managing the solution of the task.

Agree: Utterances expressing agreement with a previous argument or solution.

Disagree: Utterances expressing disagreement with a previous argument or solution.

None: Utterances that do not fall into any of the other categories.

Given the possible deliberation roles and their definitions, answer the following multiple choice question regarding what deliberation role is being expressed in an utterance. Answer only with the letter corresponding to the correct answer.
'''

LEVEL_ONE_EXAMPLE_FORMAT = '''Utterance: {original_text}
Q. What type of deliberation is being expressed in the given utterance?
Choices:
(A) None
(B) Non-probing deliberation
(C) Probing deliberation
'''

LEVEL_TWO_EXAMPLE_FORMAT = '''Utterance: {original_text}
Q. What specific deliberative move is being expressed in the given utterance?
Choices:
(A) None
(B) Solution
(C) Reasoning
(D) Agree
(E) Disagree
(F) Moderation
'''

SYSTEM_PROMPT_EXAMPLE_LEAD_IN = 'Consider the following examples:\n'


LEVEL_1_TO_LEVEL_2 = {
    'Probing': ['Moderation', 'Reasoning', 'Solution'],
    'Non-probing-deliberation': ['Reasoning', 'Solution', 'Agree', 'Disagree'],
    'None': ['None'],
}