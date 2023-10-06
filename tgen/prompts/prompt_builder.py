from typing import Any, Dict, List

from tgen.common.util.enum_util import EnumDict
from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_config import PromptConfig


class PromptBuilder:

    def __init__(self, prompts: List[Prompt] = None):
        """
        Constructs prompt creator with prompt arguments as configuration.
        :param prompts: The list of prompts to use to build the final prompt
        """
        self.prompts = prompts if prompts else []
        self._create_config()

    def build(self, model_format_args: PromptArgs, correct_completion: Any = EMPTY_STRING, **prompt_kwargs, ) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :param model_format_args: Defines the formatting specific to the model
        :param correct_completion: The correct completion that the model should produce
        :return: Dictionary containing the prompt and completion
        """
        built_prompts = [prompt.build(**prompt_kwargs) for prompt in self.prompts]
        base_prompt = NEW_LINE.join(built_prompts)
        prompt = self._format_prompt_for_model(base_prompt, prompt_args=model_format_args)
        completion = self._format_completion(correct_completion, prompt_args=model_format_args)
        return EnumDict({
            PromptKeys.PROMPT: prompt,
            PromptKeys.COMPLETION: completion
        })

    def add_prompt(self, prompt: Prompt, i: int = None) -> None:
        """
        Adds a prompt at the given index (appens to end by defailt
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
            if prompt.id == prompt_id:
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
        return {prompt.id: prompt.parse_response(res) for prompt in self.prompts}

    def _create_config(self) -> PromptConfig:
        """
        Creates a config for the given prompts
        :return: The configuration for the prompt builder
        """
        self.config = PromptConfig(requires_trace_per_prompt=False,
                                   requires_artifact_per_prompt=False,
                                   requires_all_artifacts=False)
        for prompt in self.prompts:
            if isinstance(prompt, MultiArtifactPrompt):
                if prompt.data_type == MultiArtifactPrompt.DataType.TRACES:
                    self.config.requires_trace_per_prompt = True
                if prompt.data_type == MultiArtifactPrompt.DataType.ARTIFACT:
                    self.config.requires_all_artifacts = True
            elif isinstance(prompt, ArtifactPrompt):
                self.config.requires_artifact_per_prompt = True
        return self.config

    @staticmethod
    def _format_prompt_for_model(base_prompt: str, prompt_args: PromptArgs) -> str:
        """
        Formats the prompt with expected prefix + suffix tokens
        :param base_prompt: The base prompt
        :param prompt_args: The arguments for properly formatting the prompt
        :return: The formatted prompt
        """
        return f"{prompt_args.prompt_prefix}{base_prompt}{prompt_args.prompt_suffix}"

    @staticmethod
    def _format_completion(base_completion: str, prompt_args: PromptArgs) -> str:
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
