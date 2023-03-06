import os
from typing import Dict, Iterable, List

import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from constants import STAGES
from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.exporters.safa_exporter import ProjectData, SafaExporter
from data.keys.structure_keys import StructuredKeys
from data.tree.trace_link import TraceLink
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from util.dict_util import ListUtil
from util.logging.logger_manager import logger


class CreateSourceSplits(AbstractJob):
    """
    Split dataset by source and export splits as structured datasets.
    """

    def __init__(self, job_args: JobArgs, trace_dataset_creator: TraceDatasetCreator, export_path: str, splits: List[float]):
        """
        Initializes job for splitting dataset creator.
        :param job_args: Job args. Not used.
        :param trace_dataset_creator: The trace dataset creator used to read project.
        :param export_path: Path to export splits to.
        :param splits: List of floats determining the validation and eval percentages.
        """
        super().__init__(job_args)
        self.trace_dataset_creator = trace_dataset_creator
        self.export_path = export_path
        self.splits = splits

    def _run(self) -> JobResult:
        """
        Separates artifacts in type into different splits and saves projects accordingly.
        :return: JobResult containing empty message.
        """
        trace_dataset = self.trace_dataset_creator.create()
        trace_links = list(trace_dataset.links.values())
        project_data = ProjectData(artifact_df=self.trace_dataset_creator.artifact_df,
                                   layer_mapping_df=self.trace_dataset_creator.layer_mapping_df, traces=trace_dataset.links)
        artifact_df = project_data["artifact_df"]
        for layer_mapping_i, layer_mapping_row in project_data["layer_mapping_df"].iterrows():
            source_name, target_name = self.get_layer_types(layer_mapping_row)
            task_name = f"task_{layer_mapping_i}"

            artifacts_to_split = artifact_df[artifact_df[StructuredKeys.Artifact.LAYER_ID] == source_name]
            split_id_batches = self.get_artifact_ids_in_splits(artifacts_to_split, self.splits)
            all_split_ids = set(ListUtil.flatten(split_id_batches))

            for split_ids, stage in tqdm(zip(split_id_batches, STAGES), desc="Processing splits."):
                other_ids = all_split_ids - set(split_ids)
                logger.info("Creating split artifacts")
                split_artifact_df = CreateSourceSplits.create_task_split_artifact_df(artifact_df,
                                                                                     [source_name, target_name],
                                                                                     source_name,
                                                                                     other_ids)
                task_split_ids = set(list(split_artifact_df[StructuredKeys.Artifact.ID]))
                logger.info("Creating split trace links")
                split_links = CreateSourceSplits.create_split_links(trace_links, task_split_ids)
                split_project_data = ProjectData(artifact_df=split_artifact_df,
                                                 layer_mapping_df=pd.DataFrame([layer_mapping_row]),
                                                 traces=split_links)
                export_path = os.path.join(self.export_path, task_name, f"{stage}")
                self.export_project_data(split_project_data, export_path)
        self.export_project_data(project_data, os.path.join(self.export_path, "base"))
        return JobResult.from_dict({"status": "ok"})

    @staticmethod
    def create_split_links(trace_links: List[TraceLink], artifact_ids) -> Dict[int, TraceLink]:
        """
        Creates trace link dictionary only containing link referencing artifacts ids.
        :param trace_links: The trace links to filter.
        :param artifact_ids: Artifacts ids to filter by.
        :return: Mapping of trace link id to trace links.
        """
        cache = {}

        def check_exists(item):
            if item not in cache:
                cache[item] = item in artifact_ids
            return cache[item]

        relevant_traces = list(filter(lambda t: check_exists(t.source.id) and check_exists(t.target.id), trace_links))
        return {trace.id: trace for trace in relevant_traces}

    @staticmethod
    def create_task_split_artifact_df(artifact_df: pd.DataFrame, task_types: List[str], artifact_type: str, other_ids: Iterable[str]):
        """
        Selects types in task and artifacts not in other splits.
        :param artifact_df: Artifact dataframe containing all artifacts.
        :param task_types: The artifacts types in task.
        :param artifact_type: The artifact type to split by.
        :param other_ids: The ids present in other splits.
        :return: Artifact dataframe containing artifacts in task without artifacts in other splits.
        """
        #
        task_mask = artifact_df[StructuredKeys.Artifact.LAYER_ID].isin(task_types)
        other_ids_mask = artifact_df[StructuredKeys.Artifact.ID].isin(other_ids)
        other_ids_type_mask = artifact_df[StructuredKeys.Artifact.LAYER_ID] == artifact_type
        split_artifact_df = artifact_df[task_mask & ~(other_ids_mask & other_ids_type_mask)]
        return split_artifact_df

    @staticmethod
    def get_artifact_ids_in_splits(artifacts: List[Dict], split_percentages: List[float]) -> List[List[str]]:
        """
        Selects artifact ids for each split.
        :param artifacts: The artifacts whose ids are split.
        :param split_percentages: The percentage of the artifacts to allocate to each subsequent split (val and eval).
        :return: List containing list of artifacts per split.
        """
        target_ids = list(artifacts[StructuredKeys.Artifact.ID])
        val_total = split_percentages[0] + split_percentages[1]
        train_ids, val_ids = train_test_split(target_ids, test_size=val_total)
        val_ids, test_ids = train_test_split(val_ids, test_size=split_percentages[1] / val_total)
        split_id_batches = [train_ids, val_ids, test_ids]
        return split_id_batches

    @staticmethod
    def export_project_data(split_project_data: ProjectData, export_path: str) -> None:
        """
        Saves split project data to export path.
        :param split_project_data: Project data for split.
        :param export_path: Path to save directory.
        :return: None
        """
        os.makedirs(export_path, exist_ok=True)
        SafaExporter.export(export_path, split_project_data)

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
