import json
import os
from typing import Callable, Dict, List, Set

from tracer.dataset.artifact import Artifact
from tracer.dataset.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.dataset.trace_dataset import TraceDataset
from tracer.dataset.trace_link import TraceLink


class SafaKey:
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
    ARTIFACTS = "artifacts"
    SOURCE_ID = "sourceName"
    TARGET_ID = "targetName"
    TRACES = "traces"


class SafaDatasetCreator(AbstractDatasetCreator):
    ARTIFACT_FILES = [SafaKey.SAFETY_GOALS_FILE, SafaKey.FUNCTIONAL_REQUIREMENTS_FILE, SafaKey.SYSTEM_REQUIREMENTS_FILE,
                      SafaKey.SOFTWARE_REQUIREMENTS_FILE, SafaKey.HARDWARE_REQUIREMENTS_FILE]
    TRACE_FILE_2_ARTIFACT = {SafaKey.FR2SG_FILE: (SafaKey.FUNCTIONAL_REQUIREMENTS_FILE, SafaKey.SAFETY_GOALS_FILE),
                             SafaKey.SR2FR_FILE: (
                                 SafaKey.SYSTEM_REQUIREMENTS_FILE, SafaKey.FUNCTIONAL_REQUIREMENTS_FILE),
                             SafaKey.SWR2SR_FILE: (
                                 SafaKey.SOFTWARE_REQUIREMENTS_FILE, SafaKey.SYSTEM_REQUIREMENTS_FILE),
                             SafaKey.HWR2SR_FILE: (
                                 SafaKey.HARDWARE_REQUIREMENTS_FILE, SafaKey.SYSTEM_REQUIREMENTS_FILE)}

    def __init__(self, project_path: str):
        """
        Creates a dataset from the SAFA dataset format.
        :param project_path: the path to the project
        """
        super().__init__()
        self.project_path = project_path

    def create(self) -> TraceDataset:
        """
        Creates the dataset
        :return: the dataset
        """
        artifact_layers = self._create_artifacts(self.project_path)
        pos_link_ids = self._get_pos_link_ids_from_files(self.project_path)
        links = self._create_links(artifact_layers, pos_link_ids)
        neg_link_ids = set(links.keys()).difference(pos_link_ids)
        return TraceDataset(links=links, pos_link_ids=list(pos_link_ids), neg_link_ids=list(neg_link_ids))

    def _create_artifacts(self, project_path: str) -> Dict[str, List[Artifact]]:
        """
        Creates map between artifact file to their artifacts.
        :param project_path: Path to project containing artifact files.
        :return: The map between artifact file to its artifacts.
        """
        artifact_layers = {}
        for artifact_file in SafaDatasetCreator.ARTIFACT_FILES:
            artifact_layers[artifact_file] = self._create_artifacts_from_file(project_path, artifact_file)
        return artifact_layers

    def _create_artifacts_from_file(self, project_path: str, data_file_name: str) -> List[Artifact]:
        """
        Create artifacts in artifact file.
        :param project_path: The path to the project containing artifact file.
        :param data_file_name: The name of the artifact file to read.
        :return: List of artifacts in file.
        """
        data_file_path = os.path.join(project_path, data_file_name)
        data_file = SafaDatasetCreator.__read_json_file(data_file_path)
        artifacts = []
        for artifact_entry in data_file[SafaKey.ARTIFACTS]:

            artifact_tokens = self._process_artifact_tokens([SafaKey.ARTIFACT_TOKEN])

            artifacts.append(
                Artifact(artifact_entry[SafaKey.ARTIFACT_ID], artifact_tokens))
        return artifacts

    def _get_pos_link_ids_from_files(self, project_path: str) -> Set[int]:
        """
        Exracts positive trace links from trace and artifact files in project.
        :param project_path: The path to the project files.
        :return: Trace link ids of positive links.
        """
        pos_link_ids = set()
        for trace_file, artifact_files in SafaDatasetCreator.TRACE_FILE_2_ARTIFACT.items():
            data_file_path = os.path.join(project_path, trace_file)
            data_file = SafaDatasetCreator.__read_json_file(data_file_path)
            layer_pos_link_ids = self._get_pos_link_ids(
                [(trace[SafaKey.SOURCE_ID], trace[SafaKey.TARGET_ID]) for trace in data_file[SafaKey.TRACES]])
            pos_link_ids.union(layer_pos_link_ids)
        return pos_link_ids

    def _create_links(self, artifact_layers: Dict[str, List[Artifact]], pos_link_ids: Set[int]) -> Dict[int, TraceLink]:
        """
        Creates mapping of trace links ids to their trace links between artifact layers.
        :param artifact_layers: Map between artifact file and its artifacts.
        :param pos_link_ids: Set of positive link ids.
        :return: Map of trace link ids to trace links.
        """
        links = {}
        for trace_file, artifact_files in SafaDatasetCreator.TRACE_FILE_2_ARTIFACT:
            source_artifacts = artifact_layers.get(artifact_files[0])
            target_artifacts = artifact_layers.get(artifact_files[1])
            layer_links = self._create_links_for_layer(source_artifacts, target_artifacts, pos_link_ids)
            links.update(layer_links)
        return links

    @staticmethod
    def __read_json_file(path_to_file: str) -> Dict:
        """
        Returns JSON file content as dictionary.
        :param path_to_file: Path to JSON file.
        :return: Dict representing file content.
        """
        with open(path_to_file, "r") as json_file:
            json_content = json.loads(json_file.read())
            return json_content
