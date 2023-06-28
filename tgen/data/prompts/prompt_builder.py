from typing import Union, List

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.util.enum_util import EnumDict


class PromptBuilder:

    def __init__(self, prompt_args: PromptArgs, prompts: List[Prompt]):
        """
        Constructs prompt creator with prompt arguments as configuration.
        :param prompt_args: The arguments customizing prompt generation.
        :param prompts: The list of prompts to use to build the final prompt
        """
        self.args = prompt_args
        self.prompts = prompts

    def build(self, base_prompt: str, base_completion: str) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :return: Dictionary containing the prompt and completion
        """

        prompt = self.format_prompt_for_model(base_prompt)
        completion = self.format_completion(base_completion)
        return EnumDict({
            PromptKeys.PROMPT: prompt,
            PromptKeys.COMPLETION: completion
        })

    def format_prompt_for_model(self, base_prompt: str) -> str:
        """
        Formats the prompt with expected prefix + suffix tokens
        :param base_prompt: The base prompt
        :return: The formatted prompt
        """
        return f"{self.args.prompt_prefix}{base_prompt}{self.args.prompt_suffix}"

    def format_completion(self, base_completion: str) -> str:
        """
        Formats the completion with expected prefix + suffix tokens
        :param base_completion: The base completion
        :return: The formatted completion
        """
        if not base_completion:
            return EMPTY_STRING
        return f"{self.args.completion_prefix}{base_completion}{self.args.completion_suffix}"
