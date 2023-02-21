import json
from typing import Dict, Generic, List, Tuple, Type, TypeVar

import pandas as pd

from data.github.abstract_github_entity import AbstractGithubArtifact
from data.github.gartifacts.gartifact_type import GArtifactType
from data.github.gartifacts.gcommit import GCommit
from data.github.gartifacts.gissue import GIssue
from data.github.gartifacts.gpull import GPull
from data.github.gtraces.glink import GLink

T = TypeVar('T', bound="AbstractArtifact")


class GArtifactSet(Generic[T]):
    """
    Represent a set of artifacts associated with an artifact type.
    """
    ID_PARAM = "id"
    BODY_PARAM = "body"
    TYPE_PARAM = "type"
    ARTIFACT_PARAM = "artifacts"

    def __init__(self, artifacts: List[T], artifact_type: GArtifactType) -> object:
        self.artifact_type = artifact_type
        self.artifacts = artifacts
        self.artifact_ids = [artifact.get_id() for artifact in artifacts]
        self.id2artifact = self.__create_id2artifact(self.artifact_ids, self.artifacts)

    def save(self, output_file_path: str, columns: List[str] = None, dataset_type: str = "NL"):
        """
        Exports the id and body of the artifacts in the set.
        :param output_file_path: The path of the file to write to.
        :param columns: The columns of the CSV file. Define is artifact list of empty.
        :param dataset_type: The type of dataset to create. Either natural langauge or programming language.
        :return: None
        """
        df_values = []
        for artifact in self.artifacts:
            entry = artifact.export(dataset_type=dataset_type)
            if entry is None:
                continue
            df_values.append(entry)
        pd.DataFrame(df_values, columns=columns).to_csv(output_file_path, index=False)

    def filter(self, artifact_ids: List[str]) -> "GArtifactSet":
        """
        Returns artifact set without artifact ids.
        :param artifact_ids: The ids of the artifacts to remove.
        :return: New artifact set with artifacts removed.
        """
        new_artifacts = [artifact for artifact in self.artifacts if artifact.get_id() in artifact_ids]
        return GArtifactSet(new_artifacts, self.artifact_type)

    @staticmethod
    def load(data_file_path: str) -> "GArtifactSet":
        """
        Reads data file, loads artifacts, and constructs artifact set.
        :param data_file_path: The path to the data file.
        :return: Artifact set with loaded artifacts.
        """
        artifacts, artifact_type = GArtifactSet.__read_data_file(data_file_path)
        return GArtifactSet(artifacts, artifact_type)

    @staticmethod
    def __read_data_file(artifact_file_path: str) -> Tuple[List[T], GArtifactType]:
        with open(artifact_file_path) as data_file:
            file_content = json.loads(data_file.read())
            artifact_type_key = file_content[GArtifactSet.TYPE_PARAM].upper()
            artifact_type = GArtifactType[artifact_type_key]
            artifacts = file_content[GArtifactSet.ARTIFACT_PARAM]
            abstract_artifact_class = GArtifactSet.__get_builder_for_type(artifact_type)
            return [abstract_artifact_class.read(row) for row in artifacts], artifact_type

    @staticmethod
    def __get_builder_for_type(artifact_type: GArtifactType) -> Type[AbstractGithubArtifact]:
        if artifact_type == GArtifactType.LINK:
            return GLink
        if artifact_type == GArtifactType.COMMIT:
            return GCommit
        if artifact_type == GArtifactType.ISSUE:
            return GIssue
        if artifact_type == GArtifactType.PULL:
            return GPull
        else:
            raise Exception("Unknown artifact type: " + artifact_type.value)

    @staticmethod
    def __create_id2artifact(artifact_ids: List[str], artifacts: List[T]) -> Dict[str, T]:
        id2artifact = {}
        assert len(artifact_ids) == len(artifacts)
        for i, a_id in enumerate(artifact_ids):
            id2artifact[a_id] = artifacts[i]
        return id2artifact

    def __getitem__(self, artifact_id: str) -> T:
        return self.id2artifact[artifact_id]

    def __contains__(self, item):
        return item in self.artifact_ids

    def __len__(self):
        return len(self.artifacts)
