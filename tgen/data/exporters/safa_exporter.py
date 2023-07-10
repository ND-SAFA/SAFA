import os
from typing import Dict, List

import pandas as pd

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from tgen.data.keys.safa_keys import SafaKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.enum_util import EnumDict
from tgen.util.file_util import FileUtil
from tgen.util.override import overrides


class SafaExporter(AbstractDatasetExporter):
    """
    Exports trace dataset as a SAFA one.
    """

    def __init__(self, export_path: str, dataset_creator: TraceDatasetCreator = None, dataset: TraceDataset = None):
        """
        Initializes exporter for given trace dataset.
        :param export_path: Path to export project to.
        :param dataset_creator: The creator in charge of making the dataset to export
        """
        super().__init__(export_path, dataset_creator, dataset)
        self.artifact_definitions = []
        self.trace_definitions = []
        self.artifact_type_to_artifacts = None

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
        self.artifact_type_to_artifacts = self.create_artifact_definitions()
        self.create_trace_definitions()
        self.create_tim()

    def create_artifact_definitions(self) -> Dict[str, ArtifactDataFrame]:
        """
        Creates dataframe for each artifact grouped by type.
        :return: None
        """
        artifact_types = set()
        for _, row in self.get_dataset().layer_df.itertuples():
            source_type = row[StructuredKeys.LayerMapping.SOURCE_TYPE]
            target_type = row[StructuredKeys.LayerMapping.TARGET_TYPE]
            artifact_types.update({source_type, target_type})

        artifact_type_to_artifacts = {}
        for artifact_type in artifact_types:
            entries: List[Dict] = []
            artifact_type_to_artifacts[artifact_type] = self.get_artifacts_of_type(artifact_type)
            for id_, artifact in artifact_type_to_artifacts[artifact_type].iterrows():
                entries.append(EnumDict({
                    StructuredKeys.Artifact.ID: id_,
                    StructuredKeys.Artifact.CONTENT: artifact[ArtifactKeys.CONTENT.value],
                }))
            file_name = artifact_type + ".csv"
            local_export_path = os.path.join(self.export_path, file_name)
            pd.DataFrame(entries).to_csv(local_export_path, index=False)
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

                if TraceKeys.SCORE.value in trace_row:
                    trace_entry["traceType"] = "GENERATED"
                    trace_entry["approvalStatus"] = "UNREVIEWED"
                    trace_entry["score"] = trace_row[TraceKeys.SCORE.value]

                else:
                    trace_entry["traceType"] = "MANUAL"
                    trace_entry["score"] = 1
                traces_json.append(trace_entry)
            FileUtil.write({"traces": traces_json}, export_file_path)

    def create_trace_df_for_layer(self, source_type, target_type) -> pd.DataFrame:
        """
        Creates data frame containing positive traces between source and target types.
        :param source_type: The name of the source type.
        :param target_type: The name of the target type.
        :return: DataFrame with positive links.
        """
        source_artifacts = self.artifact_type_to_artifacts[source_type]
        target_artifacts = self.artifact_type_to_artifacts[target_type]
        entries = []
        for source_id in source_artifacts.index:
            for target_id in target_artifacts.index:
                if source_id == target_id:
                    continue
                trace_link_id = TraceDataFrame.generate_link_id(source_id, target_id)
                trace_link: EnumDict = self.get_dataset().trace_df.get_link(trace_link_id)
                assert trace_link is not None, f"Expected trace (source: {source_id}, target: {target_id}) to exist but it does not"
                if trace_link[TraceKeys.LABEL] == 1:
                    entries.append(EnumDict({
                        StructuredKeys.Trace.TARGET: target_id,
                        StructuredKeys.Trace.SOURCE: source_id
                    }))
        return pd.DataFrame(entries)

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
        return DataFrameUtil.query_df(self.get_dataset().artifact_df, {ArtifactKeys.LAYER_ID: artifact_type})
