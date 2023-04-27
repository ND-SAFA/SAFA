from dataclasses import dataclass


@dataclass
class PromptArgs:
    """
    Defines arguments for defining properties for prompt dataset creation.
    """

    def __init__(self, prompt_separator: str, completion_prefix: str, completion_suffix: str):
        """
        Constructs prompt args using base prompt and all arguments defined in AI prompt args.
        :param prompt_separator: The delimiter between prompt and completion.
        :param completion_prefix: The token to prefix completion labels with.
        :param completion_suffix: The token to append completion labels with.
        """
        self.prompt_separator = prompt_separator
        self.completion_prefix = completion_prefix
        self.completion_suffix = completion_suffix
