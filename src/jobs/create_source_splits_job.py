import os
from typing import List, Union

from sklearn.model_selection import train_test_split

from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.dataframes.artifact_dataframe import ArtifactDataFrame
from data.dataframes.layer_dataframe import LayerDataFrame
from data.dataframes.trace_dataframe import TraceKeys, TraceDataFrame
from data.datasets.trace_dataset import TraceDataset
from data.exporters.safa_exporter import SafaExporter
from data.keys.structure_keys import StructuredKeys
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from util.dataframe_util import DataFrameUtil

STAGES = ["train", "val", "eval"]


class CreateSourceSplitsJob(AbstractJob):
    """
    Split dataset by source and export splits as structured datasets.
    """

    def __init__(self, job_args: JobArgs, trace_dataset_creator: TraceDatasetCreator, export_path: str, splits: List[float],
                 artifact_type: str):
        """
        Initializes job for splitting dataset creator.
        :param job_args: Job args. Not used.
        :param trace_dataset_creator: The trace dataset creator used to read project.
        :param export_path: Path to export splits to.
        :param splits: List of floats determining the validation and eval percentages.
        :param artifact_type: String representing artifact type to split by.
        """
        super().__init__(job_args)
        self.trace_dataset_creator = trace_dataset_creator
        self.export_path = export_path
        self.splits = splits
        self.artifact_type = artifact_type

    def _run(self) -> JobResult:
        """
        Separates artifacts in type into different splits and saves projects accordingly.
        :return: JobResult containing empty message.
        """
        trace_dataset = self.trace_dataset_creator.create()
        types_defined = list(trace_dataset.artifact_df[StructuredKeys.Artifact.LAYER_ID.value].unique())
        assert self.artifact_type in types_defined, f"{self.artifact_type} is not in: {types_defined}"

        target_artifacts = trace_dataset.artifact_df[
            trace_dataset.artifact_df[StructuredKeys.Artifact.LAYER_ID.value] == self.artifact_type]
        target_ids = list(target_artifacts.index)

        val_total = self.splits[0] + self.splits[1]
        train_ids, val_ids = train_test_split(target_ids, test_size=val_total)
        val_ids, test_ids = train_test_split(val_ids, test_size=self.splits[1] / val_total)
        split_id_batches = [train_ids, val_ids, test_ids]
        type_artifact_ids = target_ids + val_ids + test_ids

        self.create_splits(split_id_batches, trace_dataset, type_artifact_ids)

        return JobResult.from_dict({"status": "ok"})

    def create_splits(self, split_artifact_id_batches: List[List], trace_dataset: TraceDataset,
                      type_artifact_ids: List[Union[str, int]]) -> None:
        """
        Creates each split by filtering only selected artifacts.
        :param split_artifact_id_batches: Batches containing artifact ids to target in each split.
        :param trace_dataset: The trace dataset containing all the trace links.
        :param type_artifact_ids: The artifact ids of all splits.
        :return: None
        """
        for split_ids, stage in zip(split_artifact_id_batches, STAGES):
            all_ids = set(type_artifact_ids)
            other_ids = all_ids - set(split_ids)

            split_artifact_ids_mask = trace_dataset.artifact_df.index.isin(other_ids)
            layer_mask = trace_dataset.artifact_df[StructuredKeys.Artifact.LAYER_ID.value] == self.artifact_type
            split_artifact_df = trace_dataset.artifact_df[~(split_artifact_ids_mask & layer_mask)]
            split_trace_df = DataFrameUtil.filter_df_by_row(trace_dataset.trace_df,
                                                            lambda t: t[TraceKeys.SOURCE.value] not in other_ids
                                                                      and t[TraceKeys.TARGET.value] not in other_ids)
            export_path = os.path.join(self.export_path, f"{stage}")
            dataset = TraceDataset(ArtifactDataFrame(split_artifact_df), TraceDataFrame(split_trace_df),
                                   LayerDataFrame(trace_dataset.layer_mapping_df))
            exporter = SafaExporter(export_path, dataset=dataset)
            exporter.export()
