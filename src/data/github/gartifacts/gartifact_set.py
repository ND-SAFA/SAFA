import json
from typing import Generic, List, Tuple, Type, TypeVar

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

    def __init__(self, artifacts: List[T], artifact_type: GArtifactType):
        """
        Initializes artifact containing given artifacts.
        :param artifacts: The github artifacts.
        :param artifact_type: The type of github artifacts given.
        """
        self.artifact_type = artifact_type
        self.artifacts = artifacts
        self.artifact_ids = [artifact.get_id() for artifact in artifacts]

    def export(self, output_file_path: str, columns: List[str] = None, dataset_type: str = "NL") -> None:
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
        """
        Reads data file artifact type and its corresponding artifacts.
        :param artifact_file_path: The path to the artifact data file.
        :return: Tuple containing Github artifacts and their corresponding artifact type.
        """
        with open(artifact_file_path) as data_file:
            file_content = json.loads(data_file.read())
            artifact_type_key = file_content[GArtifactSet.TYPE_PARAM].upper()
            artifact_type = GArtifactType[artifact_type_key]
            artifacts = file_content[GArtifactSet.ARTIFACT_PARAM]
            abstract_artifact_class = GArtifactSet.__get_constructor_for_type(artifact_type)
            return [abstract_artifact_class.read(row) for row in artifacts], artifact_type

    @staticmethod
    def __get_constructor_for_type(artifact_type: GArtifactType) -> Type[AbstractGithubArtifact]:
        """
        Returns the constructor of the artifact for given type.
        :param artifact_type: The type of artifact to create.
        :return: Class constructor for given type.
        """
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

    def __contains__(self, artifact_id: str) -> bool:
        """
        Return whether artifact id contained in set.
        :param artifact_id: The artifact id to check for inclusion.
        :return: True is contained, false otherwise.
        """
        return artifact_id in self.artifact_ids

    def __len__(self) -> int:
        """
        :return: Returns the number of artifacts contained in set.
        """
        return len(self.artifacts)
