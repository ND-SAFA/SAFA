from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.util.enum_util import EnumDict


class GenerationPromptCreator(AbstractPromptCreator):
    """
    Constructs prompt datasets for generation tasks.
    """

    def __init__(self, prompt_args: PromptArgs = None, base_prompt: SupportedPrompts = SupportedPrompts.SYSTEM_REQUIREMENT_CREATION):
        """
        Constructs generation prompt dataset creator for specified library.
        :param prompt_args: The arguments used for creating prompts. Defaults to OpenAI format.
        :param base_prompt: The base prompt to use to generate final prompt.
        """
        if prompt_args is None:
            prompt_args = OpenAiArgs.prompt_args
        super().__init__(prompt_args=prompt_args, base_prompt=base_prompt),

    def create(self, source_content: str, target_content: str, **kwargs) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :param source_content: The content of the source artifact
        :param target_content: The content of the target artifact
        :return: Dictionary containing the prompt and completion
        """
        return self.generate_base(self.base_prompt.format(target_content), source_content)
