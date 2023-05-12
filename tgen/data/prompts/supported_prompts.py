from tgen.util.supported_enum import SupportedEnum


class Prompt(str):
    def __init__(self, value: str):
        self.value = value

    def format(self, format_spec, **kwargs):
        return self.value.format(format_spec)


class SupportedPrompts(SupportedEnum):
    """
    Enumerates supported prompts used for completion tasks.
    """
    CLASSIFICATION = Prompt("Is (1) related to (2)?\n.")
    CODE_SUMMARY = Prompt(
        "Provide 5 sentence paragraph describing the high-level usage of the code below. Do not focus on implementation " \
        "details and assume your audience works on this system. '{}'")
    NL_SUMMARY = Prompt("Summarize the following '{}'")
    USER_STORY_CREATION = Prompt("Write a single user story that focuses on the functionality of the following code descriptions. " \
                                 "Make the user story start with 'As a'\n '{}'")
    SYSTEM_REQUIREMENT_CREATION = Prompt("Given a summary of python code, write a system-level requirement\n The requirements should " \
                                         "reference physical world entities related to the UAV systems, be numbered system level " \
                                         "requirements and use the 'shall' format:\n '{}'")
