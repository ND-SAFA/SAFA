from dataclasses import dataclass
from typing import Dict

from tgen.data.prompts.base_prompt import BasePrompt
from tgen.data.prompts.abstract_prompt_generator import AbstractPromptGenerator


@dataclass
class CreationPromptGenerator(AbstractPromptGenerator):
    base_prompt: BasePrompt = BasePrompt.SYSTEM_REQUIREMENT_CREATION

    def generate(self, source_content: str, target_content: str) -> Dict[str, str]:
        """
        Generates the prompt and response
        :source_content: The content of the source artifact
        :target_content: The content of the target artifact
        :return: Dictionary containing the prompt and completion
        """
        return self.generate_base(self.base_prompt.value.format(target_content), source_content)
