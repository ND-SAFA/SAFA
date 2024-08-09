from typing import Dict, List, Tuple, Type

from common_resources.tools.util.override import overrides
from common_resources.data.processing.abstract_data_processor import AbstractDataProcessor
from common_resources.data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep


class DataAugmenter(AbstractDataProcessor):
    ordered_steps: List[AbstractDataAugmentationStep]

    @overrides(AbstractDataProcessor)
    def run(self, data_entries: List[Tuple[str, str]], n_total_expected: int,
            exclude_all_but_step_type: Type[AbstractDataAugmentationStep] = None,
            include_all_but_step_type: Type[AbstractDataAugmentationStep] = None) \
            -> Dict[str, AbstractDataAugmentationStep.AUGMENTATION_RESULT]:
        """
        Runs all given steps with the given run_arg
        :param data_entries: the arguments to use when running
        :param n_total_expected: total number of expected data entries at the end
        :param exclude_all_but_step_type: if provided, will ONLY run step of given type
        :param include_all_but_step_type: if provided, will run all steps BUT the given type
        :return: the augmentation step id mapped to its results
        """
        n_needed = n_total_expected - len(data_entries)
        steps2run = self._get_steps_to_run(exclude_all_but_step_type, include_all_but_step_type)
        augmentation_results = {}
        for step in steps2run:
            n_expected_for_step = self._get_n_expected_for_step(step, n_needed)
            augmentation_result = step.run(data_entries, n_expected_for_step)
            augmentation_results[step.get_id()] = augmentation_result
        return augmentation_results

    def _get_steps_to_run(self, exclude_all_but_step_type: Type[AbstractDataAugmentationStep] = None,
                          include_all_but_step_type: Type[AbstractDataAugmentationStep] = None) -> List[AbstractDataAugmentationStep]:
        """
        Gets the steps that should be run
        :param exclude_all_but_step_type: if provided, will ONLY run step of given type
        :param include_all_but_step_type: if provided, will run all steps BUT the given type
        :return: the steps to run
        """
        if include_all_but_step_type:
            steps2run = self._filter_step_type(self.ordered_steps, include_all_but_step_type)
        elif exclude_all_but_step_type:
            step = self._get_step_of_type(self.ordered_steps, exclude_all_but_step_type)
            steps2run = [step] if step else []
        else:
            steps2run = self.ordered_steps
        return steps2run

    @staticmethod
    def _filter_step_type(steps: List[AbstractDataAugmentationStep], step_type: Type[AbstractDataAugmentationStep]) \
            -> List[AbstractDataAugmentationStep]:
        """
        Filters out the given step type from the list of steps
        :param steps: a list of all steps
        :param step_type: the step type to filter
        :return: the filtered list of steps
        """
        return [step for step in steps if not isinstance(step, step_type)]

    @staticmethod
    def _get_step_of_type(steps: List[AbstractDataAugmentationStep], step_type: Type[AbstractDataAugmentationStep]) \
            -> AbstractDataAugmentationStep:
        """
        Gets a step matching the given type
        :param steps: a list of all steps
        :param step_type: the step type to get
        :return: the step matching the given type
        """
        for step in steps:
            if isinstance(step, step_type):
                return step

    @staticmethod
    def _get_n_expected_for_step(step: AbstractDataAugmentationStep, n_total_expected: int) -> int:
        """
        Gets the number of entries that the step should create based on its assigned weight
        :param step: the step
        :param n_total_expected: total number of expected data entries at the end
        :return: the n_expected for the given step
        """
        return round(step.percent_to_weight * n_total_expected)
