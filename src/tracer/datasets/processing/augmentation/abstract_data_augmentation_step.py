import random
from abc import ABC, abstractmethod
from typing import List, Iterable, Tuple

from config.override import overrides
from tracer.datasets.processing.abstract_data_processing_step import AbstractDataProcessingStep, ProcessingOrder


class AbstractDataAugmentationStep(AbstractDataProcessingStep, ABC):

    def __init__(self, percent_to_weight: float, order: ProcessingOrder = ProcessingOrder.ANY):
        """
        :param percent_to_weight: the percentage of the data that the augmentation step will augment
        :param order: the order the step should be run in
        """
        self.percent_to_weight = percent_to_weight
        super().__init__(order)

    @overrides(AbstractDataProcessingStep)
    def run(self, contents_list: List[str], n_expected: int) -> Tuple[str, int]:
        """
        Runs the data augmentation to obtain a larger dataset
        :param contents_list: a list of data content
        :param n_expected: the number of data entries desired
        :return: list of tuples containing the augmented data and the orig indices for the entry
        """

        n_orig = len(contents_list)
        n_sample = self._get_number_to_sample(n_orig, 0, n_expected)
        augmented_content = []
        index_references = []
        while n_sample > 0:
            for i in random.sample([i for i in range(n_orig)], k=n_sample):
                orig_content = contents_list[i]
                augmented_content.append(self._generate_new_content(orig_content))
                index_references.append(i)
            n_sample = self._get_number_to_sample(n_orig, len(augmented_content), n_expected)
        return augmented_content, index_references

    @abstractmethod
    def _generate_new_content(self, orig_content: str) -> str:
        """
        Generates new content by performing the data augmentation step on the original content
        :param orig_content: the original content
        :return: the new content
        """
        pass

    @staticmethod
    def _get_number_to_sample(n_orig: int, n_new: int, n_expected: int) -> int:
        """
        Gets the number of data entries to select for word replacements
        :param n_orig: the number of orig data entries
        :param n_new: the current total of orig data entries
        :param n_expected: the number of desired data entries
        :return: the number of data entries to select
        """
        return min(n_expected - (n_new + n_orig), n_orig)

    @classmethod
    def get_aug_id(cls) -> str:
        """
        Gets a unique augmentation id for the step
        :return: the augmentation id for the step
        """
        return str(hash(cls.__name__))[:8]

