import json
import os
from typing import Callable, Dict, List, Set

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from tracer.dataset.artifact import Artifact
from tracer.dataset.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.dataset.trace_dataset import TraceDataset
from tracer.dataset.trace_link import TraceLink
from tracer.models.model_generator import ModelGenerator


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

    def __init__(self, project_path: str, model_generator: ModelGenerator,
                 validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT):
        """
        Creates a dataset from the SAFA dataset format.
        :param project_path: the path to the project
        :param model_generator: the model generator for the project
        :param validation_percentage: percentage of dataset used for validation, if no value is supplied then dataset will not be split
        """
        artifact_layers = self._create_artifacts(project_path, model_generator.get_feature)
        pos_link_ids = self._get_pos_link_ids(project_path)
        links = self._create_links(artifact_layers, pos_link_ids, model_generator.get_feature)
        neg_link_ids = set(links.keys()).difference(pos_link_ids)
        self.arch_type = model_generator.arch_type
        self.validation_percentage = validation_percentage
        self.dataset = TraceDataset(links=links, pos_link_ids=list(pos_link_ids),
                                    neg_link_ids=list(neg_link_ids))

    def create(self) -> TraceDataset:
        return self.dataset

    @staticmethod
    def _create_artifacts(project_path: str, feature_func: Callable) -> Dict[str, List[Artifact]]:
        """
        Creates map between artifact file to their artifacts.
        :param project_path: Path to project containing artifact files.
        :param feature_func: The function creating dataset features.
        :return: The map between artifact file to its artifacts.
        """
        artifact_layers = {}
        for artifact_file in SafaDatasetCreator.ARTIFACT_FILES:
            artifact_layers[artifact_file] = SafaDatasetCreator._create_artifacts_from_file(project_path, artifact_file,
                                                                                            feature_func)
        return artifact_layers

    @staticmethod
    def _get_pos_link_ids(project_path: str) -> Set[int]:
        """
        Exracts positive trace links from trace and artifact files in project.
        :param project_path: The path to the project files.
        :return: Trace link ids of positive links.
        """
        pos_link_ids = set()
        for trace_file, artifact_files in SafaDatasetCreator.TRACE_FILE_2_ARTIFACT.items():
            layer_pos_link_ids = SafaDatasetCreator._get_pos_link_ids_from_file(project_path, trace_file)
            pos_link_ids.union(layer_pos_link_ids)
        return pos_link_ids

    @staticmethod
    def _create_links(artifact_layers: Dict[str, List[Artifact]], pos_link_ids: Set[int], feature_func: Callable) \
            -> Dict[int, TraceLink]:
        """
        Creates mapping of trace links ids to their trace links between artifact layers.
        :param artifact_layers: Map between artifact file and its artifacts.
        :param pos_link_ids: Set of positive link ids.
        :param feature_func: Function for getting features from all link.
        :return: Map of trace link ids to trace links.
        """
        links = {}
        for trace_file, artifact_files in SafaDatasetCreator.TRACE_FILE_2_ARTIFACT:
            source_artifacts = artifact_layers.get(artifact_files[0])
            target_artifacts = artifact_layers.get(artifact_files[1])
            layer_links = SafaDatasetCreator._create_links_for_layer(source_artifacts, target_artifacts, pos_link_ids,
                                                                     feature_func)
            links.update(layer_links)
        return links

    @staticmethod
    def _create_links_for_layer(source_artifacts: List[Artifact], target_artifacts: List[Artifact],
                                pos_link_ids: Set[int], feature_func: Callable) -> Dict[int, TraceLink]:
        """
        Creates map between trace link id to trace link.
        :param source_artifacts: The source artifacts to extract links for.
        :param target_artifacts: The target artifacts to extract links for.
        :param pos_link_ids: The list of all positive link ids in project.
        :param feature_func: Function for getting features from trace links.
        :return: Map between trace link ids and trace links for given source and target artifacts.
        """
        links = {}
        for source in source_artifacts:
            for target in target_artifacts:
                link = TraceLink(source, target, feature_func)
                if link.id in pos_link_ids:
                    link.is_true_link = True
                links[link.id] = link
        return links

    @staticmethod
    def _create_artifacts_from_file(project_path: str, data_file_name: str, feature_func: Callable) -> List[Artifact]:
        """
        Create artifacts in artifact file.
        :param project_path: The path to the project containing artifact file.
        :param data_file_name: The name of the artifact file to read.
        :param feature_func: Function to get features from artifacts.
        :return: List of artifacts in file.
        """
        data_file_path = os.path.join(project_path, data_file_name)
        data_file = SafaDatasetCreator.__read_json_file(data_file_path)
        artifacts = []
        for artifact_entry in data_file[SafaKey.ARTIFACTS]:
            artifacts.append(
                Artifact(artifact_entry[SafaKey.ARTIFACT_ID], artifact_entry[SafaKey.ARTIFACT_TOKEN], feature_func))
        return artifacts

    @staticmethod
    def _get_pos_link_ids_from_file(project_path: str, data_file_name: str) -> Set[int]:
        """
        Gets set of positive ids in trace file.
        :param project_path: Path to project containing trace file.
        :param data_file_name: The name of the trace file.
        :return: Set of trace link ids.
        """
        data_file_path = os.path.join(project_path, data_file_name)
        data_file = SafaDatasetCreator.__read_json_file(data_file_path)
        pos_link_ids = set()
        for trace in data_file[SafaKey.TRACES]:
            source_id = trace[SafaKey.SOURCE_ID]
            target_id = trace[SafaKey.TARGET_ID]
            pos_link_ids.add(TraceLink.generate_link_id(source_id, target_id))
        return pos_link_ids

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
