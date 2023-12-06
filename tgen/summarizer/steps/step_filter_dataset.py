from typing import List, Union

from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_state import SummarizerState


class StepFilterDataset(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Filters the dataset to only include certain artifacts.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        if not args.include_subset_by_type and not args.include_subset_by_dir:
            return
        artifact_df = state.dataset.artifact_df
        indices2keep = [a_id for a_id in artifact_df.index if self.in_dirs(a_id, args.include_subset_by_dir)
                        or self.is_file_type(a_id, args.include_subset_by_type)]
        state.dataset.update_artifact_df(artifact_df.filter_by_index(index_to_filter=indices2keep))

    @staticmethod
    def check_condition(a_id: str, conditions2check: Union[List[str], str], method2use: str) -> bool:
        """
        Checks whether an artifact id meets a certain condition.
        :param a_id: The artifact id.
        :param conditions2check: The list of conditions to check for.
        :param method2use: The string method to use to check the condition (e.g. startswith).
        :return: True if it meets one or more of the conditions else False.
        """
        conditions2check = [conditions2check] if not isinstance(conditions2check, list) else conditions2check
        for condition in conditions2check:
            if getattr(a_id, method2use)(condition):
                return True
        return False

    @staticmethod
    def in_dirs(a_id: str, directories:  Union[List[str], str]) -> bool:
        """
        Checks whether a file is inside of the dir based on its name.
        :param a_id: The artifact id.
        :param directories: The list of directories to check for.
        :return: True if it is in the directory else False.
        """
        return StepFilterDataset.check_condition(a_id, directories, "startswith")

    @staticmethod
    def is_file_type(a_id: str, file_types:  Union[List[str], str]) -> bool:
        """
        Checks whether a file is one of the given types.
        :param a_id: The artifact id.
        :param file_types: The list of file types to check for.
        :return: True if file is one of the given types else False.
        """
        return StepFilterDataset.check_condition(a_id, file_types, "endswith")
