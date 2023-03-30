from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class PromptGenerator:
    __PROMPT_SEPARATOR = "\n\n###\n\n"
    __COMPLETION_SEPARATOR = "###"
    COMPLETION_START = " "
    PROMPT_KEY = "prompt"
    COMPLETION_KEY = "completion"
    pos_class = "yes"
    neg_class = "no"
    base_prompt = "Are these two artifacts related?"
    artifact_prompt_format = "\n1. {}\n2. {}"

    def generate(self, source_content: Any, target_content: Any, label: int) -> Dict[str, str]:
        """
        Generates the prompt and response
        :return: Dictionary containing the prompt and completion
        """
        artifact_prompt = self.artifact_prompt_format.format(source_content, target_content, label)
        prompt = f"{self.base_prompt}{artifact_prompt}{self.__PROMPT_SEPARATOR}"
        class_ = self.pos_class if label == 1 else self.neg_class
        completion = f"{self.COMPLETION_START}{class_}{self.__COMPLETION_SEPARATOR}"
        return {
            "prompt": prompt,
            "completion": completion
        }