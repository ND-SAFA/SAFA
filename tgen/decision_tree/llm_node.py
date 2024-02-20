from dataclasses import dataclass, field
from typing import Dict, Any, Callable

from tgen.common.constants.model_constants import get_best_default_llm_manager_short_context
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.decision_tree.abstract_node import AbstractNode
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.select_question_prompt import SelectQuestionPrompt


@dataclass
class LLMNode(AbstractNode):
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_short_context)
    input_variable_converter: Callable = None

    def create_prompt_builder(self, input_variables: Dict[str, Any]) -> PromptBuilder:
        """
        Creates the prompt builder for the LLM to make a decision at the current node.
        :param input_variables: Any variables to format the prompt with in a dictionary mapping var name to value.
        :return: The prompt builder for the LLM to make a decision at the current node.
        """
        prompt = SelectQuestionPrompt(categories=list(self.choices.keys()), question=self.description)
        prompt.format_value(**input_variables)
        builder = PromptBuilder([prompt])
        return builder

    def choose_branch(self, input_: Any) -> str:
        """
        Decides which path to take from the current node.
        :param input_: The unique input to the node.
        :return: The choice of the next branch.
        """
        input_variables = {"input": input_} if self.input_variable_converter is None else self.input_variable_converter(input_)
        prompt_builder = self.create_prompt_builder(input_variables)
        prompt = prompt_builder.build(self.llm_manager.prompt_args)[PromptKeys.PROMPT]
        res: GenerationResponse = self.llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                                           prompt=[prompt])
        choice = prompt_builder.parse_responses(res.batch_responses[0])
        return choice
