from dataclasses import dataclass
from typing import Dict

from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.base_prompt import BasePrompt


@dataclass
class ClassificationPromptCreator(AbstractPromptCreator):
    base_prompt: BasePrompt = BasePrompt.CLASSIFICATION
    pos_class: str = "yes"
    neg_class: str = "no"
    artifact_prompt_format: str = "\n1. {}\n2. {}"

    def create(self, source_content: str, target_content: str, label: int = None) -> Dict[str, str]:
        """
        Generates the prompt and response
        :source_content: The content of the source artifact
        :target_content: The content of the target artifact
        :label: The label of the link
        :return: Dictionary containing the prompt and completion
        """
        artifact_prompt = self.artifact_prompt_format.format(source_content, target_content, label)
        prompt = f"{self.base_prompt.value}{artifact_prompt}"
        class_ = self.pos_class if label == 1 else self.neg_class
        return self.generate_base(prompt, class_)
