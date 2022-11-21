import json
import os
from typing import Dict, List, Set, Tuple

import pandas as pd

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.datasets.data_objects.artifact import Artifact
from tracer.datasets.trace_dataset import TraceDataset
from tracer.pre_processing.steps.abstract_pre_processing_step import AbstractPreProcessingStep


class SafaKeys:
    SAFETY_GOALS_FILE = "sg.json"
    SYSTEM_REQUIREMENTS_FILE = "SYS.json"
    FUNCTIONAL_REQUIREMENTS_FILE = "fsr.json"
    SOFTWARE_REQUIREMENTS_FILE = "swr.json"
    HARDWARE_REQUIREMENTS_FILE = "hwr.json"
    FR2SG_FILE = "fsr2sg.json"
    SR2FR_FILE = "SYS2fsr.json"
    SWR2SR_FILE = "swr2SYS.json"
    HWR2SR_FILE = "hwr2SYS.json"

    ARTIFACT_ID = "name"
    ARTIFACT_TOKEN = "body"
    SOURCE_ID = "sourceName"
    TARGET_ID = "targetName"
    ARTIFACTS = "artifacts"
    TRACES = "traces"

    TRACE_FILES_2_ARTIFACTS = {FR2SG_FILE: (FUNCTIONAL_REQUIREMENTS_FILE, SAFETY_GOALS_FILE),
                               SR2FR_FILE: (
                                   SYSTEM_REQUIREMENTS_FILE, FUNCTIONAL_REQUIREMENTS_FILE),
                               SWR2SR_FILE: (
                                   SOFTWARE_REQUIREMENTS_FILE, SYSTEM_REQUIREMENTS_FILE),
                               HWR2SR_FILE: (
                                   HARDWARE_REQUIREMENTS_FILE, SYSTEM_REQUIREMENTS_FILE)}

    def __init__(self, artifact_id_key: str = ARTIFACT_ID, artifact_token_key: str = ARTIFACT_TOKEN,
                 source_id_key: str = SOURCE_ID,
                 target_id_key: str = TARGET_ID, artifacts_key: str = ARTIFACTS, traces_key: str = TRACES,
                 trace_files_2_artifacts: Dict[str, Tuple[str, str]] = None):
        self.artifact_id_key = artifact_id_key
        self.artifact_token_key = artifact_token_key
        self.source_id_key = source_id_key
        self.target_id_key = target_id_key
        self.artifacts_key = artifacts_key
        self.traces_key = traces_key
        self.trace_files_2_artifacts = trace_files_2_artifacts if trace_files_2_artifacts else SafaKeys.TRACE_FILES_2_ARTIFACTS


class SafaDatasetCreator(AbstractTraceDatasetCreator):
    JSON_EXT = ".json"
    CSV_EXT = ".csv"
    KEYS = SafaKeys()

    def __init__(self, project_path: str, pre_processing_steps: List[AbstractPreProcessingStep] = None,
                 data_keys: SafaKeys = KEYS, use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Creates a datasets from the SAFA datasets format.
        :param project_path: the path to the project
        :param pre_processing_steps: tuple containing the desired pre-processing steps and related params
        :param data_keys: keys to use to access data
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(pre_processing_steps, use_linked_targets_only)
        self.project_path = project_path
        self.keys = data_keys

    def create(self) -> TraceDataset:
        """
        Creates the datasets
        :return: the datasets
        """
        return self._create_dataset_from_files(self.keys)

    def _create_dataset_from_files(self, keys: SafaKeys) -> TraceDataset:
        """
        Creates datasets params from datasets files
        :param keys: keys used to access data in dataframe
        :return: the links, pos_link-ids, and neg_link_ids
        """
        links = {}
        pos_link_ids = set()
        for trace_file, source_target_files in keys.trace_files_2_artifacts.items():
            source_artifacts = self._create_artifacts_from_file(source_target_files[0])
            target_artifacts = self._create_artifacts_from_file(source_target_files[1])
            layer_pos_link_ids = self._get_pos_link_ids_from_file(trace_file)
            pos_link_ids = pos_link_ids.union(layer_pos_link_ids)
            links.update(self._create_links_for_layer(source_artifacts, target_artifacts, layer_pos_link_ids))
        neg_link_ids = set(links.keys()).difference(pos_link_ids)
        return TraceDataset(links, list(pos_link_ids), list(neg_link_ids))

    def _create_artifacts_from_file(self, data_file_name: str) -> List[Artifact]:
        """
        Create artifacts in artifact file.
        :param data_file_name: The name of the artifact file to read.
        :return: List of artifacts in file.
        """
        artifacts_file = self._read_data_file(self.project_path, data_file_name, self.keys.artifacts_key)

        artifacts = []
        for i, row in artifacts_file.iterrows():
            artifact_tokens = self._process_tokens(row[self.keys.artifact_token_key])
            if artifact_tokens:
                artifacts.append(Artifact(row[self.keys.artifact_id_key], artifact_tokens))

        return artifacts

    def _get_pos_link_ids_from_file(self, data_file_name: str) -> Set[int]:
        """
        Extracts positive trace links from trace files in project.
        :return: Trace link ids of positive links.
        """
        links_df = self._read_data_file(self.project_path, data_file_name, self.keys.traces_key)
        return self._get_pos_link_ids([(link[self.keys.source_id_key], link[self.keys.target_id_key])
                                       for _, link in links_df.iterrows()])

    @staticmethod
    def _read_data_file(project_path: str, data_file_name: str, data_key: str) -> pd.DataFrame:
        """
        Returns file content as dataframe.
        :param project_path: Path to project dir
        :param data_file_name: name of the data file
        :param data_key: used to access the list of dictionaries in a json file
        :return: dataframe containing file content.
        """
        ext = os.path.splitext(data_file_name)[-1]
        if ext == SafaDatasetCreator.JSON_EXT:
            data_read_method = SafaDatasetCreator._read_json_file
        elif ext == SafaDatasetCreator.CSV_EXT:
            data_read_method = SafaDatasetCreator._read_csv_file
        else:
            raise Exception("Unknown file type %s" % ext)

        return data_read_method(project_path, data_file_name, data_key)

    @staticmethod
    def _read_json_file(project_path: str, data_file_name: str, data_key: str) -> pd.DataFrame:
        """
        Returns JSON file content as dataframe.
        :param project_path: Path to project dir
        :param data_file_name: name of the data file
        :param data_key: used to access the list of dictionaries in a json file
        :return: dataframe containing file content.
        """
        path_to_file = os.path.join(project_path, data_file_name)
        with open(path_to_file, "r") as json_file:
            json_content = json.loads(json_file.read())
        return pd.json_normalize(json_content[data_key])

    @staticmethod
    def _read_csv_file(project_path: str, data_file_name: str, data_key: str = ''):
        """
        Returns CSV file content as dataframe.
        :param project_path: Path to project dir
        :param data_file_name: name of the data file
        :param data_key: the key to access data within the file (not used)
        :return: dataframe containing file content.
        """
        return pd.read_csv(os.path.join(project_path, data_file_name))
