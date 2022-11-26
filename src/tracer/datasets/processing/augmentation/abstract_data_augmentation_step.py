import random
from abc import ABC, abstractmethod
from typing import List, Iterable, Tuple, Union

from config.override import overrides
from tracer.datasets.processing.abstract_data_processing_step import AbstractDataProcessingStep, ProcessingOrder


class AbstractDataAugmentationStep(AbstractDataProcessingStep, ABC):
    AUGMENTATION_RESULT = Iterable[Tuple[Tuple[str], int]]

    def __init__(self, percent_to_weight: float, order: ProcessingOrder = ProcessingOrder.ANY):
        """
        :param percent_to_weight: the percentage of the data that the augmentation step will augment
        :param order: the order the step should be run in
        """
        self.percent_to_weight = percent_to_weight
        super().__init__(order)

    @overrides(AbstractDataProcessingStep)
    def run(self, data_entries: List, n_needed: int) -> AUGMENTATION_RESULT:
        """
        Runs the data augmentation to obtain a larger dataset
        :param data_entries: a list of tokens as source, target pairs
        :param n_needed: the number of new data entries needed
        :return: list of containing the augmented data and the orig indices for the entry
        """
        n_orig = len(data_entries)
        n_sample = self._get_number_to_sample(n_orig, 0, n_needed)
        augmented_data = []
        index_references = []
        while n_sample > 0:
            for i in random.sample([i for i in range(n_orig)], k=n_sample):
                augmented_data.append(self._augment(data_entries[i]))
                index_references.append(i)
            n_sample = self._get_number_to_sample(n_orig, len(augmented_data), n_needed)
        return zip(augmented_data, index_references)

    @abstractmethod
    def _augment(self, data_entry: Tuple[str, str]) -> Tuple[str]:
        """
        Generates new content by performing the data augmentation step on the original content
        :param data_entry: the original content of the source, target artifact
        :return: the new content
        """
        pass

    @staticmethod
    def _get_number_to_sample(n_orig: int, n_new: int, n_needed: int) -> int:
        """
        Gets the number of data entries to select for word replacements
        :param n_orig: the number of orig data entries
        :param n_new: the current total of orig data entries
        :param n_needed: the number of new data entries needed
        :return: the number of data entries to select
        """
        return min(n_needed - n_new, n_orig)

    @classmethod
    def get_aug_id(cls) -> str:
        """
        Gets a unique augmentation id for the step
        :return: the augmentation id for the step
        """
        return str(hash(cls.__name__))[:8]
