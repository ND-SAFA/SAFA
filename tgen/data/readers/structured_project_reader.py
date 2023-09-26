import os
from typing import Dict

import pandas as pd

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.json_util import JsonUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.safa_keys import SafaKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.readers.abstract_project_reader import AbstractProjectReader, TraceDataFramesTypes
from tgen.data.readers.definitions.abstract_project_definition import AbstractProjectDefinition
from tgen.data.readers.definitions.structure_project_definition import StructureProjectDefinition
from tgen.data.readers.definitions.tim_project_definition import TimProjectDefinition
from tgen.data.readers.entity.entity_reader import EntityReader


class StructuredProjectReader(AbstractProjectReader[TraceDataFramesTypes]):
    """
    Responsible for reading artifacts and trace links and constructing
    a trace dataset.
    """

    def __init__(self, project_path: str, conversions=None, overrides: dict = None):
        """
        Creates reader for project at path and column definitions given.
        :param project_path: Path to the project.
        :param conversions: Column definitions available to project.
        """
        super().__init__(overrides, project_path)
        if conversions is None:
            conversions = {}
        self.definition_reader = None
        self._definition = None
        self.conversions = conversions

    def read_project(self) -> TraceDataFramesTypes:
        """
        Reads artifact and trace links from files.
        :return: Returns DataFrames containing artifacts, traces, and mapping between layers.
        """
        definition = self.get_project_definition()
        self.overrides.update(definition.get(StructuredKeys.OVERRIDES, {}))
        artifact_df = self.read_artifact_df()
        trace_df = self._read_trace_df()
        layer_mapping_df = self._read_layer_mapping_df()
        logger.info(f"Artifacts: {len(artifact_df)} Traces: {len(trace_df)} Queries: {len(layer_mapping_df)}")
        return artifact_df, trace_df, layer_mapping_df

    def get_project_definition(self) -> Dict:
        """
        Gets the definition for reading the project in the correct format
        :return: The definition for reading the project in the correct format
        """
        if self._definition is None:
            self.definition_reader = self.get_definition_reader()
            self._definition = self.definition_reader.read_project_definition(self.get_full_project_path())
        return self._definition

    def get_project_conversions(self) -> Dict:
        """
        Gets the definition for reading the project in the correct format
        :return: The definition for reading the project in the correct format
        """
        if not self.conversions:
            self.conversions = self.get_project_definition().get(StructuredKeys.CONVERSIONS, {})
        return self.conversions

    def get_project_name(self) -> str:
        """
        :return: Returns the name of the project directory.
        """
        return FileUtil.get_file_name(self.get_full_project_path())

    def read_artifact_df(self) -> pd.DataFrame:
        """
        Reads artifacts in project converting each to its own data frame.
        :return:  Mapping between artifacts' name and its reader.
        """
        artifact_df = ArtifactDataFrame()
        artifact_definitions = self._get_artifact_definitions()
        for artifact_type, artifact_definition in artifact_definitions.items():
            artifact_reader = EntityReader(self.get_full_project_path(),
                                           artifact_definition,
                                           conversions=self.get_project_conversions())
            artifact_type_df = artifact_reader.read_entities()
            artifact_type_df[StructuredKeys.Artifact.LAYER_ID.value] = artifact_type
            artifact_df = pd.concat([artifact_df, artifact_type_df], ignore_index=True)
        final_df = ArtifactDataFrame(artifact_df)
        if self.summarizer:
            final_df.summarize_content(self.summarizer)
        return final_df

    def _read_trace_df(self) -> pd.DataFrame:
        """
        Reads trace matrix files and aggregates them into single data frame.
        :return: DataFrame containing all trace links read from project.
        """
        trace_links = TraceDataFrame()
        for _, trace_definition_json in self._get_trace_definitions().items():
            trace_reader = EntityReader(self.get_full_project_path(), trace_definition_json,
                                        conversions=self.get_project_conversions())
            trace_links = pd.concat([trace_links, trace_reader.read_entities()], ignore_index=True)
        trace_links[StructuredKeys.Trace.LABEL.value] = [1 for link in trace_links.index]
        return TraceDataFrame(trace_links)

    def _read_layer_mapping_df(self) -> pd.DataFrame:
        """
        Creates DataFrame containing entries mapping layers to generate trace links for.
        :return: DataFrame containing layer mappings.
        """
        entries = []
        for _, trace_definition_json in self._get_trace_definitions().items():
            trace_definition_json = EnumDict(trace_definition_json)
            source_layer_id = trace_definition_json[StructuredKeys.Trace.SOURCE]
            target_layer_id = trace_definition_json[StructuredKeys.Trace.TARGET]
            entries.append(EnumDict({
                StructuredKeys.LayerMapping.SOURCE_TYPE: source_layer_id,
                StructuredKeys.LayerMapping.TARGET_TYPE: target_layer_id
            }))
        return LayerDataFrame(entries)

    def _get_artifact_definitions(self) -> Dict[str, Dict]:
        """
        Returns project's artifact definitions.
        :return: Artifact name to definition mapping.
        """
        definition = self.get_project_definition()
        JsonUtil.require_properties(definition, [StructuredKeys.ARTIFACTS])
        return definition[StructuredKeys.ARTIFACTS]

    def _get_trace_definitions(self) -> Dict[str, Dict]:
        """
        Returns project's trace definitions.
        :return: Mapping of trace matrix name to its trace defintion.
        """
        definition = self.get_project_definition()
        JsonUtil.require_properties(definition, [StructuredKeys.TRACES])
        return definition[StructuredKeys.TRACES]

    def get_definition_reader(self, raise_exception: bool = True) -> AbstractProjectDefinition:
        """
        If tim.json file exists in project, then TimProjectDefinition is returned. Otherwise, StructuredProjectDefinition is returned.
        :return: AbstractProjectDefinition corresponding to definition file found.
        """
        tim_path = os.path.join(self.get_full_project_path(), SafaKeys.TIM_FILE)
        structure_definition_path = os.path.join(self.get_full_project_path(), StructureProjectDefinition.STRUCTURE_DEFINITION_FILE_NAME)
        if os.path.exists(tim_path):
            return TimProjectDefinition()
        elif os.path.exists(structure_definition_path):
            return StructureProjectDefinition()
        else:
            required_paths = [tim_path, structure_definition_path]
            if raise_exception:
                raise ValueError(f"{self.get_full_project_path()} does not contain: {required_paths}")
