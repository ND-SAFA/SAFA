from collections import Counter
from typing import List, Set, Union

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.summarize.summarizer_args import SummarizerArgs
from gen_common.summarize.summarizer_state import SummarizerState
from gen_common.util.dataframe_util import DataFrameUtil


class StepFilterDataset(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Filters the dataset to only include certain artifacts.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        artifact_df = state.dataset.artifact_df
        should_filter = args.include_subset_by_type or args.include_subset_by_dir
        indices2remove = StepFilterDataset.identify_indices_with_duplicate_content(artifact_df)
        missing_content = {i for i, a in artifact_df.itertuples() if not DataFrameUtil.get_optional_value(a[ArtifactKeys.CONTENT],
                                                                                                          allow_empty=True)}
        indices2remove.update(missing_content)
        if should_filter:
            indices2remove.update({a_id for a_id in artifact_df.index if not (self.in_dirs(a_id, args.include_subset_by_dir)
                                                                              or self.is_file_type(a_id,
                                                                                                   args.include_subset_by_type))})
        indices2keep = set(artifact_df.index).difference(indices2remove)
        filtered_artifacts = artifact_df.filter_by_index(index_to_filter=indices2keep)
        assert len(filtered_artifacts) > 0, "No artifacts remain after filtering. Please check the filter conditions."
        filtered_artifacts.drop_large_files()
        state.dataset.update_artifact_df(filtered_artifacts)

    @staticmethod
    def identify_indices_with_duplicate_content(artifact_df: ArtifactDataFrame) -> Set:
        """
        Identifies indices in the dataframe that have duplicated content so they can be removed.
        :param artifact_df: The artifact df to identify duplicates in.
        :return: The set of indices in the dataframe that have duplicated content so they can be removed.
        """
        duplicate_content = {content for content, n in Counter([a[ArtifactKeys.CONTENT]
                                                                for a in artifact_df.to_artifacts()]).items() if n > 1}
        indices2remove = set()
        for artifact in artifact_df.to_artifacts():
            if artifact[ArtifactKeys.CONTENT] in duplicate_content:
                indices2remove.add(artifact[ArtifactKeys.ID])
                duplicate_content.remove(artifact[ArtifactKeys.CONTENT])
        return indices2remove

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
    def in_dirs(a_id: str, directories: Union[List[str], str]) -> bool:
        """
        Checks whether a file is inside of the dir based on its name.
        :param a_id: The artifact id.
        :param directories: The list of directories to check for.
        :return: True if it is in the directory else False.
        """
        return StepFilterDataset.check_condition(a_id, directories, "startswith")

    @staticmethod
    def is_file_type(a_id: str, file_types: Union[List[str], str]) -> bool:
        """
        Checks whether a file is one of the given types.
        :param a_id: The artifact id.
        :param file_types: The list of file types to check for.
        :return: True if file is one of the given types else False.
        """
        return StepFilterDataset.check_condition(a_id, file_types, "endswith")
