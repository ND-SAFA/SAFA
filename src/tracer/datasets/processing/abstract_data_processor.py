from abc import abstractmethod
from typing import List, Iterable, Any

from tracer.datasets.processing.abstract_data_processing_step import AbstractDataProcessingStep


class AbstractDataProcessor:

    def __init__(self, steps: List[AbstractDataProcessingStep]):
        """
        Handles Pre-Processing
        :param steps: the selected pre-process options to run
        """
        self.steps = steps if steps else []
        self.ordered_steps = self._order_steps(steps)

    @staticmethod
    def _order_steps(steps: List[AbstractDataProcessingStep]) -> List[AbstractDataProcessingStep]:
        """
        Orders the steps in the order they should be run
        :param steps: a list of unordered steps
        :return: the list of steps in order
        """
        return sorted(steps)

    @abstractmethod
    def run(self, content_list: List, **kwargs) -> Any:
        """
        Runs the selected-processing steps on the artifact body
        :param content_list: a list of artifact body strings
        :return: the results
        """
        processed = []
        word_lists = [AbstractDataProcessingStep.get_word_list(content) for content in content_list]
        for word_list in word_lists:
            processed_word_list = word_list
            for step in self.ordered_steps:
                processed_word_list = step.run(processed_word_list)
            processed.append(processed_word_list)
        return [AbstractDataProcessingStep.reconstruct_content(word_list) for word_list in processed]
