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
    def run(self, data_entries: List, n_expected: int = None) -> AbstractDataAugmentationStep.AUGMENTATION_RESULT:
        """
        Runs the resample step to obtain a larger dataset
        :param data_entries: a list of tokens as source, target pairs
        :param n_expected: the number of data entries desired
        :return: list of containing the augmented data and the orig indices for the entry
        """
        if n_expected:
            self.resample_rate = max(round(n_expected / len(data_entries)), 1)
        augmented_data = []
        index_references = []
        for i, data_entry in data_entries:
            resampled_data = self._augment(data_entry)
            augmented_data.extend(resampled_data)
            index_references.extend([i for j in range(len(resampled_data))])
        return zip(augmented_data, index_references)

    def _augment(self, data_entry: Tuple[str, str]) -> List[Tuple[str, str]]:
        """
        Resamples the data entry by the resample_rate
        :param data_entry: the data entry to resample
        :return: a list of the entry the number of times the resample_rate
        """
        return [data_entry for i in range(self.resample_rate)]

    @classmethod
    @overrides(AbstractDataAugmentationStep)
    def get_aug_id(cls) -> str:
        return ""
