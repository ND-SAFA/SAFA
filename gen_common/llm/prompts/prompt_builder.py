import uuid
from typing import Any, Dict, List, Tuple

from langchain_core.prompts import ChatPromptTemplate

from gen_common.constants import EMPTY_STRING, NEW_LINE
from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.llm.abstract_llm_manager import PromptRoles
from gen_common.llm.prompts.artifact_prompt import ArtifactPrompt
from gen_common.llm.prompts.context_prompt import ContextPrompt
from gen_common.llm.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_config import PromptConfig
from gen_common.util import EnumDict, StrUtil, default_mutable


class PromptBuilder:

    def __init__(self, prompts: List[Prompt] = None, **format_variables):
        """
        Constructs prompt creator with prompt arguments as configuration.
        :param prompts: The list of prompts to use to build the final prompt
        :param format_variables: A dictionary mapping format key to a list of values corresponding to each prompt that will be built
        """
        self.prompts = prompts if prompts else []
        self.format_variables = format_variables if format_variables else {}
        self._n_built = 0
        self._create_config()
        self.id = str(uuid.uuid4())

    def build(self, model_format_args: LLMPromptBuildArgs, correct_completion: Any = EMPTY_STRING,
              **prompt_kwargs) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :param model_format_args: Defines the formatting specific to the model
        :param correct_completion: The correct completion that the model should produce
        :return: Dictionary containing the prompt and completion
        """
        format_vars = {key: val[self._n_built] for key, val in self.format_variables.items() if len(val) > self._n_built}
        prompt_kwargs.update(format_vars)
        build_all = not model_format_args.build_system_prompts
        system_prompt = self._build_prompts(build_all=build_all, only_use_system_prompts=True, **prompt_kwargs) \
            if not build_all else None
        base_prompt = self._build_prompts(build_all=build_all, only_use_system_prompts=False, **prompt_kwargs)
        prompt = self.format_prompt_for_model(base_prompt, prompt_args=model_format_args)
        completion = self._format_completion(correct_completion, prompt_args=model_format_args)
        self._n_built += 1
        return EnumDict({
            PromptKeys.PROMPT: prompt,
            PromptKeys.COMPLETION: completion,
            PromptKeys.PROMPT_BUILDER_ID: self.id,
            PromptKeys.SYSTEM: system_prompt,
        })

    def build_as_langgraph(self, model_format_args: LLMPromptBuildArgs = None, correct_completion: Any = EMPTY_STRING,
                           conversation: List[Tuple[str, str]] = None,
                           **prompt_kwargs) -> ChatPromptTemplate:
        """
        Generates the prompt for langgraph.
        :param model_format_args: Defines the formatting specific to the model
        :param correct_completion: The correct completion that the model should produce
        :param conversation: List of (role, message) tuples for previous messages.
        :return: Langgraph chat template.
        """
        model_format_args = LLMPromptBuildArgs() if not model_format_args else model_format_args
        built_prompt = self.build(model_format_args, correct_completion, partial_format_instructions=True, **prompt_kwargs)
        partial_variables = {}
        for prompt in self.prompts:
            partial_variables.update(prompt.response_instructions_variables)
        return self.to_langgraph(built_prompt, conversation, partial_variables)

    def add_prompt(self, prompt: Prompt, i: int = None) -> None:
        """
        Adds a prompt at the given index (appends to end by default)
        :param prompt: The prompt to add
        :param i: The index to insert the prompt
        :return: None
        """
        if i is None or i == len(self.prompts):
            self.prompts.append(prompt)
        else:
            self.prompts.insert(i, prompt)
        self._create_config()

    def format_prompts_with_var(self, **kwargs) -> None:
        """
        Formats all prompts that have missing values (identified by '{$var_name$}') that are provided in the kwargs
        :param kwargs: Contains var_name to value mappings to format the prompts with
        :return: None
        """
        for prompt in self.prompts:
            prompt.format_value(**kwargs)

    def remove_prompt(self, i: int = None, prompt_id: str = None) -> None:
        """
        Removes the prompt at the given index or removes the prompt with the given id
        :param i: The index of the prompt to remove
        :param prompt_id: The id of the prompt to remove
        :return: None
        """
        if prompt_id is not None:
            i = self.find_prompt_by_id(prompt_id)
            if i < 0:
                i = None
        if i is not None:
            self.prompts.pop(i)
            self._create_config()

    def find_prompt_by_id(self, prompt_id: str) -> int:
        """
        Finds a prompt by its id and returns the index
        :param prompt_id: The id of the prompt to find
        :return: The index of the prompt if it exists, else -1
        """
        for i, prompt in enumerate(self.prompts):
            if prompt.args.prompt_id == prompt_id:
                return i
        return -1

    def get_prompt(self, index: int) -> Prompt:
        """
        Gets the prompt by the index number
        :param index: The index
        :return: The prompt at the given index
        """
        return self.prompts[index]

    def get_prompt_by_id(self, prompt_id: str) -> Prompt:
        """
        Finds a prompt by its id
        :param prompt_id: The id of the prompt to find
        :return: The prompt if it exists, else None
        """
        i = self.find_prompt_by_id(prompt_id)
        return self.prompts[i] if i >= 0 else None

    def get_all_prompts(self) -> List[Prompt]:
        """
        Gets all prompts
        :return: The list of prompts
        """
        return self.prompts

    def parse_responses(self, res: str) -> Dict[str, Any]:
        """
        Extracts the answers from the model response
        :param res: The model response
        :return: A dictionary mapping prompt id to its answers
        """
        return {prompt.args.prompt_id: prompt.parse_response(res) for prompt in self.prompts}

    def get_response_prompts(self) -> List[Prompt]:
        """
        Gets any prompts that expect a response from the LLM.
        :return: A list of prompts with response tags.
        """
        return [p for p in self.prompts if p.response_manager.response_tag]

    def _build_prompts(self, build_all: bool = True, only_use_system_prompts: bool = False, **prompt_kwargs) -> str:
        """
        Builds each prompt and combines them to create one final prompt.
        :param build_all: If True, builds all prompts regardless if system prompt or not.
        :param only_use_system_prompts: If True, only builds system prompts.
        :param prompt_kwargs: Args for building each promtp.
        :return: All prompts built and combined into one final prompt.
        """
        built_prompts = [prompt.build(**prompt_kwargs) for prompt in self.prompts
                         if prompt.args.system_prompt == only_use_system_prompts or build_all]
        base_prompt = NEW_LINE.join(built_prompts) if built_prompts or not only_use_system_prompts else None
        return base_prompt

    def _create_config(self) -> PromptConfig:
        """
        Creates a config for the given prompts
        :return: The configuration for the prompt builder
        """
        self.config = PromptConfig(requires_trace_per_prompt=False,
                                   requires_artifact_per_prompt=False,
                                   requires_all_artifacts=False)
        for prompt in self.prompts:
            if isinstance(prompt, ContextPrompt):
                self.config.requires_artifact_per_prompt = True
            elif isinstance(prompt, MultiArtifactPrompt):
                if prompt.data_type == MultiArtifactPrompt.DataType.TRACES:
                    self.config.requires_trace_per_prompt = True
                if prompt.data_type == MultiArtifactPrompt.DataType.ARTIFACT:
                    self.config.requires_all_artifacts = True
            elif isinstance(prompt, ArtifactPrompt):
                self.config.requires_artifact_per_prompt = True
        return self.config

    @staticmethod
    @default_mutable()
    def to_langgraph(built_prompt: EnumDict, conversation: List[Tuple[str, str]] = None,
                     partial_variables: Dict = None) -> ChatPromptTemplate:
        """
        Converts a prompt to the langgraph format.
        :param built_prompt: Output of the 'build method' which contains prompt attributes such as system and user prompt.
        :param conversation: List of (role, message) tuples for previous messages.
        :param partial_variables: Dictionary containing all partial variables.
        :return: A langgraph Chat Prompt Template.
        """
        system, prompt = built_prompt.get(PromptKeys.SYSTEM), built_prompt.get(PromptKeys.PROMPT)
        messages = []
        if system:
            messages.append((PromptKeys.SYSTEM.value, system))
        if conversation:
            messages.extend(conversation)
        if prompt:
            messages.append((PromptRoles.HUMAN, prompt))
        chat_template = ChatPromptTemplate.from_messages(messages)
        chat_template.partial_variables = partial_variables
        chat_template.input_variables = list(set(chat_template.input_variables).difference(partial_variables))
        return chat_template

    @staticmethod
    def format_prompt_for_model(base_prompt: str, prompt_args: LLMPromptBuildArgs) -> str:
        """
        Formats the prompt with expected prefix + suffix tokens
        :param base_prompt: The base prompt
        :param prompt_args: The arguments for properly formatting the prompt
        :return: The formatted prompt
        """
        prefix = prompt_args.prompt_prefix if not base_prompt.startswith(prompt_args.prompt_prefix) else EMPTY_STRING
        suffix = prompt_args.prompt_suffix if not base_prompt.endswith(prompt_args.prompt_prefix) else EMPTY_STRING
        return f"{prefix}{base_prompt}{suffix}"

    @staticmethod
    def remove_format_for_model_from_prompt(base_prompt: str, prompt_args: LLMPromptBuildArgs) -> str:
        """
        Formats the prompt with expected prefix + suffix tokens
        :param base_prompt: The base prompt
        :param prompt_args: The arguments for properly formatting the prompt
        :return: The formatted prompt
        """
        base_prompt = StrUtil.remove_substring(base_prompt, prompt_args.prompt_prefix, only_if_startswith=True)
        base_prompt = StrUtil.remove_substring(base_prompt, prompt_args.prompt_suffix, only_if_endswith=True)
        return base_prompt

    @staticmethod
    def _format_completion(base_completion: str, prompt_args: LLMPromptBuildArgs) -> str:
        """
        Formats the completion with expected prefix + suffix tokens
        :param base_completion: The base completion
        :param prompt_args: The arguments for properly formatting the prompt
        :return: The formatted completion
        """
        if not base_completion:
            return EMPTY_STRING
        return f"{prompt_args.completion_prefix}{base_completion}{prompt_args.completion_suffix}"

    def __len__(self) -> int:
        """
        Returns the number of prompts in the builder
        :return: The number of prompts in the builder
        """
        return len(self.prompts)
