import re

from typing_extensions import override

from tgen.util.supported_enum import SupportedEnum


class Prompt(str):
    """
    Represents a prompt with special formatting that allows delaying the formatting of certain fields
    """

    def __init__(self, value: str):
        """
        Initialize with the value of the prompt
        :param value: The value of the prompt
        """
        self.value = value

    def format(self, *args: object, **kwargs: object) -> str:
        """
        Overrides string format to allow the formatting of only selective fields
        :param args: Ordered params to format the prompt with
        :param kwargs: Key, value pairs to format the prompt with
        """
        formatting_fields = re.findall(r'\{(\w*)\}', self.value)
        updated_args = [arg for arg in args]
        for i, field in enumerate(formatting_fields):
            if kwargs and field not in kwargs:
                kwargs[field] = '{%s}' % field
            if args and i >= len(args):
                updated_args.append('{%s}' % field)
        return Prompt(super().format(*updated_args, **kwargs))


class SupportedPrompts(SupportedEnum):
    """
    Enumerates supported prompts used for completion tasks.
    """
    CLASSIFICATION = Prompt("Is (1) related to (2)?\n.")
    CODE_SUMMARY = Prompt("Provide 5 sentence paragraph describing the high-level usage of the code below. "
                          "Do not focus on implementation details and assume your audience works on this system.\n '{target_content}'")
    NL_SUMMARY = Prompt("Summarize the following '{target_content}'")
    USER_STORY_CREATION = Prompt("Write a single {artifact_type} that focuses on the {artifact_id} functionality of the "
                                 "following code descriptions. Enclose the user story in the tags <doc></doc>:\n '{target_content}'")
    UAV_SYSTEM_REQUIREMENT = Prompt("Given a summary of python code, write a system-level requirement\n "
                                    "The requirements should reference physical world entities related to the UAV systems, "
                                    "be numbered system level requirements and use the 'shall' format:\n '{target_content}'")
    CLUSTERING = Prompt("I am giving you a numbered list of software artifact descriptions. Group the artifacts by functionality. "
                        "Enclose each group in tags <group></group> and inside each group provide a brief summary of the group's "
                        "functionality in <summary></summary> and the numbers corresponding to the artifacts in the group inside of "
                        "<artifacts></artifacts>:\n '{target_content}'")