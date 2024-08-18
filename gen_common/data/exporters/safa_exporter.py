import os
from typing import Dict, List

import pandas as pd

from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from gen_common.data.keys.safa_keys import SafaKeys
from gen_common.data.keys.structure_keys import ArtifactKeys, StructuredKeys, TraceKeys
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.dataframe_util import DataFrameUtil
from gen_common.util.file_util import FileUtil
from gen_common.util.override import overrides


class SafaExporter(AbstractDatasetExporter):
    """
    Exports trace dataset as a SAFA one.
    """

    def __init__(self, export_path: str, dataset_creator: TraceDatasetCreator = None, dataset: TraceDataset = None,
                 artifact_types: List[str] = None):
        """
        Initializes exporter for given trace dataset.
        :param export_path: Path to export project to.
        :param dataset_creator: The creator in charge of making the dataset to export
        :param dataset: Built dataset to replace using creator.
        :param artifact_types: The artifacts types to export.
        """
        super().__init__(export_path, dataset_creator, dataset)
        self.artifact_definitions = []
        self.trace_definitions = []
        self.artifact_type_to_artifacts = None
        self.artifact_types = artifact_types

    @staticmethod
    def include_filename() -> bool:
        """
        Returns True if the dataset exporter expects the export path to include the filename, else False
        :return: True if the dataset exporter expects the export path to include the filename, else False
        """
        return False

    @overrides(AbstractDatasetExporter)
    def export(self, **kwargs) -> None:
        """
        Exports entities as a project in the safa format.
        :return: None
        """
        artifact_df = self.get_dataset().artifact_df
        if not self.artifact_types:
            self.artifact_types = set(artifact_df[ArtifactKeys.LAYER_ID.value].unique())
        self.artifact_type_to_artifacts = self.create_artifact_definitions()
        self.create_trace_definitions()
        self.create_tim()
        logger.info(f"Exported SAFA dataset to {self.export_path}")

    def create_artifact_definitions(self) -> Dict[str, ArtifactDataFrame]:
        """
        Creates dataframe for each artifact grouped by type.
        :return: None
        """
        artifact_df = self.get_dataset().artifact_df

        artifact_type_to_artifacts = {}
        for artifact_type in self.artifact_types:
            artifact_type_df = artifact_df.get_artifacts_by_type(artifact_type)
            artifact_type_to_artifacts[artifact_type] = artifact_type_df
            # Export artifacts of type
            file_name = f"{artifact_type}.csv"
            artifact_type_export_path = os.path.join(self.export_path, file_name)
            artifact_type_df.to_csv(artifact_type_export_path)
            self.artifact_definitions.append({
                SafaKeys.TYPE: artifact_type,
                SafaKeys.FILE: file_name
            })
        return artifact_type_to_artifacts

    def create_trace_definitions(self) -> None:
        """
        Create trace definition between each layer in trace creator.
        :return: None
        """

        for _, row in self.get_dataset().layer_df.itertuples():
            source_type = row[StructuredKeys.LayerMapping.SOURCE_TYPE]
            target_type = row[StructuredKeys.LayerMapping.TARGET_TYPE]
            if source_type not in self.artifact_types or target_type not in self.artifact_types:
                continue
            matrix_name = f"{source_type}2{target_type}"
            file_name = matrix_name + ".json"
            export_file_path = os.path.join(self.export_path, file_name)
            trace_df = self.create_trace_df_for_layer(source_type, target_type)
            self.trace_definitions.append({
                SafaKeys.FILE: file_name,
                SafaKeys.SOURCE_ID: source_type,
                SafaKeys.TARGET_ID: target_type
            })
            traces_json = []
            for trace_index, trace_row in trace_df.iterrows():
                trace_entry = {
                    "sourceName": trace_row[TraceKeys.SOURCE.value],
                    "targetName": trace_row[TraceKeys.TARGET.value]
                }
                score = DataFrameUtil.get_optional_value_from_df(trace_row, TraceKeys.SCORE.value)
                label = DataFrameUtil.get_optional_value_from_df(trace_row, TraceKeys.LABEL.value)
                if score:
                    trace_entry["traceType"] = "GENERATED"
                    trace_entry["approvalStatus"] = "UNREVIEWED"
                    trace_entry["score"] = score
                    trace_entry["explanation"] = trace_row.get(TraceKeys.EXPLANATION.value, None)
                elif label and label == 1:
                    trace_entry["traceType"] = "MANUAL"
                    trace_entry["score"] = 1
                else:  # negative link
                    continue
                traces_json.append(trace_entry)
            FileUtil.write({"traces": traces_json}, export_file_path)

    def create_trace_df_for_layer(self, source_type, target_type) -> pd.DataFrame:
        """
        Creates data frame containing positive traces between source and target types.
        :param source_type: The name of the source type.
        :param target_type: The name of the target type.
        :return: DataFrame with positive links.
        """
        trace_df = self.get_dataset().trace_df

        source_artifacts = self.artifact_type_to_artifacts[source_type]
        target_artifacts = self.artifact_type_to_artifacts[target_type]
        trace_ids = [TraceDataFrame.generate_link_id(source_id, target_id)
                     for source_id in source_artifacts.index for target_id in target_artifacts.index]
        trace_df_layer = trace_df.filter_by_index(trace_ids)
        return trace_df_layer

    def create_tim(self) -> None:
        """
        Writes TIM file to export path.
        :return: None
        """
        tim_definition = {
            SafaKeys.ARTIFACTS: self.artifact_definitions,
            SafaKeys.TRACES: self.trace_definitions
        }
        tim_export_path = os.path.join(self.export_path, "tim.json")
        FileUtil.write(tim_definition, tim_export_path)

    def get_artifacts_of_type(self, artifact_type: str) -> ArtifactDataFrame:
        """
        Gets a dataframe of artifacts of a given type
        :param artifact_type: The artifact type
        :return: A dataframe of artifacts of a given type
        """
        return DataFrameUtil.query_df(self.get_dataset().artifact_df, {ArtifactKeys.LAYER_ID.value: artifact_type})
