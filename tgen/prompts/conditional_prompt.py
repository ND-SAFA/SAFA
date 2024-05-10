from typing import Callable, List

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.prompts.multi_prompt import MultiPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_response_manager import PromptResponseManager


class ConditionalPrompt(MultiPrompt):

    def __init__(self, candidate_prompts: List[Prompt], prompt_selector: Callable,
                 prompt_args: PromptArgs = None, response_manager: PromptResponseManager = None):
        """
        Selects a prompt based on some condition.
        :param candidate_prompts: List of all candidate prompts that can be chosen
        :param prompt_selector: The prompt will selected based on the conditional value
        :param prompt_args: Any additional params for the prompt class
        :param response_manager: Handles parsing the response from the LLM.
        """
        self.prompt_selector = prompt_selector
        super().__init__(main_prompt_value=EMPTY_STRING, child_prompts=candidate_prompts, prompt_args=prompt_args,
                         response_manager=response_manager)

    def _build(self, **kwargs) -> str:
        """
        Used to fulfill api, specific method of building for a prompt may be defined in child classes
        :param kwargs: Any additional arguments for the prompt
        :return: The formatted prompt
        """
        selected_prompt_index = int(self.prompt_selector(kwargs))
        if 0 <= selected_prompt_index < len(self.child_prompts):
            return self.child_prompts[selected_prompt_index].build(**kwargs)
        return EMPTY_STRING
