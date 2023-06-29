from tgen.data.prompts.prompt import ArtGenPrompt, Prompt
from tgen.util.supported_enum import SupportedEnum

CONFIDENCE_LABEL = "confidence"
INTERSECTION_LABEL = "intersection"
INTERSECTION_SCORE = "intersection_score"
CLASSIFICATION_LABEL = "classification"
JUSTIFICATION = "justification"
CHANGE_ANALYSIS = "change_analysis"

A_CATEGORY = "Do the two artifacts have interdependent relationship that is essential to the " \
             "primary functionality of at least one artifact? " \
             "For example, were they derived from related precursors or provide similar, linked functionality? " \
             "If yes, select A. If no, proceed to next question. "
B_CATEGORY = "Do the artifacts have a tightly coupled relationship " \
             "where changes to one would require changes to the other? " \
             "If yes, select B. If unsure or no, proceed to next question."
C_CATEGORY = "Are the artifacts only loosely related at a high level, " \
             "where changes are unclear or uncertain to propagate? " \
             "If yes, select C. If no or unsure, proceed to next question"
D_CATEGORY = "Do the artifacts share any minor properties, interfaces or other characteristics? " \
             "If yes, select D. If no, proceed to next question. "
E_CATEGORY = "Are there any discernible relationships or connections between the two artifacts? " \
             "If yes, return to previous questions to re-assess categories. If no, select E."
REVERSE_CATEGORIES = ["E"]
CLASSIFICATION_SCORES = {
    "A": [0.9, 1],
    "B": [0.7, 0.9],
    "C": [0.5, 0.7],
    "D": [0.3, 0.5],
    "E": [0.0, 0.3],
}
DEFAULT_CLASSIFICATION_PROMPT = Prompt("# Task\nYou are a senior software engineer working on a software project. "
                                       "Your task is to analyze the relationships between project artifacts "
                                       "to determine which are related."
                                       "# Questions\n"

                                       "\n- Describe the intersection between the responsibilities of (1) and (2). "
                                       f"Enclose your answer in <{INTERSECTION_LABEL}></{INTERSECTION_LABEL}>."

                                       "\n- Provide a score between 0 and 1 justifying the intersection of your answer. "
                                       "Higher scores correspond to more intersection. "
                                       f"Enclose your answer in <{INTERSECTION_SCORE}></{INTERSECTION_SCORE}>"

                                       "\n- Analyze the likely effect of changes made to one artifact on the other. "
                                       f"Enclose your answer in <{CHANGE_ANALYSIS}></{CHANGE_ANALYSIS}>."

                                       "\n- Classify the relationship between (1) and (2) into one of the following:"
                                       f"\nA) {A_CATEGORY}"
                                       f"\nB) {B_CATEGORY}"
                                       f"\nC) {C_CATEGORY}"
                                       f"\nD) {D_CATEGORY}"
                                       f"\nE) {E_CATEGORY}"
                                       f"\nEnclose your answer in<{CLASSIFICATION_LABEL}></{CLASSIFICATION_LABEL}>."

                                       "\n- Provide a detailed reasoning of the classification using your answers as references. "
                                       f"Enclose your answer in <{JUSTIFICATION}></{JUSTIFICATION}>."

                                       "\n- Rate your confidence that the artifacts belong to the selected category. "
                                       "Provide a floating point number between 0 and 1. "
                                       "Higher scores should be given only when confident the relationship clearly belongs in the "
                                       "selected category based on the factors above. Mid or lower range scores indicate less "
                                       "certainty or a weaker relationship for that category. Consider adjacent categories when "
                                       "unsure if a link belongs in the selected class. "
                                       f"Enclose your answer in <{CONFIDENCE_LABEL}></{CONFIDENCE_LABEL}>.\n"
                                       "# Artifacts\n")


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
