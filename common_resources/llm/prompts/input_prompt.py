from common_resources.llm.prompts.prompt import Prompt
from common_resources.llm.prompts.prompt_args import PromptArgs
from common_resources.tools.util.str_util import StrUtil


class InputPrompt(Prompt):

    def __init__(self, input_var: str, input_title: str = None):
        """
        Represents some input to the model.
        :param input_var: The name of the input variable.
        :param input_title: The title displayed to LLM above variable.
        """
        super().__init__(value=StrUtil.get_format_symbol(input_var),
                         prompt_args=PromptArgs(title=input_title, structure_with_new_lines=True))
