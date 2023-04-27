from dataclasses import dataclass

from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.base_prompt import BasePrompt
from tgen.util.enum_util import EnumDict


@dataclass
class GenerationPromptCreator(AbstractPromptCreator):
    """
    Responsible for creating prompts for generation (e.g artifact creation, summarization)
    """
    base_prompt: BasePrompt = BasePrompt.SYSTEM_REQUIREMENT_CREATION

    def create(self, source_content: str, target_content: str, **kwargs) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :param source_content: The content of the source artifact
        :param target_content: The content of the target artifact
        :return: Dictionary containing the prompt and completion
        """
        return self.generate_base(self.base_prompt.value.format(target_content), source_content)
