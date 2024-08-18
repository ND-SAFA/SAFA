from abc import abstractmethod
from typing import Any, List

from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from gen_common.infra.base_object import BaseObject


class AbstractDataProcessor(BaseObject):

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
        pass
