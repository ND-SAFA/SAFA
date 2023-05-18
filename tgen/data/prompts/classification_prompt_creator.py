from typing import Union

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.util.enum_util import EnumDict


class ClassificationPromptCreator(AbstractPromptCreator):
    """
    Creates prompt datasets used for classification for some defined AI libray.
    """

    def __init__(self, prompt_args: PromptArgs = None, pos_class: str = "Yes", neg_class: str = "No",
                 artifact_prompt_format: str = "\n1. {}\n\n2. {}",
                 base_prompt: Union[str, SupportedPrompts] = SupportedPrompts.CLASSIFICATION):
        """
        Constructs classification prompt creator
        :param prompt_args: The arguments used to construct prompts.
        :param pos_class: The label used for positive classes.
        :param neg_class: The label used for negative classes.
        :param artifact_prompt_format: The prompt used for formatting source and target artifacts.
        :param base_prompt: The base classification prompt to use.
        """
        if prompt_args is None:
            from tgen.models.llm.open_ai_manager import OpenAIManager  # used to automatically have args for tests
            prompt_args = OpenAIManager.prompt_args
        super().__init__(prompt_args, base_prompt)
        self.pos_class = pos_class
        self.neg_class = neg_class
        self.artifact_prompt_format = artifact_prompt_format

    def create(self, target_content: str, source_content: str = EMPTY_STRING, label: int = None) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :param source_content: The content of the source artifact
        :param target_content: The content of the target artifact
        :param label: The label of the link
        :return: Dictionary containing the prompt and completion
        """
        artifact_prompt = self.artifact_prompt_format.format(source_content, target_content, label)
        prompt = f"{self.base_prompt}{artifact_prompt}"
        class_ = self.pos_class if label == 1 else self.neg_class
        prompt = self.generate_base(prompt, class_)
        return prompt
