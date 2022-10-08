from typing import Dict, List, Union, Tuple

from common.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep, AbstractPreProcessingBeforeStep
from common.pre_processing.pre_processing_options import PreProcessingOptions


class PreProcessor:

    OPTION2PARAM = {PreProcessingOptions.REPLACE_WORDS: "word_replace_mappings",
                    PreProcessingOptions.FILTER_MIN_LENGTH: "min_length"}

    def __init__(self, selected_options: Dict[PreProcessingOptions, bool], **kwargs):
        step_params = self._get_step_params(**kwargs)
        self.ordered_before_steps, self.ordered_regular_steps = self._get_ordered_steps(selected_options, step_params)

    @staticmethod
    def _get_ordered_steps(selected_options: Dict[PreProcessingOptions, bool], step_params: Dict[PreProcessingOptions, Dict]) \
            -> Tuple[List[AbstractPreProcessingStep], List[AbstractPreProcessingStep]]:
        before_steps = []
        regular_steps = []
        for option, should_run in selected_options.items():
            if should_run:
                step = option.value(**step_params[option]) if option in step_params else option.value()
                if step.run_before:
                    before_steps.append(step)
                else:
                    regular_steps.append(step)
        return PreProcessor._order_steps(before_steps), PreProcessor._order_steps(regular_steps)

    @staticmethod
    def _order_steps(steps: List[AbstractPreProcessingStep]) -> List[AbstractPreProcessingStep]:
        return sorted(steps)

    @staticmethod
    def _get_step_params(**kwargs):
        step_params = {}
        for option, param in PreProcessor.OPTION2PARAM.items():
            if param in kwargs:
                step_params[option] = {param: kwargs[param]}
        return step_params

    @staticmethod
    def _get_word_list(content: str) -> List[str]:
        return content.split()

    @staticmethod
    def _reconstruct_content(word_list: List[str]) -> str:
        return " ".join(word_list)

    @staticmethod
    def _run_steps(steps: List[AbstractPreProcessingStep], run_args: Union[List[str], str]) -> Union[List[str], str]:
        for step in steps:
            run_args = step.run(run_args)
        return run_args

    def run(self, artifact_content: List[str]) -> List[str]:
        processed_content = []
        for content in artifact_content:
            processed_txt = self._run_steps(self.ordered_before_steps, content)
            processed_word_list = self._run_steps(self.ordered_regular_steps, self._get_word_list(processed_txt))
            processed_content.append(PreProcessor._reconstruct_content(processed_word_list))
        return processed_content
