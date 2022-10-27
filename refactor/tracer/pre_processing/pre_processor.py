from typing import Dict, List, Tuple, Union, Type

from tracer.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep
from tracer.pre_processing.pre_processing_option import PreProcessingOption


class PreProcessor:

    def __init__(self, selected_options: List[PreProcessingOption] = None, **kwargs):
        """
        Handles Pre-Processing
        :param selected_options: the selected pre-process options to run
        """
        selected_options = selected_options if selected_options else []
        self.ordered_before_steps, self.ordered_regular_steps = self._get_ordered_steps(selected_options, **kwargs)

    @staticmethod
    def _get_ordered_steps(selected_options: List[PreProcessingOption], **kwargs) \
            -> Tuple[List[AbstractPreProcessingStep], List[AbstractPreProcessingStep]]:
        """
        Gets the steps in the order they should be run
        :param selected_options: the selected pre-process options to run
        :return: the ordered list of steps to run before and the ordered list of steps to run after words are split into word list
        """
        before_steps = []
        regular_steps = []
        for option in selected_options:
            step_class = option.value
            step_params = PreProcessor._get_step_params(step_class, **kwargs)
            step = step_class(**step_params)
            if step.run_before:
                before_steps.append(step)
            else:
                regular_steps.append(step)
        return PreProcessor._order_steps(before_steps), PreProcessor._order_steps(regular_steps)

    @staticmethod
    def _get_step_params(step_class: Type[AbstractPreProcessingStep], **kwargs) -> Dict[str, any]:
        """
        Creates a dictionary of the parameters used to initialize a pre-processing step
        :param step_class: the class of the pre-processing step
        :return: a dictionary of the parameters used to initialize a pre-processing step
        """
        step_params = {}
        for name, value in kwargs.items():
            if hasattr(step_class, name):
                step_params[name] = value
        return step_params

    @staticmethod
    def _order_steps(steps: List[AbstractPreProcessingStep]) -> List[AbstractPreProcessingStep]:
        """
        Orders the steps in the order they should be run
        :param steps: a list of unordered steps
        :return: the list of steps in order
        """
        return sorted(steps)

    @staticmethod
    def _get_word_list(content: str) -> List[str]:
        """
        Splits the content into its individual words
        :param content: the content as a string
        :return: the list of words in the content
        """
        return content.split()

    @staticmethod
    def _reconstruct_content(word_list: List[str]) -> str:
        """
        Reconstructs the list of individual words into a string
        :param word_list: the list of words in the content
        :return: the content as a string
        """
        return " ".join(word_list)

    @staticmethod
    def _run_steps(steps: List[AbstractPreProcessingStep], run_args: Union[List[str], str]) -> Union[List[str], str]:
        """
        Runs all given steps with the given run_arg
        :param steps: list of steps to run
        :param run_args: the arguments to use when running
        :return: the results from the steps
        """
        for step in steps:
            run_args = step.run(run_args)
        return run_args

    def run(self, tokens: List[str]) -> List[str]:
        """
        Runs the selected-preprocessing steps on each artifact content
        :param tokens: a list of artifact content strings
        :return: list of processed artifact content strings
        """
        processed_tokens = []
        for content in tokens:
            processed_txt = self._run_steps(self.ordered_before_steps, content)
            processed_word_list = self._run_steps(self.ordered_regular_steps, self._get_word_list(processed_txt))
            processed_tokens.append(PreProcessor._reconstruct_content(processed_word_list))
        return processed_tokens
