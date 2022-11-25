from typing import List, Dict, Iterable, Tuple

from config.override import overrides
from tracer.datasets.processing.abstract_data_processor import AbstractDataProcessor
from tracer.datasets.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep


class DataAugmenter(AbstractDataProcessor):
    RUN_RESULTS = Dict[str, Iterable[Tuple[Tuple[str, str], int]]]

    @overrides(AbstractDataProcessor)
    def run(self, data_entries: List[Tuple[str, str]], n_total_expected: int) -> RUN_RESULTS:
        """
        Runs all given steps with the given run_arg
        :param data_entries: the arguments to use when running
        :param n_total_expected: total number of expected data entries at the end
        :return: the results from the steps
        """
        augmentation_results = {}
        for step in self.ordered_steps:
            content_list = [step.WORD_SEP.join([source, step.get_aug_id(), target]) for source, target in data_entries]
            n_expected_for_step = self._get_n_expected_for_step(step, n_total_expected)
            augmented_content, index_references = step.run(content_list, n_expected_for_step)
            augmented_data = [content.split(step.WORD_SEP + step.get_aug_id() + step.WORD_SEP) for content in augmented_content]
            augmentation_results[step.get_aug_id()] = zip(augmented_data, index_references)
        return augmentation_results

    @staticmethod
    def _get_n_expected_for_step(step: AbstractDataAugmentationStep, n_total_expected: int) -> int:
        """
        Gets the number of entries that the step should create based on its assigned weight
        :param step: the step
        :param n_total_expected: total number of expected data entries at the end
        :return: the n_expected for the given step
        """
        return round(step.percent_to_weight * n_total_expected)
