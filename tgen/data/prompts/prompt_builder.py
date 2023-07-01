from typing import List, Tuple, Any, Dict

from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.util.enum_util import EnumDict
from tgen.util.llm_response_util import LLMResponseUtil


class PromptBuilder:

    def __init__(self, prompts: List[Prompt]):
        """
        Constructs prompt creator with prompt arguments as configuration.
        :param prompts: The list of prompts to use to build the final prompt
        """
        self.prompts = prompts
        self.requires_traces, self.requires_artifacts = self._check_requirements(self.prompts)

    def build(self, prompt_args: PromptArgs, correct_completion: Any = EMPTY_STRING, **prompt_kwargs,) -> EnumDict[str, str]:
        """
        Generates the prompt and response
        :param correct_completion: The correct completion that the model should produce
        :return: Dictionary containing the prompt and completion
        """
        built_prompts = [prompt.build(**prompt_kwargs) for prompt in self.prompts]
        base_prompt = NEW_LINE.join(built_prompts)
        prompt = self._format_prompt_for_model(base_prompt, prompt_args=prompt_args)
        completion = self._format_completion(correct_completion, prompt_args=prompt_args)
        return EnumDict({
            PromptKeys.PROMPT: prompt,
            PromptKeys.COMPLETION: completion
        })
    
    def format_prompts_with_var(self, **kwargs) -> None:
        """
        Formats all prompts that have missing values (identified by '{$var_name$}') that are provided in the kwargs
        :param kwargs: Contains var_name to value mappings to format the prompts with
        :return: None
        """
        for prompt in self.prompts:
            prompt.format_value(**kwargs)

    def parse_responses(self, res: str) -> Dict[str, Any]:
        """
        Extracts the answers from the model response
        :param res: The model response
        :return: A dictionary mapping prompt id to its answers
        """
        tags = self._get_response_tag_to_prompt_indices()
        tag2response = LLMResponseUtil.extract_labels(res, list(tags.keys())) 
        responses = [[None] * len(self.prompts)]
        for label, response in tag2response.items():
            prompt_indices = tags[label]
            for i, p_i in enumerate(prompt_indices):
                if i >= len(response):
                    e = AssertionError(f"Received too few responses for {label}")
                    responses[p_i] = self.prompts[p_i].parse_response_on_failure("", e)
                else:
                    responses[p_i] = self.prompts[p_i].parse_response(response[i])
        return {prompt.id: responses[i] for i, prompt in enumerate(self.prompts)}

    def _get_response_tag_to_prompt_indices(self) -> Dict[str, List[int]]:
        """
        Gets the response tag for each prompt and maps it to the corresponding indices of the prompt
        :return: A mapping of tag to prompt indices
        """
        tags = {}
        for i, prompt in enumerate(self.prompts):
            tag = prompt.response_tag
            if tag:
                if tag not in tags:
                    tags[tag] = []
                tags[tag].append(i)
        return tags

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

    @staticmethod
    def _check_requirements(prompts: List[Prompt]) -> Tuple[bool, bool]:
        """
        Determines if traces or artifacts are needed for prompt
        :return: Tuple containing a bool representing if traces are required and bool for artifacts requirement
        """
        requires_traces, requires_artifacts = False, False
        for prompt in prompts:
            if prompt.requires_traces:
                requires_traces = True
            if prompt.requires_artifacts:
                requires_artifacts = True
        return requires_traces, requires_artifacts
