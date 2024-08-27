from typing import Any, Dict, List, Optional, Set, Tuple, Type

from langchain_anthropic.chat_models import ChatAnthropic
from langchain_anthropic.output_parsers import ToolsOutputParser
from langchain_core.documents.base import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai.chat_models.base import ChatOpenAI
from pydantic.main import BaseModel

from gen_common.constants import anthropic_constants, environment_constants
from gen_common.constants.environment_constants import ANTHROPIC_KEY, OPEN_AI_KEY
from gen_common.constants.graph_defaults import BASE_AGENT_DEFAULT_MODEL
from gen_common.constants.symbol_constants import EMPTY_STRING
from gen_common.graph.branches.paths.path_selector import PathSelector
from gen_common.graph.io.graph_state import GraphState, has_state_value
from gen_common.graph.io.graph_state_vars import GraphStateVars
from gen_common.graph.io.state_var import StateVar
from gen_common.graph.llm_tools.tool import ToolType
from gen_common.infra.t_threading.threading_state import MultiThreadState
from gen_common.llm.anthropic_exception_handler import anthropic_exception_handler
from gen_common.llm.prompts.input_prompt import InputPrompt
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_args import PromptArgs
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.response_managers.abstract_response_manager import AbstractResponseManager
from gen_common.util.dict_util import DictUtil
from gen_common.util.enum_util import EnumUtil
from gen_common.util.langchain_util import ExceptionOptions, LangchainUtil
from gen_common.util.pythonisms_util import default_mutable
from gen_common.util.reflection_util import ReflectionUtil
from gen_common.util.supported_enum import SupportedEnum


class SupportedLLMs(SupportedEnum):
    ANTHROPIC = ChatAnthropic
    OPENAI = ChatOpenAI


API_KEYS = {
    SupportedLLMs.ANTHROPIC: ANTHROPIC_KEY,
    SupportedLLMs.OPENAI: OPEN_AI_KEY
}


class BaseAgent:
    MULTI_THREAD_STATE = MultiThreadState(
        [],
        title=EMPTY_STRING,
        retries=set(),
        max_attempts=anthropic_constants.ANTHROPIC_MAX_RE_ATTEMPTS,
        collect_results=True,
        rpm=anthropic_constants.ANTHROPIC_MAX_RPM,
        exception_handlers=[anthropic_exception_handler]
    )

    @default_mutable()
    def __init__(self, system_prompt: Prompt | str | PathSelector,
                 response_manager: AbstractResponseManager = None,
                 chat_model_type: BaseChatModel | SupportedLLMs = SupportedLLMs.ANTHROPIC,
                 model_name: str = BASE_AGENT_DEFAULT_MODEL,
                 state_vars_for_context: List[StateVar] = None,
                 allowed_missing_state_vars: Set[StateVar] = None,
                 tools: List[ToolType] | PathSelector = None,
                 **model_args):
        """
        A  simple chat bot agent.
        :param system_prompt: The main task prompt given to the LLM.
        :param response_manager: Handles how the LLM should respond.
        :param chat_model_type: Defines the chat model class to use.
        :param model_name: The name of the specific model to use.
        :param system_prompt: The prompt given to the agent if provided.
        :param state_vars_for_context: State keys that are relevant to scoring.
        :param allowed_missing_state_vars: Set of state keys that are OK to be None or Empty.
        :param tools: The tools available to the LLM.
        :param model_args: Additional args for the model initialization.
        """
        self.response_manager = response_manager
        self.system_prompt = system_prompt
        self.__model = None
        self.vars_for_context = state_vars_for_context
        if environment_constants.IS_TEST:
            self.vars_for_context.append(GraphStateVars.THREAD_ID)
            allowed_missing_state_vars.add(GraphStateVars.THREAD_ID)
        self.allowed_missing_state_vars = allowed_missing_state_vars
        self.tools = tools
        self.chat_model_type = chat_model_type
        self.model_args = DictUtil.update_kwarg_values(model_args, model=model_name)

    def respond(self, state: GraphState, run_async: bool = False) -> BaseModel:
        """
        Agent responds to provided prompt.
        :param state: The current state.
        :param run_async: If True, runs in async mode else synchronously.
        :return: The Response model containing LLM response.
        """
        system_prompt = self._get_system_prompt(state)
        langchain_prompt = self._create_prompt(system_prompt, state)
        tools, tool_schemas = self._get_tools(state)
        response = self._get_response(langchain_prompt, tools, tool_schemas, run_async=run_async)
        return response

    def extract_answer(self, response_obj: BaseModel) -> Optional[str]:
        """
        If the LLM responded as expected, returns the result of the first response tag.
        :param response_obj: The response obj.
        :return: The response if as expected.
        """
        expected_response_type = self.get_response_manager().get_langgraph_model()
        if isinstance(response_obj, expected_response_type) and self.get_first_response_tag():
            return getattr(response_obj, self.get_first_response_tag(), None)

    def create_response_obj(self, response: str | Dict | List) -> BaseModel:
        """
        Creates a response model object from a response string or a dictionary of responses for each variable.
        :param response: The response string or a dictionary mapping variable name to its response.
        :return: The response model object.
        """
        expected_response_type = self.get_response_manager().get_langgraph_model()
        if isinstance(response, str):
            response = {self.get_first_response_tag(): response}
        elif isinstance(response, list):
            response_tags = self.get_response_manager().get_all_tag_ids()
            assert len(response) <= len(response_tags), f"Too many response vals: Expected {len(response_tags)}, Got {len(response)}"
            response = {response_tags[i]: res for i, res in enumerate(response)}
        return expected_response_type(**response)

    def get_first_response_tag(self) -> str:
        """
        Gets the response tag (or first response tag if more than one).
        :return: The response tag used when the model responds.
        """
        tags = self.get_response_manager().get_all_tag_ids()
        if tags:
            return tags[0]

    def get_response_manager(self) -> AbstractResponseManager:
        """
        Gets the response manager used for extracting model response.
        :return: The response manager used for extracting model response.
        """
        if self.response_manager:
            return self.response_manager
        elif self._get_system_prompt().response_manager.response_tag:
            return self._get_system_prompt().response_manager

    def _create_prompt(self, system_prompt: Prompt, state: GraphState) -> ChatPromptTemplate:
        """
        Constructs the prompt builder for the agent prompt.
        :param system_prompt: The main task prompt for the model.
        :param state: The current state.
        :return: The prompt builder for the grader prompt.
        """
        inputs = {}
        prompts = [system_prompt]

        for state_var in self.vars_for_context:

            if not has_state_value(state, state_var.var_name):
                assert state_var in self.allowed_missing_state_vars, f"Required key {state_var.var_name} not found in state"
                continue

            value = state_var.get_value(state)
            title = state_var.prompt_config.title

            if state_var.prompt_config.prompt_converter is not None:
                var_prompt = state_var.prompt_config.prompt_converter.convert(value, name=state_var.var_name, title=title)
                var_prompt = [var_prompt] if not isinstance(var_prompt, list) else var_prompt
                prompts.extend(var_prompt)
            elif state_var.prompt_config.include_in_message_prompt:
                prompts.append(InputPrompt(input_var=state_var.var_name, input_title=title))

            inputs[state_var.var_name] = value

        # Need to add response formatting as a separate prompt
        if self.response_manager and system_prompt.response_manager != self.response_manager:
            prompts.append(Prompt(response_manager=self.response_manager))

        prompt_builder = PromptBuilder(prompts)
        prompt = prompt_builder.build_as_langgraph(conversation=inputs.get(GraphStateVars.CHAT_HISTORY.var_name), **inputs)
        return prompt

    def _get_response(self, prompt: ChatPromptTemplate, tools: List[ToolType],
                      tool_schemas: List[Dict], run_async: bool = False) -> BaseModel:
        """
        Gets the response using the given response manager and specific inputs.
        :param prompt: The prompt used to get the response.
        :param tools: The tools provided to the model.
        :param tool_schemas: The schemas for each tool.
        :param run_async: If True, runs in async mode else synchronously.
        :return: The response model containing the LLM response.
        """
        agent = self._get_model().bind_tools(tool_schemas)
        output_parser = ToolsOutputParser(first_tool_only=True,
                                          pydantic_schemas=tools)
        chain = prompt | agent | output_parser
        response, attempts = None, 0

        while attempts < 1 or isinstance(response, Exception):
            if run_async:
                self.MULTI_THREAD_STATE.add_work("item")  # need to keep infinite work coming until prompt is completed
                self.MULTI_THREAD_STATE.get_work()

            response = LangchainUtil.optionally_run_async(chain, run_async, raise_exception=ExceptionOptions.SYNC_ONLY)
            if isinstance(response, Exception):
                is_handled = self.MULTI_THREAD_STATE.on_exception(response)
                if not (is_handled and self.MULTI_THREAD_STATE.below_attempt_threshold(attempts)):
                    raise response

            attempts += 1
        return response

    @default_mutable()
    def _get_tools(self, state: Dict = None) -> Tuple[List[ToolType], List[Dict]]:
        """
        Gets the tools provided to the model.
        :param state: The current state if necessary to select the tools.
        :return: The tools provided to the model.
        """
        ResponseModel = self.get_response_manager().get_langgraph_model()

        tools = []
        if isinstance(self.tools, PathSelector):
            tools = self.tools.select(state)
        elif self.tools:
            tools = self.tools
        if not isinstance(tools, list):
            tools = [tools]
        tools.append(ResponseModel)
        tool_schemas = [tool.to_schema(state) if hasattr(tool, "to_schema") else tool for tool in tools]
        return tools, tool_schemas

    @default_mutable()
    def _get_system_prompt(self, state: Dict = None) -> Prompt:
        """
        Gets the prompt to use as the system prompt.
        :param state: The current state if necessary to select prompt.
        :return: The prompt to use as the system prompt.
        """
        system_prompt = self.system_prompt
        if isinstance(system_prompt, PathSelector):
            system_prompt = system_prompt.select(state)
        if isinstance(system_prompt, str):
            return Prompt(system_prompt)
        assert isinstance(system_prompt, Prompt), f"System prompt must be of type {Prompt.__name__}, " \
                                                  f"found {system_prompt.__class__.__name__}"
        system_prompt.args.system_prompt = True
        return system_prompt

    @staticmethod
    def _requires_context_prompt(state_val: Any) -> bool:
        """
        Returns True if state value should be a context prompt.
        :param state_val: The state value.
        :return: True if state value should be a context prompt else False.
        """
        return isinstance(state_val, dict) \
            and ReflectionUtil.is_type(DictUtil.get_value_by_index(state_val), List[Document])

    @staticmethod
    def _get_llm_selected(chat_model_type: BaseChatModel | SupportedLLMs) -> Tuple[SupportedLLMs, Type[BaseChatModel]]:
        """
        Gets the LLM selected if it is a supported one (otherwise None) and ensures chat model type is a BaseChatModel.
        :param chat_model_type: Defines the chat model class to use.
        :return: The LLM selected if it is a supported one (otherwise None) and chat model type as BaseChatModel class.
        """
        if isinstance(chat_model_type, SupportedLLMs):
            llm_selected = chat_model_type
            chat_model_type = llm_selected.value
        else:
            llm_selected: SupportedLLMs = EnumUtil.get_enum_from_value(SupportedLLMs, chat_model_type)
        assert issubclass(chat_model_type, BaseChatModel), f"Unknown model type {chat_model_type.__name__}"
        return llm_selected, chat_model_type

    @staticmethod
    def _update_api_key(llm_selected: SupportedLLMs, model_args: Dict[str, Any]) -> None:
        """
        Updates the args to have the appropriate api key.
        :param llm_selected: The LLM selected if it is a supported one (otherwise None).
        :param model_args: Additional args for the model initialization.
        :return: None (updates directly)
        """
        if llm_selected is not None:
            param_name = f"{llm_selected.name.lower()}_api_key"
            model_args[param_name] = API_KEYS.get(llm_selected)

    def _get_model(self) -> BaseChatModel:
        """
        Gets the chat model to use.
        :return: The chat model.
        """
        if not self.__model:
            self.__model = self._create_model(self.chat_model_type, **self.model_args)
        return self.__model

    @staticmethod
    def _create_model(chat_model_type: BaseChatModel | SupportedLLMs, **model_args) -> BaseChatModel:
        """
        Creates the chat model to use.
        :param chat_model_type: Defines the chat model class to use.
        :param model_args: Additional args for the model initialization.
        """
        llm_selected, chat_model_type = BaseAgent._get_llm_selected(chat_model_type)
        BaseAgent._update_api_key(llm_selected, model_args)
        return chat_model_type(**model_args)
