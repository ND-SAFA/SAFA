import os
from typing import Dict, Tuple

import pandas as pd

from data.keys.safa_format import SafaKeys
from data.keys.structure_keys import StructuredKeys
from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.definitions.abstract_project_definition import AbstractProjectDefinition
from data.readers.definitions.structure_project_definition import StructureProjectDefinition
from data.readers.definitions.tim_project_definition import TimProjectDefinition
from data.readers.entity.entity_reader import EntityReader
from util.file_util import FileUtil
from util.json_util import JsonUtil
from util.override import overrides


class StructuredProjectReader(AbstractProjectReader):
    """
    Responsible for reading artifacts and trace links and constructing
    a trace dataset.
    """

    def __init__(self, project_path: str, conversions=None):
        """
        Creates reader for project at path and column definitions given.
        :param project_path: Path to the project.
        :param conversions: Column definitions available to project.
        """
        if conversions is None:
            conversions = {}
        self.project_path = project_path
        self.definition_reader = self._get_definition_reader()
        self.definition = None
        self.conversions = conversions

    def read_project(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Reads artifact and trace links from files.
        :return: Returns DataFrames containing artifacts, traces, and mapping between layers.
        """
        self.definition = self.definition_reader.read_project_definition(self.project_path)
        self.conversions = self.definition.get(StructuredKeys.CONVERSIONS, self.conversions)
        self.overrides = self.definition.get(StructuredKeys.OVERRIDES, {})
        artifact_df = self._read_artifact_df(self.project_path, self._get_artifact_definitions())
        trace_df = self._read_trace_df()
        layer_mapping_df = self._read_layer_mapping_df()
        return artifact_df, trace_df, layer_mapping_df

    def get_project_name(self) -> str:
        """
        :return: Returns the name of the project directory.
        """
        return FileUtil.get_file_name(self.project_path)

    @overrides(AbstractProjectReader)
    def get_overrides(self) -> Dict:
        """
        :return: Returns properties to override defined in project definition.
        """
        return {k.upper(): v for k, v in self.overrides.items()}

    def _read_artifact_df(self, project_path: str, type2definition: Dict[str, Dict]) -> pd.DataFrame:
        """
        Reads artifacts in project converting each to its own data frame.
        :param project_path: Path to project.
        :param type2definition: Mapping between artifacts' name and definition.
        :return:  Mapping between artifacts' name and its reader.
        """
        artifacts_df = pd.DataFrame()
        for artifact_type, artifact_definition in type2definition.items():
            artifact_reader = EntityReader(project_path,
                                           artifact_definition,
                                           conversions=self.conversions)
            artifact_type_df = artifact_reader.read_entities()
            artifact_type_df[StructuredKeys.Artifact.LAYER_ID] = artifact_type
            artifacts_df = pd.concat([artifacts_df, artifact_type_df], ignore_index=True)
        return artifacts_df

    def _read_trace_df(self) -> pd.DataFrame:
        """
        Reads trace matrix files and aggregates them into single data frame.
        :return: DataFrame containing all trace links read from project.
        """
        trace_links = pd.DataFrame()
        for _, trace_definition_json in self._get_trace_definitions().items():
            trace_reader = EntityReader(self.project_path, trace_definition_json,
                                        conversions=self.conversions)
            trace_links = pd.concat([trace_links, trace_reader.read_entities()], ignore_index=True)
        return trace_links

    def _read_layer_mapping_df(self) -> pd.DataFrame:
        """
        Creates DataFrame containing entries mapping layers to generate trace links for.
        :return: DataFrame containing layer mappings.
        """
        entries = []
        for _, trace_definition_json in self._get_trace_definitions().items():
            source_layer_id = trace_definition_json[StructuredKeys.Trace.SOURCE]
            target_layer_id = trace_definition_json[StructuredKeys.Trace.TARGET]
            entries.append({
                StructuredKeys.LayerMapping.SOURCE_TYPE: source_layer_id,
                StructuredKeys.LayerMapping.TARGET_TYPE: target_layer_id
            })
        return pd.DataFrame(entries)

    def _get_artifact_definitions(self) -> Dict[str, Dict]:
        """
        Returns project's artifact definitions.
        :return: Artifact name to definition mapping.
        """
        JsonUtil.require_properties(self.definition, [StructuredKeys.ARTIFACTS])
        return self.definition[StructuredKeys.ARTIFACTS]

    def _get_trace_definitions(self) -> Dict[str, Dict]:
        """
        Returns project's trace definitions.
        :return: Mapping of trace matrix name to its trace defintion.
        """
        JsonUtil.require_properties(self.definition, [StructuredKeys.TRACES])
        return self.definition[StructuredKeys.TRACES]

    def _get_definition_reader(self) -> AbstractProjectDefinition:
        """
        If tim.json file exists in project, then TimProjectDefinition is returned. Otherwise, StructuredProjectDefinition is returned.
        :return: AbstractProjectDefinition corresponding to definition file found.
        """
        tim_path = os.path.join(self.project_path, SafaKeys.TIM_FILE)
        structure_definition_path = os.path.join(self.project_path, StructureProjectDefinition.STRUCTURE_DEFINITION_FILE_NAME)
        if os.path.exists(tim_path):
            return TimProjectDefinition()
        elif os.path.exists(structure_definition_path):
            return StructureProjectDefinition()
        else:
            required_paths = [tim_path, structure_definition_path]
            raise ValueError(f"{self.project_path} does not contain: {required_paths}")
