import json
from typing import Dict, Generic, List, Tuple, TypeVar

import pandas as pd
from github.Issue import Issue

from data.github.entities.commit import Commit
from data.github.entities.github_artifact_type import GithubArtifactType
from data.github.entities.github_link import Link
from data.github.entities.github_pull import GithubPull

T = TypeVar('T', bound="AbstractArtifact")


class RepositoryArtifactSet(Generic[T]):
    """
    Represent a set of artifacts associated with an artifact type.
    """
    ID_PARAM = "id"
    BODY_PARAM = "body"
    TYPE_PARAM = "type"
    ARTIFACT_PARAM = "artifacts"

    def __init__(self, artifacts: List[T], artifact_type: GithubArtifactType):
        self.artifact_type = artifact_type
        self.artifacts = artifacts
        self.artifact_ids = [artifact.get_id() for artifact in artifacts]
        self.id2artifact = self.__create_id2artifact(self.artifact_ids, self.artifacts)

    def save(self, output_file_path: str):
        """
        Saves list of artifacts to a file.
        :param output_file_path: The path to the file to save to.
        :return: None
        """
        values = [artifact.to_dict() for artifact in self.artifacts]
        file_content = {
            RepositoryArtifactSet.TYPE_PARAM: self.artifact_type.value,
            RepositoryArtifactSet.ARTIFACT_PARAM: values
        }

        with open(output_file_path, mode="w") as output_file:
            output_file.write(json.dumps(file_content, indent=4))

    @staticmethod
    def load(data_file_path: str) -> "RepositoryArtifactSet":
        """
        Reads data file, loads artifacts, and constructs artifact set.
        :param data_file_path: The path to the data file.
        :return: Artifact set with loaded artifacts.
        """
        artifacts, artifact_type = RepositoryArtifactSet.__read_data_file(data_file_path)
        return RepositoryArtifactSet(artifacts, artifact_type)

    def export_training_data(self, output_file_path: str, columns: List[str] = None, dataset_type: str = "NL"):
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

    def filter(self, artifact_ids: List[str]) -> "RepositoryArtifactSet":
        """
        Returns artifact set without artifact ids.
        :param artifact_ids: The ids of the artifacts to remove.
        :return: New artifact set with artifacts removed.
        """
        new_artifacts = [artifact for artifact in self.artifacts if artifact.get_id() in artifact_ids]
        return RepositoryArtifactSet(new_artifacts, self.artifact_type)

    @staticmethod
    def __read_data_file(artifact_file_path: str) -> Tuple[List[T], GithubArtifactType]:
        with open(artifact_file_path) as data_file:
            file_content = json.loads(data_file.read())
            artifact_type = GithubArtifactType[file_content[RepositoryArtifactSet.TYPE_PARAM].upper()]
            artifacts = file_content[RepositoryArtifactSet.ARTIFACT_PARAM]
            abstract_artifact_class = RepositoryArtifactSet.__get_builder_for_type(artifact_type)
            return [abstract_artifact_class.read(row) for row in artifacts], artifact_type

    @staticmethod
    def __get_builder_for_type(artifact_type: GithubArtifactType):
        if artifact_type == GithubArtifactType.LINK:
            return Link
        if artifact_type == GithubArtifactType.COMMIT:
            return Commit
        if artifact_type == GithubArtifactType.ISSUE:
            return Issue
        if artifact_type == GithubArtifactType.PULL_REQUEST:
            return GithubPull
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
