from tgen.util.supported_enum import SupportedEnum


class SupportedPrompts(SupportedEnum):
    """
    Enumerates supported prompts used for completion tasks.
    """
    CLASSIFICATION = "Is (1) related to (2)?\n."
    CODE_SUMMARY = "Provide 5 sentence paragraph describing the high-level usage of the code below. Do not focus on implementation " \
                   "details and assume your audience works on this system. '{}'"
    NL_SUMMARY = "Summarize the following '{}'"
    USER_STORY_CREATION = "Write a single user story that captures the main functionality of the following code descriptions. " \
                          "Make the user story start with 'As a'\n '{}'"
    SYSTEM_REQUIREMENT_CREATION = "Given a summary of python code, write a system-level requirement\n The requirements should " \
                                  "reference physical world entities related to the UAV systems, be numbered system level " \
                                  "requirements and use the 'shall' format:\n '{}'"
