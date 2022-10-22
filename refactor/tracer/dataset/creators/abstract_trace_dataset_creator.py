from abc import ABC, abstractmethod
from typing import List, Union, Set, Dict, Tuple

import pandas as pd
from tracer.dataset.data_objects.artifact import Artifact
from tracer.dataset.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.dataset.trace_dataset import TraceDataset
from tracer.dataset.data_objects.trace_link import TraceLink
from tracer.pre_processing.pre_processor import PreProcessor


class Keys:
    
    def __init__(self, artifact_id_key: str, artifact_token_key: str, source_id_key: str, target_id_key: str,
                 artifacts_key: str = '', traces_key: str = ''):
        self.artifact_id_key = artifact_id_key
        self.artifact_token_key = artifact_token_key
        self.source_id_key = source_id_key
        self.target_id_key = target_id_key
        self.artifacts_key = artifacts_key
        self.traces_key = traces_key


class AbstractTraceDatasetCreator(AbstractDatasetCreator, ABC):

    def __init__(self, pre_processor: PreProcessor, use_linked_targets_only: bool):
        """
        Responsible for creating dataset in format for defined models.
        :pre_processor: the pre_processor to run on the data
        :use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(pre_processor)
        self._linked_targets = set()
        self.use_linked_targets_only = use_linked_targets_only

    @abstractmethod
    def create(self) -> TraceDataset:
        """
        Creates the trace dataset
        :return: the dataset
        """
        pass

    @staticmethod
    @abstractmethod
    def _read_data_file(project_path: str, data_file_name: str, data_key: str) -> pd.Dataframe:
        """
        Returns file content as dataframe.
        :param project_path: Path to project dir
        :param data_file_name: name of the data file
        :param data_key: the key to access data within the file (e.g. for json files)
        :return: dataframe containing file content.
        """
        pass

    def _create_dataset_params_from_files(self, keys: Keys, project_path: str, trace_files_2_artifacts: Dict[str, Tuple[str, str]]) \
            -> Tuple[Dict[int, TraceLink], Set[int], Set[int]]:
        """
        Creates dataset params from dataset files
        :param keys: keys used to access data in dataframe
        :param project_path: the path to the project
        :param trace_files_2_artifacts: a dictionary mapping trace file name to source and target artifact names
        :return: the links, pos_link-ids, and neg_link_ids
        """
        links = {}
        pos_link_ids = set()
        for trace_file, source_target_files in trace_files_2_artifacts.items():
            source_artifacts = self._create_artifacts_from_file(keys, project_path, source_target_files[0])
            target_artifacts = self._create_artifacts_from_file(keys, project_path, source_target_files[1])
            layer_pos_link_ids = self._get_pos_link_ids_from_file(keys, project_path, trace_file)
            pos_link_ids.union(layer_pos_link_ids)
            links.update(self._create_links_for_layer(source_artifacts, target_artifacts, layer_pos_link_ids))
        neg_link_ids = set(links.keys()).difference(pos_link_ids)
        return links, pos_link_ids, neg_link_ids

    def _create_artifacts_from_file(self, keys: Keys, repo_path: str, data_file_name: str) -> List[Artifact]:
        """
        Create artifacts in artifact file.
        :param keys: keys used to access data in dataframe
        :param repo_path: The path to the project containing artifact file.
        :param data_file_name: The name of the artifact file to read.
        :return: List of artifacts in file.
        """
        artifacts_file = self._read_data_file(repo_path, data_file_name, keys.artifacts_key)

        artifacts = []
        for i, row in artifacts_file.iterrows():
            artifact_tokens = self._process_tokens(row[keys.artifact_token_key])
            if artifact_tokens:
                artifacts.append(Artifact(row[keys.artifact_id_key], artifact_tokens))

        return artifacts

    def _get_pos_link_ids_from_file(self, keys: Keys, project_path: str, data_file_name: str) -> Set[int]:
        """
        Extracts positive trace links from trace files in project.
        :param keys: keys used to access data in dataframe
        :param project_path: The path to the project files.
        :return: Trace link ids of positive links.
        """
        links_df = self._read_data_file(project_path, data_file_name, keys.traces_key)
        return self._get_pos_link_ids([(link[keys.source_id_key], link[keys.target_id_key])
                                       for _, link in links_df.iterrows()])

    def _create_links_for_layer(self, source_artifacts: List[Artifact], target_artifacts: List[Artifact],
                                pos_link_ids: Set[int]) -> Dict[int, TraceLink]:
        """
        Creates map between trace link id to trace link.
        :param source_artifacts: The source artifacts to extract links for.
        :param target_artifacts: The target artifacts to extract links for.
        :param pos_link_ids: The list of all positive link ids in project.
        :return: Map between trace link ids and trace links for given source and target artifacts.
        """
        if self.use_linked_targets_only:
            target_artifacts = self._filter_unlinked_targets(target_artifacts)

        links = {}
        for source in source_artifacts:
            for target in target_artifacts:
                link = TraceLink(source, target)
                link.is_true_link = link.id in pos_link_ids
                links[link.id] = link
        return links

    def _get_pos_link_ids(self, true_links: List[Tuple[str, str]]) -> Set[int]:
        """
        Creates a set of all positive and negative link ids
        :param true_links: list of tuples containing linked source and target ids
        :return: a list of the positive link ids, and a list of the negative link ids
        """
        pos_link_ids = set()
        for source_id, target_id in true_links:
            link_id = TraceLink.generate_link_id(source_id, target_id)
            pos_link_ids.add(link_id)
            self._linked_targets.add(target_id)
        return pos_link_ids

    def _filter_unlinked_targets(self, all_target_artifacts: List[Artifact]) -> List[Artifact]:
        """
        Gets only the target artifacts that are part of at least one true link
        :param all_target_artifacts: a list of all target artifacts
        :return: a list of linked target artifacts only
        """
        return [artifact for artifact in all_target_artifacts if artifact.id in self._linked_targets]
