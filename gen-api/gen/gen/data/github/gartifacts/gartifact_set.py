import json
import os
from typing import Dict, Generic, List, Tuple, Type, TypeVar

import pandas as pd
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.file_util import FileUtil

from gen.data.github.abstract_github_entity import AbstractGithubArtifact
from gen.data.github.gartifacts.gartifact_type import GArtifactType
from gen.data.github.gartifacts.supported_gartifacts import SupportedGArtifacts

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

    def save(self, output_file_path: str):
        """
        Saves list of artifacts to a file.
        :param output_file_path: The path to the file to save to.
        :return: None
        """
        values = [artifact.get_state_dict() for artifact in self.artifacts]
        file_content = {
            GArtifactSet.TYPE_PARAM: self.artifact_type.value,
            GArtifactSet.ARTIFACT_PARAM: values
        }

        with open(output_file_path, mode="w") as output_file:
            output_file.write(json.dumps(file_content, indent=4))
        logger.info(f"Saved entities to: {output_file_path}")

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
            entry = artifact.as_dataframe_entry(dataset_type=dataset_type)
            if entry is None:
                continue
            df_values.append(entry)
        FileUtil.create_dir_safely(os.path.dirname(output_file_path))
        pd.DataFrame(df_values, columns=columns).to_csv(output_file_path, index=False)
        logger.info(f"{output_file_path}: {len(self)}")

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
        logger.info(f"Loading artifacts: {data_file_path}")
        artifacts, artifact_type = GArtifactSet.__read_data_file(data_file_path)
        return GArtifactSet(artifacts, artifact_type)

    def get_entity_dict(self) -> Dict[str, T]:
        """
        :return: Returns mapping betwen entity ids and artifacts.
        """
        return {entity_id: entity for entity, entity_id in zip(self.artifacts, self.artifact_ids)}

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
            return [abstract_artifact_class.from_state_dict(row) for row in artifacts], artifact_type

    @staticmethod
    def __get_constructor_for_type(artifact_type: GArtifactType) -> Type[AbstractGithubArtifact]:
        """
        Returns the constructor of the artifact for given type.
        :param artifact_type: The type of artifact to create.
        :return: Class constructor for given type.
        """
        return SupportedGArtifacts.get_value(artifact_type)

    def __getitem__(self, item_index: int) -> T:
        """
        Returns artifact at given index.
        :param item_index: The index of the artifact to retrieve.
        :return: The artifact.
        """
        assert isinstance(item_index, int), f"Expected index to be int but got {type(item_index)}"
        return self.artifacts[item_index]

    def __iter__(self):
        """
        :return: Returns iterator to artifacts.
        """
        for artifact in self.artifacts:
            yield artifact

    def __add__(self, other):
        """
        Adds to artifact sets together if they contain the same type of entities.
        :param other: The other artifact set.
        :return: Artifact set containing combined articacts.
        """
        assert isinstance(other, GArtifactSet), f"Expected other to be GArtifactSet."
        assert self.artifact_type == other.artifact_type, f"Expected same artifact types {self.artifact_type} {other.artifact_type}."
        entity_dict: Dict[str, T] = self.get_entity_dict()
        entity_dict.update(other.get_entity_dict())
        artifacts = list(entity_dict.values())
        return GArtifactSet(artifacts, self.artifact_type)

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
