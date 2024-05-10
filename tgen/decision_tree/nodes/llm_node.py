import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Callable

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.model_constants import get_best_default_llm_manager_short_context
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.select_question_prompt import SelectQuestionPrompt

PROMPT_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(0)))
RESPONSE_TAG = "answer"


@dataclass
class LLMNode(AbstractNode):
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_short_context)
    input_variable_converter: Callable = None

    def create_prompt_builder(self, input_: Any) -> PromptBuilder:
        """
        Creates the prompt builder for the LLM to make a decision at the current node.
        :param input_: The input to the node.
        :return: The prompt builder for the LLM to make a decision at the current node.
        """
        input_variables = {"input": input_} if self.input_variable_converter is None else self.input_variable_converter(input_)
        prompt = SelectQuestionPrompt(categories={choice: EMPTY_STRING for choice in self.branches.keys()},
                                      question=self.description,
                                      instructions="Answer with one of the following responses: ",
                                      response_format="Enclose your answer in {}",
                                      response_tag=RESPONSE_TAG,
                                      loose_response_validation=True)
        prompt.args.prompt_id = PROMPT_ID
        prompt.format_value(**input_variables)
        builder = PromptBuilder([prompt])
        return builder

    def make_choice(self, input_: Any) -> str:
        """
        Decides which path to take from the current node.
        :param input_: The unique input to the node.
        :return: The choice of the next branch.
        """
        prompt_builder = self.create_prompt_builder(input_)
        prompt = prompt_builder.build(self.llm_manager.prompt_args)[PromptKeys.PROMPT]
        res: GenerationResponse = self.llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                                           prompt=[prompt])
        choice = prompt_builder.parse_responses(res.batch_responses[0])
        return self.get_choice_from_response(choice)

    @staticmethod
    def get_choice_from_response(parsed_res: Dict) -> str:
        """
        Gets the model's choice from the parsed response.
        :param parsed_res: The parsed response.
        :return: The model's choice from the parsed response.
        """
        res = parsed_res[PROMPT_ID][RESPONSE_TAG]
        return res[0] if len(res) > 0 else None

    def get_formatted_question(self, input_: Any) -> str:
        """
        Formats the question using the given input.
        :param input_: The input to the question.
        :return: The question formatted using the given input.
        """
        question = self.description
        if self.input_variable_converter:
            format_vars = self.input_variable_converter(input_)
            question = question.format(**format_vars)
        return question
