from tgen.data.prompts.prompt import ArtGenPrompt, Prompt
from tgen.util.supported_enum import SupportedEnum


class SupportedPrompts(SupportedEnum):
    """
    Enumerates supported prompts used for completion tasks.
    """
    CLASSIFICATION = Prompt("Is the functionality of (1) related to (2)?\n.")
    CODE_SUMMARY = Prompt("Provide 5 sentence paragraph describing the high-level usage of the code below. "
                          "Do not focus on implementation details and assume your audience works on this system:\n '{target_content}'")
    NL_SUMMARY = Prompt("Summarize the following:\n '{target_content}'")
    ARTIFACT_GENERATION = ArtGenPrompt("Write a single {artifact_type} that describes on the {artifact_id} functionality of the "
                                       "following software descriptions. Enclose the {artifact_type} in the tags <doc></doc>:\n "
                                       "'{target_content}'")
    UAV_SYSTEM_REQUIREMENT = Prompt("Given a summary of python code, write a system-level requirement\n "
                                    "The requirements should reference physical world entities related to the UAV systems, "
                                    "be numbered system level requirements and use the 'shall' format:\n '{target_content}'")
    CLUSTERING = Prompt("I am giving you a numbered list of software artifact descriptions. "
                        "Group the artifacts into groups of at most 5 artifacts "
                        "where each group shares some common functionality. "
                        "Artifacts should belong to at least 1 group. "
                        "Enclose each group in tags <group></group>. "
                        "Inside each group name the group's functionality in <summary></summary> "
                        "and the numbers corresponding to the artifacts in the group inside of <artifacts></artifacts>:"
                        "\n\n '{target_content}'")
