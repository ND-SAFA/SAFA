import enum
import math
from abc import ABC, abstractmethod
from functools import total_ordering
from typing import List, Type

from gen_common.constants import SPACE
from gen_common.util import BaseObject
from gen_common.util.override import overrides


class ProcessingOrder(enum.Enum):
    BEFORE_WORD_SPLIT = -1
    FIRST = 0
    NEXT = 1
    ANY = 100
    LAST = math.inf


@total_ordering
class AbstractDataProcessingStep(BaseObject, ABC):
    def __init__(self, order: ProcessingOrder = ProcessingOrder.ANY):
        """
        :param order: the order the step should be run in
        """
        self.order = order

    @abstractmethod
    def run(self, data_entries: List, **kwargs) -> List:
        """
        Runs the pre-processing step on a given word_list
        :param data_entries: the list of words to process
        :return: the processed word_list
        """
        pass

    @staticmethod
    def get_word_list(content: str) -> List[str]:
        """
        Splits the content into its individual words
        :param content: the content as a string
        :return: the list of words in the content
        """
        return content.split() if isinstance(content, str) else []

    @staticmethod
    def reconstruct_content(word_list: List[str]) -> str:
        """
        Reconstructs the list of individual words into a string
        :param word_list: the list of words in the content
        :return: the content as a string
        """
        return SPACE.join(word_list)

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from gen_common.data.processing.cleaning.supported_data_cleaning_step import SupportedDataCleaningStep
        from gen_common.data.processing.augmentation.supported_data_augmentation_step import SupportedAugmentationStep
        if child_class_name in SupportedDataCleaningStep.__members__:
            return SupportedDataCleaningStep
        return SupportedAugmentationStep

    def __eq__(self, other) -> bool:
        """
        Compares the order of the steps
        :param other: the other step to compare
        :return: True if both steps can occur in interchangeable order
        """
        return self.order.value == other.order.value

    def __lt__(self, other) -> bool:
        """
        Compares the order of the steps
        :param other: the other step to compare
        :return: True if the current step should occur before the other
        """
        return self.order.value < other.order.value
