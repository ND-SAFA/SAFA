import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Callable

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.model_constants import get_best_default_llm_manager_long_context
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.dict_util import DictUtil
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.pipeline.pipeline_args import PipelineArgs
from tgen.pipeline.state import State
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.select_question_prompt import SelectQuestionPrompt

PROMPT_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(0)))
DEFAULT_RESPONSE_TAG = "answer"


@dataclass
class LLMNode(AbstractNode):
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
    input_variable_converter: Callable = None
    response_manager_params: Dict = field(default_factory=dict)
    response_tag: str = field(init=False, default=DEFAULT_RESPONSE_TAG)

    def create_prompt_builder(self, args: PipelineArgs, state: State) -> PromptBuilder:
        """
        Creates the prompt builder for the LLM to make a decision at the current node.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: The prompt builder for the LLM to make a decision at the current node.
        """
        prompt = self.create_prompt()
        input_variables = self._get_input_variables(args, state)
        prompt.format_value(**input_variables)
        builder = PromptBuilder([prompt])
        return builder

    def create_prompt(self) -> Prompt:
        """
        Creates the prompt used to probe the LLM to make a choice.
        :return: The prompt.
        """
        self.response_tag = DictUtil.get_kwarg_values(self.response_manager_params, response_tag=self.response_tag, pop=True)
        if len(self.branches) == 1:
            prompt = Prompt(self.description, response_manager=PromptResponseManager(response_tag=self.response_tag,
                                                                                     **self.response_manager_params))
        else:
            params = DictUtil.update_kwarg_values(response_format="Enclose your answer in {}", replace_existing=False,
                                                  orig_kwargs=self.response_manager_params)
            prompt = SelectQuestionPrompt(categories={choice: EMPTY_STRING for choice in self.branches.keys()},
                                          question=self.description,
                                          instructions="Answer with one of the following responses: ",
                                          response_tag=self.response_tag,
                                          multiple_responses_allowed=True,
                                          loose_response_validation=True,
                                          **params)

        prompt.args.prompt_id = PROMPT_ID
        return prompt

    def make_choice(self, args: PipelineArgs, state: State) -> Any:
        """
        Decides which path to take from the current node.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: The choice of the next branch.
        """
        prompt_builder = self.create_prompt_builder(args, state)
        prompt = prompt_builder.build(self.llm_manager.prompt_args)[PromptKeys.PROMPT]
        res: GenerationResponse = self.llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                                           prompt=[prompt])
        choice = prompt_builder.parse_responses(res.batch_responses[0])
        return self.get_choice_from_response(choice)

    def get_choice_from_response(self, parsed_res: Dict) -> str:
        """
        Gets the model's choice from the parsed response.
        :param parsed_res: The parsed response.
        :return: The model's choice from the parsed response.
        """
        return self.parse_response(parsed_res, self.response_tag)

    @staticmethod
    def parse_response(parsed_res: Dict, response_tag: str = DEFAULT_RESPONSE_TAG) -> str:
        """
        Gets the model's choice from the parsed response.
        :param parsed_res: The parsed response.
        :param response_tag: The response tag used to enclose the choice.
        :return: The model's choice from the parsed response.
        """
        res = parsed_res[PROMPT_ID][response_tag]
        return res[0] if len(res) > 0 else None

    def get_formatted_question(self, input_: Any, **kwargs) -> str:
        """
        Formats the question using the given input.
        :param input_: The input to the question.
        :return: The question formatted using the given input.
        """
        question = self.description
        if self.input_variable_converter:
            format_vars = self.input_variable_converter(input_, **kwargs)
            question = question.format(**format_vars)
        return question

    def _get_input_variables(self, args: PipelineArgs, state: State) -> Dict[str, Any]:
        """
        Gets the input variables needed for the prompt.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: Dictionary mapping variable name to value.
        """
        input_variables = self.input_variable_converter(args, state) if self.input_variable_converter is not None else {}
        additional_kwargs = DataclassUtil.convert_to_dict(args)
        additional_kwargs.update(DataclassUtil.convert_to_dict(state))
        input_variables = DictUtil.update_kwarg_values(input_variables, replace_existing=False, **additional_kwargs)
        return input_variables
