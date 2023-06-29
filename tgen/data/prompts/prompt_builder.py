from typing import List, Tuple

from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.util.enum_util import EnumDict


class PromptBuilder:

    def __init__(self, prompt_args: PromptArgs, prompts: List[Prompt], base_completion: str = None):
        """
        Constructs prompt creator with prompt arguments as configuration.
        :param prompt_args: The arguments customizing prompt generation.
        :param prompts: The list of prompts to use to build the final prompt
        """
        self.args = prompt_args
        self.prompts = prompts
        self.base_completion = base_completion
        self.requires_traces, self.requires_artifacts = self._check_requirements(self.prompts)

    def build(self, **prompt_kwargs) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :return: Dictionary containing the prompt and completion
        """
        base_prompt = NEW_LINE.join([prompt.build(**prompt_kwargs) for prompt in self.prompts])
        prompt = self.format_prompt_for_model(base_prompt)
        completion = self.format_completion(self.base_completion)
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

    @staticmethod
    def _check_requirements(prompts: List[Prompt]) -> Tuple[bool, bool]:
        """
        Determines if traces or artifacts are needed for prompt
        :return: Tuple containing a bool representing if traces are required and bool for artifacts requirement
        """
        requires_traces, requires_artifacts = False, False
        for prompt in prompts:
            if prompt.requires_traces:
                requires_traces = True
            if prompt.requires_artifacts:
                requires_artifacts = True
        return requires_traces, requires_artifacts
