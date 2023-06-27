from tgen.data.prompts.prompt import ArtGenPrompt, Prompt
from tgen.util.supported_enum import SupportedEnum

SOURCE_COMPONENT_LABEL = "source_component"
TARGET_COMPONENT_LABEL = "target_component"

SCORE_LABEL = "related-score"
RELATED_LABEL = "related"
UNRELATED_LABEL = "unrelated"
RELATIONSHIP_LABEL = "relationship"
CLASSIFICATION_LABEL = "label"
DEFAULT_CLASSIFICATION_PROMPT = Prompt("You are a software engineer working on a software project. "
                                       "Your task is to trace software artifacts of this system. "
                                       "\n- In 10 words, describe the function of the sub-system containing (2)? "
                                       f"Enclose your answer in <{SOURCE_COMPONENT_LABEL}></{SOURCE_COMPONENT_LABEL}>."

                                       "\n- In 10 words, describe the function of the sub-system containing (1)? "
                                       f"Enclose your answer in <{TARGET_COMPONENT_LABEL}></{TARGET_COMPONENT_LABEL}>."

                                       "\n- In 10 words, describe how (1) and (2) might interact within the system? "
                                       f"Enclose your answer in <{RELATIONSHIP_LABEL}></{RELATIONSHIP_LABEL}>."

                                       "\n- In 10 words, describe why the responsibilities of (1) and (2) might be related. "
                                       f"Enclose your answer in <{RELATED_LABEL}></{RELATED_LABEL}>."

                                       "\n- In 10 words, describe why the responsibilities of (1) and (2) are different. "
                                       f"Enclose your answer in <{UNRELATED_LABEL}></{UNRELATED_LABEL}>. "

                                       "\n- Is there a direct traceability link between (1) and (2)? "
                                       f"Answer should be 'yes' or 'no' enclosed in <{CLASSIFICATION_LABEL}></{CLASSIFICATION_LABEL}>."

                                       "\nProvide a floating point number between 0 and 1 describing the strength of the traceability link. "
                                       "A score between 0.75 and 1.0 means (1) and (2) describe similar responsibilities. "
                                       "A score between 0.5 and 0.7 means (1) and (2) describe interfacing responsibilities. "
                                       "A score between 0.2 and 0.45 means there is an indirect relationship between (1) and (2). "
                                       "A score between 0 and 0.2 means there is no relationship between (1) and (2). "
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
