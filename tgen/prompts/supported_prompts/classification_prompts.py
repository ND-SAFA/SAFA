from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager
from tgen.prompts.select_question_prompt import SelectQuestionPrompt

SOURCE_COMPONENT_LABEL = "subsystem_one"
TARGET_COMPONENT_LABEL = "subsystem_two"
SCORE_LABEL = "related-score"
RELATED_LABEL = "related"
UNRELATED_LABEL = "unrelated"
CLASSIFICATION_LABEL = "classification"
JUSTIFICATION = "justification"
CURRENT_LABELS = [SOURCE_COMPONENT_LABEL, TARGET_COMPONENT_LABEL, RELATED_LABEL, UNRELATED_LABEL, CLASSIFICATION_LABEL, JUSTIFICATION,
                  SCORE_LABEL]
A_CATEGORY = "Are the artifacts exactly the same or was one derived directly from the other? If so, select A."
B_CATEGORY = "Will changes to one artifact very likely require changes to the other? " \
             "If a big change must occur, select B. If small or indirect changes must occur, select C."
C_CATEGORY = "Are the artifacts related but changes may or may not propagate? Select C if linkage is unclear."
D_CATEGORY = "Do minor relationships exist but artifacts are largely standalone? Select D for weak, tangential links."
E_CATEGORY = "Are the artifacts completely separate with no relationship? Select E only if fully independent."
CLASSIFICATION_CATEGORIES = {
    "DIRECT": A_CATEGORY,
    "INDIRECT SIGNIFICANT": B_CATEGORY,
    "INDIRECT RELATED": C_CATEGORY,
    "INDIRECT UNRELATED": D_CATEGORY,
    "INDEPENDENT": E_CATEGORY
}
CLASSIFICATION_SCORES = {
    "DIRECT": [0.75, 1],
    "INDIRECT SIGNIFICANT": [0.75, 0.5],
    "INDIRECT RELATED": [0.25, 0.5],
    "INDIRECT UNRELATED": [0, 0.25],
    "INDEPENDENT": [0, 0]
}
REVERSE_CATEGORIES = ["E"]
CATEGORIES = list(CLASSIFICATION_CATEGORIES.keys())

CLASSIFICATION_STEPS = {
    1: QuestionPrompt("In 10 words, describe the function of the sub-system containing (1).",
                      response_manager=XMLResponseManager(response_tag=SOURCE_COMPONENT_LABEL)),

    2: QuestionPrompt("In 10 words, describe the function of the sub-system containing (2).",
                      response_manager=XMLResponseManager(response_tag=TARGET_COMPONENT_LABEL)),

    3: QuestionPrompt("Describe all the ways that (1) and (2) are dependent on each other.",
                      response_manager=XMLResponseManager(response_tag=RELATED_LABEL)),

    4: QuestionPrompt("Describe all the ways that (1) and (2) are independent on each other.",
                      response_manager=XMLResponseManager(response_tag=UNRELATED_LABEL)),

    5: SelectQuestionPrompt(CLASSIFICATION_CATEGORIES, question="Classify (1) and (2) into one of the following:"),

    6: QuestionPrompt("Provide a detailed reasoning of the classification using your answers as references.",
                      response_manager=XMLResponseManager(response_tag=JUSTIFICATION))
}

STRENGTH = "Rate the strength of the relatedness between the artifacts with a floating point number between 0 and 1. " \
           "For each category, place rating close to their upper or lower bounds. "

STRENGTH_INSTRUCTIONS = "Categories score bounds:"
STRENGTH_CATEGORIES = {
    CATEGORIES[0]: "should receive scores between (0.9, 1.0)",
    CATEGORIES[1]: "should receive scores between (0.6, 0.9)",
    CATEGORIES[2]: "should receive scores between (0.4, 0.6)",
    CATEGORIES[3]: "should receive scores between (0.2, 0.4)",
    CATEGORIES[4]: "should receive scores between (0.0, 0.2)"
}
Q7 = SelectQuestionPrompt(STRENGTH_CATEGORIES, question=STRENGTH, instructions=STRENGTH_INSTRUCTIONS,
                          response_tag="related-score")

CLASSIFICATION_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=CLASSIFICATION_STEPS)
