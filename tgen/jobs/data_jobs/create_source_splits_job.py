import os
from typing import Iterable, List, Set, Union

import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from common_resources.tools.util.dataframe_util import DataFrameUtil
from common_resources.tools.util.list_util import ListUtil
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from common_resources.data.keys.structure_keys import ArtifactKeys, StructuredKeys, TraceKeys
from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs


class CreateSourceSplitsJob(AbstractJob):
    """
    Split dataset by source and export splits as structured datasets.
    """

    def __init__(self, exporter: AbstractDatasetExporter, splits: List[float], job_args: JobArgs = None):
        """
        Initializes job for splitting dataset creator.
        :param job_args: Job args. Not used.
        :param exporter: The exporter to use to save the dataset
        :param splits: List of floats determining the validation and eval percentages.
        :param job_args: The args for the job
        """
        super().__init__(job_args)
        self.exporter = exporter
        self.splits = splits

    def _run(self) -> str:
        """
        Separates artifacts in type into different splits and saves projects accordingly.
        :return: JobResult containing empty message.
        """
        dataset = self.exporter.get_dataset()
        for layer_mapping_i, layer_mapping_row in dataset.layer_df.itertuples():
            source_name, target_name = self.get_layer_types(layer_mapping_row)
            task_name = f"task_{layer_mapping_i}"

            artifacts_to_split = DataFrameUtil.query_df(dataset.artifact_df, {StructuredKeys.Artifact.LAYER_ID.value: source_name})
            split_id_batches = self.get_artifact_ids_in_splits(artifacts_to_split, self.splits)
            all_split_ids = set(ListUtil.flatten(split_id_batches))

            stages = [e for e in DatasetRole if e != DatasetRole.PRE_TRAIN]
            for split_ids, stage in tqdm(zip(split_id_batches, stages), desc="Processing splits."):
                other_ids = all_split_ids - set(split_ids)
                logger.info("Creating split artifacts")
                split_artifact_df = CreateSourceSplitsJob.create_task_split_artifact_df(dataset.artifact_df,
                                                                                        [source_name, target_name],
                                                                                        source_name,
                                                                                        other_ids)
                task_split_ids = set(split_artifact_df.index)
                logger.info("Creating split trace links")
                split_links = CreateSourceSplitsJob.create_split_links(dataset.trace_df, task_split_ids)
                split_project_data = TraceDataset(artifact_df=split_artifact_df,
                                                  layer_df=LayerDataFrame([layer_mapping_row]),
                                                  trace_df=split_links)
                export_path = os.path.join(self.exporter.export_path, task_name, f"{stage.value}")
                split_exporter = self.exporter.make_new(export_path=export_path, dataset=split_project_data)
                split_exporter.export()
        export_path = os.path.join(self.exporter.export_path, "base")
        self.exporter.update_export_path(export_path)
        self.exporter.export()
        return export_path

    @staticmethod
    def create_split_links(trace_links: TraceDataFrame, artifact_ids: Set[Union[str, int]]) -> TraceDataFrame:
        """
        Creates trace link dictionary only containing link referencing artifacts ids.
        :param trace_links: The trace links to filter.
        :param artifact_ids: Artifacts ids to filter by.
        :return: Mapping of trace link id to trace links.
        """

        def check_exists(item):
            """
            Closure checking if item is in artifact ids.
            :param item: The item to check.
            :return: True if item is contained.
            """
            return item in artifact_ids

        relevant_traces = DataFrameUtil.filter_df_by_row(trace_links,
                                                         lambda t: check_exists(t[TraceKeys.SOURCE.value]) and check_exists(
                                                             t[TraceKeys.TARGET.value]))
        return TraceDataFrame(relevant_traces)

    @staticmethod
    def create_task_split_artifact_df(artifact_df: ArtifactDataFrame, task_types: List[str],
                                      artifact_type: str, other_ids: Iterable[str]) -> ArtifactDataFrame:
        """
        Selects types in task and artifacts not in other splits.
        :param artifact_df: Artifact dataframe containing all artifacts.
        :param task_types: The artifacts types in task.
        :param artifact_type: The artifact type to split by.
        :param other_ids: The ids present in other splits.
        :return: Artifact dataframe containing artifacts in task without artifacts in other splits.
        """
        #
        task_mask = artifact_df[ArtifactKeys.LAYER_ID].isin(task_types)
        other_ids_mask = artifact_df.index.isin(other_ids)
        other_ids_type_mask = artifact_df[ArtifactKeys.LAYER_ID] == artifact_type
        split_artifact_df = artifact_df[task_mask & ~(other_ids_mask & other_ids_type_mask)]
        return ArtifactDataFrame(split_artifact_df)

    @staticmethod
    def get_artifact_ids_in_splits(artifacts: ArtifactDataFrame, split_percentages: List[float]) -> List[List[str]]:
        """
        Selects artifact ids for each split.
        :param artifacts: The artifacts whose ids are split.
        :param split_percentages: The percentage of the artifacts to allocate to each subsequent split (val and eval).
        :return: List containing list of artifacts per split.
        """
        target_ids = list(artifacts.index)
        val_total = split_percentages[0] + split_percentages[1]
        train_ids, val_ids = train_test_split(target_ids, test_size=val_total)
        val_ids, test_ids = train_test_split(val_ids, test_size=split_percentages[1] / val_total)
        split_id_batches = [train_ids, val_ids, test_ids]
        return split_id_batches

    @staticmethod
    def filter_by_type(artifact_df, types: List[str]):
        """
        Creates artifact dataframe containing types given.
        :param artifact_df: The artifact dataframe containing artifacts for all types.
        :param types: The artifacts types to include in final dataframe.
        :return:
        """
        type_mask = artifact_df[StructuredKeys.Artifact.LAYER_ID].isin(types)
        return artifact_df[type_mask]

    @staticmethod
    def get_layer_types(layer_mapping_row: pd.Series):
        """
        Returns the source and target layers defined in layer mapping.
        :param layer_mapping_row: Row in layer mapping dataframe containing source and target types.
        :return: Source and target types.
        """
        source_name = layer_mapping_row[StructuredKeys.LayerMapping.SOURCE_TYPE]
        target_name = layer_mapping_row[StructuredKeys.LayerMapping.TARGET_TYPE]
        return source_name, target_name
