import math
import random
from typing import Union, Tuple, List

from config.constants import RESAMPLE_RATE_DEFAULT
from config.override import overrides
from tracer.datasets.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep


class ResampleStep(AbstractDataAugmentationStep):

    def __init__(self, percent_to_weight: float, resample_rate: int = RESAMPLE_RATE_DEFAULT):
        """
        Handles word replacement to augment the data and obtain a larger dataset
        :param percent_to_weight: the percentage of the data that the augmentation step will augment
        :param resample_rate: the rate at which to resample the data
        """
        self.resample_rate = resample_rate
        super().__init__(percent_to_weight)

    @overrides(AbstractDataAugmentationStep)
    def run(self, data_entries: List, n_needed: int = None) -> AbstractDataAugmentationStep.AUGMENTATION_RESULT:
        """
        Runs the resample step to obtain a larger dataset
        :param data_entries: a list of tokens as source, target pairs
        :param n_needed: the number of new data entries needed
        :return: list of containing the augmented data and the orig indices for the entry
        """
        if n_needed is None:
            n_needed = self.resample_rate * len(data_entries)
        else:
            self.resample_rate = 1
        return super().run(data_entries, n_needed)
        #     n_per_entry = n_needed / len(data_entries)
        #     if 0 < n_per_entry < 1:
        #         n_sample = round(n_per_entry * len(data_entries))
        #         data_entries = random.sample(data_entries, k=n_sample)
        #     self.resample_rate = math.ceil(n_per_entry)
        #
        # augmented_data = []
        # index_references = []
        # for i, data_entry in enumerate(data_entries):
        #     resampled_data = self._augment(data_entry)
        #     augmented_data.extend(resampled_data)
        #     index_references.extend([i for j in range(len(resampled_data))])
        #
        # if len(augmented_data) > n_needed:
        #     sample_indices = random.sample([i for i in range(len(augmented_data))], n_needed)
        #     return zip([augmented_data[i] for i in sample_indices],  [index_references[i] for i in sample_indices])
        # return zip(augmented_data, index_references)

    def _augment(self, data_entry: Tuple[str, str]) -> List[Tuple[str, str]]:
        """
        Resamples the data entry by the resample_rate
        :param data_entry: the data entry to resample
        :return: a list of the entry the number of times the resample_rate
        """
        return [data_entry for i in range(self.resample_rate)]

    @staticmethod
    @overrides(AbstractDataAugmentationStep)
    def _add_augmented_data(augmented_data: List, index_reference: int, augmented_data_entries: List, index_references: List) -> None:
        """
        Adds the augmented data to the appropriate lists
        :param augmented_data: the augmented data
        :param index_reference: the reference index to original data entry
        :param augmented_data_entries: a list of the current augmented data entries
        :param index_references: a list of the current reference indices to original data entries
        :return: None
        """
        augmented_data_entries.extend(augmented_data)
        index_references.extend([index_reference for i in range(len(augmented_data))])

    @classmethod
    @overrides(AbstractDataAugmentationStep)
    def _unique_step_id(cls) -> str:
        """
        Uses a empty string as id so that resulting links will have same ids as original
        :return: the id
        """
        return ""
