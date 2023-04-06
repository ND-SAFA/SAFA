from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Dict, Type

from tgen.data.prompts.base_prompt import BasePrompt
from tgen.util.base_object import BaseObject
from tgen.util.override import overrides


@dataclass
class AbstractPromptGenerator(ABC, BaseObject):
    base_prompt = BasePrompt

    __PROMPT_SEPARATOR = "\n\n###\n\n"
    __COMPLETION_SEPARATOR = "###"
    COMPLETION_START = " "
    PROMPT_KEY = "prompt"
    COMPLETION_KEY = "completion"

    def format_prompt(self, base_prompt: str) -> str:
        """
        Formats the prompt with expected prefix + suffix tokens
        :param base_prompt: The base prompt
        :return: The formatted prompt
        """
        return f"{base_prompt}{self.__PROMPT_SEPARATOR}"

    def format_completion(self, base_completion: str) -> str:
        """
        Formats the completion with expected prefix + suffix tokens
        :param base_completion: The base completion
        :return: The formatted completion
        """
        return f"{self.COMPLETION_START}{base_completion}{self.__COMPLETION_SEPARATOR}"

    def generate_base(self, base_prompt: str, base_completion: str) -> Dict[str, str]:
        """
        Generates the prompt and response
        :return: Dictionary containing the prompt and completion
        """
        prompt = self.format_prompt(base_prompt)
        completion = self.format_completion(base_completion)
        return {
            "prompt": prompt,
            "completion": completion
        }

    @abstractmethod
    def generate(self, source_content: str, target_content: str, label: int = None) -> Dict[str, str]:
        """
        Generates the prompt and response
        :source_content: The content of the source artifact
        :target_content: The content of the target artifact
        :label: The label of the link
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
        from tgen.data.prompts.supported_prompt_generator import SupportedPromptGenerator
        return SupportedPromptGenerator
