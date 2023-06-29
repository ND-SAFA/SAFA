from tgen.data.prompts.prompt import ArtGenPrompt, Prompt
from tgen.util.supported_enum import SupportedEnum

SCORE_LABEL = "related-score"
RELATED_LABEL = "dependencies"
UNRELATED_LABEL = "unrelated"
CLASSIFICATION_LABEL = "classification"
JUSTIFICATION = "justification"

A_CATEGORY = "Do the two artifacts have a highly close or interdependent traceability relationship? " \
             "For example, were they derived from related precursors or provide similar, linked functionality? " \
             "If yes, select A. If no, proceed to next question. "
B_CATEGORY = "Do the artifacts have a tightly coupled relationship " \
             "where changes to one would require changes to the other? " \
             "If yes, select B. Remember that if there is a direct traceability link between them, select A. " \
             "If unsure or no, proceed to next question."
C_CATEGORY = "Are the artifacts only loosely related at a high level, " \
             "where changes are unclear or uncertain to propagate? " \
             "If yes, select C. If no or unsure, proceed to next question"
D_CATEGORY = "Do the artifacts share any minor properties, interfaces or other characteristics? " \
             "If yes, select D. If no, proceed to next question. "
E_CATEGORY = "Are there any discernable relationships or connections between the two artifacts? " \
             "If yes, return to previous questions to re-assess categories. If no, select E."
CLASSIFICATION_SCORES = {
    "A": 0.9,
    "B": 0.7,
    "C": 0.5,
    "D": 0.3,
    "E": 0.1,
    "F": 0
}
DEFAULT_CLASSIFICATION_PROMPT = Prompt("You are a software engineer working on a software project. "
                                       "Your task is to trace software artifacts of this system. "

                                       "\n- Describe all the ways that (1) and (2) are dependent on each other. "
                                       f"Enclose your answer in <{RELATED_LABEL}></{RELATED_LABEL}>."

                                       "\n- Describe all the ways that (1) and (2) are independent on each other. "
                                       f"Enclose your answer in <{UNRELATED_LABEL}></{UNRELATED_LABEL}>."

                                       "\n- Classify (1) and (2) into one of the following:"
                                       f"\nA) {A_CATEGORY}"
                                       f"\nB) {B_CATEGORY}"
                                       f"\nC) {C_CATEGORY}"
                                       f"\nD) {D_CATEGORY}"
                                       f"\nE) {E_CATEGORY}"
                                       "\nF) The two artifacts have opposite or incompatible purposes, functionality or effects."
                                       f"\nEnclose your answer in<{CLASSIFICATION_LABEL}></{CLASSIFICATION_LABEL}>."

                                       "\n- Provide a detailed reasoning of the classification using your answers as references. "
                                       f"Enclose your answer in <{JUSTIFICATION}></{JUSTIFICATION}>."

                                       "\n- Rate the strength of the artifacts with a floating point number between 0 and 1. "
                                       "Category A should receive scores between (0.8, 1.0), "
                                       "Category B should receive scores between (0.6, 0.8), "
                                       "Category C should receive scores between (0.4, 0.6), "
                                       "Category D should receive scores between (0.2, 0.4), "
                                       "Category E should receive scores between (0.0, 0.2), "
                                       "Category F should receive a score of 0."
                                       "For each category, place rating close to their upper or lower bounds. "
                                       f"Enclose your answer in <{SCORE_LABEL}></{SCORE_LABEL}>.\n")


class SupportedPrompts(SupportedEnum):
    """
    Enumerates supported prompts used for completion tasks.
    """
    CLASSIFICATION = DEFAULT_CLASSIFICATION_PROMPT
    CODE_SUMMARY = Prompt("Provide a few sentences describing the high-level usage of the code below. "
                          "Do not focus on implementation details and assume your audience works on this system."
                          "The summary should be enclosed in the tags <summary></summary>:\n '{target_content}'")
    NL_SUMMARY = Prompt("Summarize the following, focusing on the high-level usage. "
                        "Enclose the summary in the tags <summary></summary>:\n '{target_content}'")
    ARTIFACT_GENERATION = ArtGenPrompt("Write a single {artifact_type} that describes the {artifact_id} feature of the "
                                       "following software descriptions, including only high-level information. "
                                       "An example of a good {artifact_type} is {example}. "
                                       "Enclose the {artifact_type} in the tags <doc></doc>:\n "
                                       "'{target_content}'")
    UAV_SYSTEM_REQUIREMENT = Prompt("Given a summary of python code, write a system-level requirement\n "
                                    "The requirements should reference physical world entities related to the UAV systems, "
                                    "be numbered system level requirements and use the 'shall' format:\n '{target_content}'")
    FUNCTIONALITIES = Prompt("I am giving you a numbered list of artifact descriptions for a software system. "
                             "Describe the functionalities of the system that would be "
                             "important for grouping related artifacts belonging to a single {target_artifact_type}. "
                             "Focus on aspects that are unique to this system but remain high-level. "
                             "Output each functionality enclosed in the tags <feature></feature>"
                             "\n\n '{target_content}'")
    RE_CLUSTER_FEATURE = Prompt("I am giving you a numbered list of software artifact descriptions relating to {feature}. "
                                "Determine sub features that would divide the artifacts into groups "
                                "belonging to a single {target_artifact_type}. "
                                "Here are some existing features that may be used for grouping the artifacts. {features}"
                                "Focus on aspects that are unique to this system but remain high-level. "
                                "Group the artifacts by these sub features "
                                "where each group has at least 2 artifacts and no more than 10 artifacts. "
                                "Artifacts should belong to at least 1 group. "
                                "Enclose each group in tags <group></group>. "
                                "Inside each group name the group's feature in <feature></feature> "
                                "and the numbers corresponding to the artifacts in the group inside of <artifacts></artifacts>:"
                                "\n\n '{target_content}'")
    CLUSTER_FROM_FEATURES = Prompt("I am giving you a list of features for creating {target_artifact_type}s "
                                   "and a numbered list of software artifact descriptions. "
                                   "Group all artifacts with the features that relate to it. "
                                   "If none of the features relate to the description, "
                                   "create a new feature for a {target_artifact_type} "
                                   "which relates to other artifacts as well "
                                   "and group these related artifacts with it. "
                                   "If the feature is too broad, you may replace it with sub features. "
                                   "Groups must contain at least 2 artifacts and at most 10 artifacts "
                                   "and all artifacts should belong to at least one group.  "
                                   "Focus on aspects that are unique to this system but remain high-level. "
                                   "Enclose each feature group in tags <group></group> "
                                   "with the feature name inside of <feature></feature> "
                                   "and the numbers corresponding to the artifacts which relate to that feature "
                                   "inside of <artifacts></artifacts>:"
                                   "\n\nfeatures: '{features}'\nartifacts: '{target_content}'")
    ARTIFACT_EXAMPLE = Prompt("Write a single example of a {artifact_type} body. Enclose the body in <example></example>.")
