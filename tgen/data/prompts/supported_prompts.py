from tgen.util.supported_enum import SupportedEnum


class SupportedPrompts(SupportedEnum):
    """
    Enumerates supported prompts used for completion tasks.
    """
    CLASSIFICATION = "Are the following software system artifacts related? Answer \"yes\" or \"no\"."
    CODE_SUMMARY = "Provide 5 sentence paragraph describing the high-level usage of the code below. Do not focus on implementation " \
                   "details and assume your audience works on this system. '{}'"
    NL_SUMMARY = "Summarize the following '{}'"
    SHALL_REQUIREMENT_SUMMARY = "Remove the terms `The system shall' from the following text and then " \
                                "summarize in 20 words or less '{}'"
    HEADING_SUMMARY = "I am trying to provide a very short and representative summary of the long text to use as a heading " \
                      "in a diagram. Please reduce the following text to less than 8 words '{}'"
    USER_STORY_CREATION = "I want to write user requirements from the perspective of key stakeholders starting with 'As a'. " \
                          "Please write two to three user stories for the following functions '{}'"
    SYSTEM_REQUIREMENT_CREATION = "Given a summary of python code, write a system-level requirement\n The requirements should " \
                                  "reference physical world entities related to the UAV systems, be numbered system level " \
                                  "requirements and use the 'shall' format:\n '{}'"
