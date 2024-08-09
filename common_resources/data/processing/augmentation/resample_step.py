from typing import List, Tuple

from common_resources.tools.util.override import overrides
from common_resources.tools.constants.dataset_constants import RESAMPLE_RATE_DEFAULT
from common_resources.data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep


class ResampleStep(AbstractDataAugmentationStep):

    def __init__(self, percent_to_weight: float = 1, resample_rate: int = RESAMPLE_RATE_DEFAULT):
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

    def _augment(self, data_entry: Tuple[str, str]) -> List[Tuple[str, str]]:
        """
        Resamples the data entry by the resample_rate
        :param data_entry: the data entry to resample
        :return: a list of the entry the number of times the resample_rate
        """
        return [data_entry for i in range(self.resample_rate)]

    @staticmethod
    @overrides(AbstractDataAugmentationStep)
    def _add_augmented_data(augmented_data: List, index_reference: int, augmented_data_entries: List,
                            index_references: List) -> None:
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
