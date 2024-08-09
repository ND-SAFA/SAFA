from typing import Tuple

from common_resources.data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep


class SourceTargetSwapStep(AbstractDataAugmentationStep):

    def __init__(self, **kwargs):
        """
        Handles swapping the source and target pairs to augment the data
        """
        super().__init__(**kwargs)

    def _augment(self, data_entry: Tuple[str, str]) -> Tuple[str]:
        """
        Swaps source and target
        :param data_entry: the original joined content of source and target
        :return: the swapped content
        """
        source_content, target_content = data_entry
        return tuple([target_content, source_content])
