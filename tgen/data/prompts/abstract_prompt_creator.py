from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Dict, Type

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.base_prompt import BasePrompt
from tgen.util.base_object import BaseObject
from tgen.util.enum_util import EnumDict
from tgen.util.override import overrides


@dataclass
class AbstractPromptCreator(BaseObject):
    """
    Responsible for formatting and creating prompts and completions for Language Models
    """
    base_prompt: BasePrompt

    _PROMPT_SEPARATOR = "\n\n###\n\n"
    _COMPLETION_SEPARATOR = "###"
    COMPLETION_START = " "

    def format_prompt(self, base_prompt: str) -> str:
        """
        Formats the prompt with expected prefix + suffix tokens
        :param base_prompt: The base prompt
        :return: The formatted prompt
        """
        return f"{base_prompt}{self._PROMPT_SEPARATOR}"

    def format_completion(self, base_completion: str) -> str:
        """
        Formats the completion with expected prefix + suffix tokens
        :param base_completion: The base completion
        :return: The formatted completion
        """
        if not base_completion:
            return EMPTY_STRING
        return f"{self.COMPLETION_START}{base_completion}{self._COMPLETION_SEPARATOR}"

    def generate_base(self, base_prompt: str, base_completion: str) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :return: Dictionary containing the prompt and completion
        """
        prompt = self.format_prompt(base_prompt)
        completion = self.format_completion(base_completion)
        return EnumDict({
            PromptKeys.PROMPT: prompt,
            PromptKeys.COMPLETION: completion
        })

    @abstractmethod
    def create(self, source_content: str, target_content: str, **kwargs) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :param source_content: The content of the source artifact
        :param target_content: The content of the target artifact
        :param kwargs: Additional params for the generation
        :return: Dictionary containing the prompt and completion
        """

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from tgen.data.prompts.supported_prompt_creator import SupportedPromptCreator
        return SupportedPromptCreator
