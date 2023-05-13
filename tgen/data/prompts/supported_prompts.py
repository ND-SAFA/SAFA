from tgen.util.supported_enum import SupportedEnum


class SupportedPrompts(SupportedEnum):
    """
    Enumerates supported prompts used for completion tasks.
    """
    CLASSIFICATION = "Is (1) related to (2)?\n."
    CODE_SUMMARY = "Provide 5 sentence paragraph describing the high-level usage of the code below. Do not focus on implementation " \
                   "details and assume your audience works on this system. '{target_content}'"
    NL_SUMMARY = "Summarize the following '{target_content}'"
    USER_STORY_CREATION = "Write a single user story that focuses on the {artifact_id} functionality of the " \
                          "following code descriptions. Make the user story start with 'As a'\n '{target_content}'"
    SYSTEM_REQUIREMENT_CREATION = "Given a summary of python code, write a system-level requirement\n The requirements should " \
                                  "reference physical world entities related to the UAV systems, be numbered system level " \
                                  "requirements and use the 'shall' format:\n '{target_content}'"
    CLUSTERING = "Group the following code descriptions by functionality: {target_content}"
