import os
from typing import Dict, List, TypedDict

import pandas as pd

from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.keys.safa_format import SafaKeys
from data.keys.structure_keys import StructuredKeys
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from util.file_util import FileUtil


class ProjectData(TypedDict):
    """
    The project data necessary to export it.
    """
    artifact_df: pd.DataFrame
    layer_mapping_df: pd.DataFrame
    traces: Dict[int, TraceLink]


class SafaExporter:
    """
    Exports trace dataset as a SAFA one.
    """

    def __init__(self):
        """
        Initializes empty exporter.
        """
        self.artifact_definitions = {}
        self.trace_definitions = {}
        self.artifact_type_2_id = None
        self.id_2_artifact = None

    @staticmethod
    def export(export_path, project_data: ProjectData):
        """
        Exports entities as a project in the safa format.
        :param export_path: Path to export project to.
        :param project_data: Data containing trace queries, artifacts, and traces between them.
        :return: None
        """
        exporter = SafaExporter()
        exporter.artifact_type_2_id, exporter.id_2_artifact = TraceDatasetCreator.create_artifact_maps(project_data["artifact_df"])
        exporter.create_artifact_definitions(project_data["layer_mapping_df"], export_path)
        exporter.create_trace_definitions(project_data["traces"], project_data["layer_mapping_df"], export_path)
        exporter.create_tim(export_path)

    def create_artifact_definitions(self, layer_mapping_df: pd.DataFrame, export_path: str) -> None:
        """
        Creates dataframe for each artifact grouped by type.
        :return: None
        """
        artifact_types = set()
        for _, row in layer_mapping_df.iterrows():
            source_type = row[StructuredKeys.LayerMapping.SOURCE_TYPE]
            target_type = row[StructuredKeys.LayerMapping.TARGET_TYPE]
            artifact_types.update({source_type, target_type})

        for artifact_type in artifact_types:
            entries: List[Dict] = []
            for artifact_id in self.artifact_type_2_id[artifact_type]:
                artifact: Artifact = self.id_2_artifact[artifact_id]
                entries.append({
                    StructuredKeys.Artifact.ID: artifact.id,
                    StructuredKeys.Artifact.BODY: artifact.token,
                })
            file_name = artifact_type + ".csv"
            local_export_path = os.path.join(export_path, file_name)
            pd.DataFrame(entries).to_csv(local_export_path, index=False, encoding="utf-8")
            self.artifact_definitions[artifact_type] = {
                SafaKeys.FILE: file_name
            }

    def create_trace_definitions(self, links: Dict[int, TraceLink], layer_mapping_df: pd.DataFrame, export_path: str) -> None:
        """
        Create trace definition between each layer in trace creator.
        :param links: The trace links to save.
        :param layer_mapping_df: DataFrame mapping trace queries in project.
        :return: None
        """
        for _, row in layer_mapping_df.iterrows():
            source_type = row[StructuredKeys.LayerMapping.SOURCE_TYPE]
            target_type = row[StructuredKeys.LayerMapping.TARGET_TYPE]
            matrix_name = f"{source_type}2{target_type}"
            file_name = matrix_name + ".csv"
            export_file_path = os.path.join(export_path, file_name)
            trace_df = self.create_trace_df(links, source_type, target_type)
            self.trace_definitions[matrix_name] = {
                "File": file_name,
                "Source": source_type,
                "Target": target_type
            }
            trace_df.to_csv(export_file_path, index=False, encoding="utf-8")

    def create_trace_df(self, links: Dict[int, TraceLink], source_type, target_type) -> pd.DataFrame:
        """
        Creates data frame containing positive traces between source and target types.
        :param links: The links to save.
        :param source_type: The name of the source type.
        :param target_type: The name of the target type.
        :return: DataFrame with positive links.
        """
        source_artifact_ids = self.artifact_type_2_id[source_type]
        target_artifact_ids = self.artifact_type_2_id[target_type]
        entries = []
        for source_id in source_artifact_ids:
            for target_id in target_artifact_ids:
                trace_link_id = TraceLink.generate_link_id(source_id, target_id)
                trace_link: TraceLink = links[trace_link_id]
                if trace_link.is_true_link:
                    entries.append({
                        StructuredKeys.Trace.SOURCE: source_id,
                        StructuredKeys.Trace.TARGET: target_id
                    })
        return pd.DataFrame(entries)

    def create_tim(self, export_path) -> None:
        """
        Writes TIM file to export path.
        :return: None
        """
        tim_definition = {
            "DataFiles": {
                **self.artifact_definitions
            },
            **self.trace_definitions
        }
        export_path = os.path.join(export_path, "tim.json")
        FileUtil.write(tim_definition, export_path)
