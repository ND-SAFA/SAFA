import json
import os
from typing import Callable, Dict, List, Set

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.dataset.data_objects.artifact import Artifact
from tracer.dataset.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator, Keys
from tracer.dataset.trace_dataset import TraceDataset
from tracer.pre_processing.pre_processor import PreProcessor
import pandas as pd


class SafaKeys(Keys):
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

    def __init__(self):
        super().__init__(SafaKeys.ARTIFACT_ID, SafaKeys.ARTIFACT_TOKEN, SafaKeys.SOURCE_ID, SafaKeys.TARGET_ID, SafaKeys.ARTIFACTS, SafaKeys.TRACES)


class SafaDatasetCreator(AbstractTraceDatasetCreator):
    TRACE_FILES_2_ARTIFACTS = {SafaKeys.FR2SG_FILE: (SafaKeys.FUNCTIONAL_REQUIREMENTS_FILE, SafaKeys.SAFETY_GOALS_FILE),
                               SafaKeys.SR2FR_FILE: (
                                   SafaKeys.SYSTEM_REQUIREMENTS_FILE, SafaKeys.FUNCTIONAL_REQUIREMENTS_FILE),
                               SafaKeys.SWR2SR_FILE: (
                                   SafaKeys.SOFTWARE_REQUIREMENTS_FILE, SafaKeys.SYSTEM_REQUIREMENTS_FILE),
                               SafaKeys.HWR2SR_FILE: (
                                   SafaKeys.HARDWARE_REQUIREMENTS_FILE, SafaKeys.SYSTEM_REQUIREMENTS_FILE)}

    def __init__(self, project_path: str, pre_processor: PreProcessor,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Creates a dataset from the SAFA dataset format.
        :param project_path: the path to the project
        :param pre_processor: the pre_processor to run on the data
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(pre_processor, use_linked_targets_only)
        self.project_path = project_path

    def create(self) -> TraceDataset:
        """
        Creates the dataset
        :return: the dataset
        """
        links, pos_link_ids, neg_link_ids = self._create_dataset_params_from_files(SafaKeys(),
                                                                                   self.project_path,
                                                                                   self.TRACE_FILES_2_ARTIFACTS)
        return TraceDataset(links, list(pos_link_ids), list(neg_link_ids))

    @staticmethod
    def _read_data_file(project_path: str, data_file_name: str, data_key: str) -> pd.Dataframe:
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
