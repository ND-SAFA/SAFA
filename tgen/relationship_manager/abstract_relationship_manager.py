import logging
import math
import os
import uuid
from abc import abstractmethod
from copy import deepcopy
from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from common_resources.tools.constants.hugging_face_constants import DEFAULT_ENCODING_BATCH_SIZE
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.dict_util import DictUtil
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.reflection_util import ReflectionUtil
from common_resources.tools.util.str_util import StrUtil
from common_resources.tools.util.supported_enum import SupportedEnum
from common_resources.data.keys.structure_keys import ArtifactKeys
from tgen.models.model_properties import ModelTask
from tgen.relationship_manager.embedding_types import IdType
from tgen.relationship_manager.model_cache import ModelCache


class RelationshipManagerObjects(SupportedEnum):
    CONTENT_MAP = "content_map"
    RELATIONSHIP_MAP = "relationship_map"


class AbstractRelationshipManager:
    MODEL_MAP = {}

    def __init__(self, content_map: Dict[str, str] = None, model_name: str = None, model: SentenceTransformer = None,
                 show_progress_bar: bool = True, model_type: str = ModelTask.SENTENCE_TRANSFORMER.name):
        """
        Initializes the relationship manager with the content used to create relationships between artifacts
        :param content_map: Maps id to the corresponding content
        :param model_name: Name of model to use for predicting relationship
        :param model: The model to use to predict on artifacts.
        :param model_type: The type of model being used.
        :param show_progress_bar: Whether to show progress bar when calculating batches.
        """
        self.model_name = model_name
        self.show_progress_bar = show_progress_bar
        self._content_map = deepcopy(content_map) if content_map else {}
        self._relationship_map = {}
        self._model = model
        self.__state_changed_since_last_save = False
        self.model_type = model_type
        self._base_path = None

    @classmethod
    def create_from_content(cls, content_list: List[str], **kwargs) -> "AbstractRelationshipManager":
        """
        Creates manager by constructing a content map from a list of its content.
        :param content_list: List of content.
        :param kwargs: Keyword arguments passed to manager.
        :return: The Manager.
        """
        content_list = list(set(content_list))
        content_map = {c: c for c in content_list}
        manager = cls(content_map, **kwargs)
        return manager

    def get_all_ids(self) -> List[Any]:
        """
        Gets a list of all ids present in the context map
        :return: A list of all ids present in the context map
        """
        return list(self._content_map.keys())

    def get_content(self, a_id: Any) -> str:
        """
        Gets the content associated with a given id
        :param a_id: The id to get content for
        :return: The content
        """
        return self._content_map.get(a_id)

    def update_or_add_content(self, a_id: Any, content: str) -> bool:
        """
        Updates or adds new content for an id
        :param a_id: The id to update the content of
        :param content: The new content
        :return: True if artifact was updated else False.
        """
        updated_artifact = False
        if a_id in self._content_map and self._content_map[a_id] != content:
            self.__state_changed_since_last_save = True
            self.remove_artifact(a_id)
            updated_artifact = True
        self._content_map[a_id] = content
        return updated_artifact

    def update_or_add_contents(self, content_map: Dict[Any, str]) -> None:
        """
        Updates or adds new content for all artifacts in teh map
        :param content_map: Maps the id of the new or existing artifact to the its content
        :return: None
        """
        for a_id, content in content_map.items():
            self.update_or_add_content(a_id=a_id, content=content)

    def remove_artifact(self, a_id: IdType) -> None:
        """
        Removes an artifact with ids from the manager.
        :param a_id: ID of the artifact to remove.
        :return: None
        """
        if a_id in self._content_map:
            self._content_map.pop(a_id)
        if a_id in self._relationship_map:
            for other_id in self._relationship_map.keys():
                self.remove_relationship(a_id, other_id)
            self.__state_changed_since_last_save = True

    def remove_artifacts(self, a_ids: Union[IdType, List[IdType]]) -> None:
        """
        Removes artifacts with ids from the manager.
        :param a_ids: IDs of the artifact to remove.
        :return: None
        """
        if isinstance(a_ids, str):
            a_ids = [a_ids]
        for a_id in a_ids:
            self.remove_artifact(a_id)

    def get_model(self) -> SentenceTransformer:
        """
        Returns sentence transformer model.
        :return: The model.
        """
        if self._model is None:
            self._model = ModelCache.get_model(self.model_name, model_type=ModelTask[self.model_type].value)
        return self._model

    def add_relationship(self, id1: str, id2: str, relationship_score: Any) -> None:
        """
        Adds the relationship between two artifacts to the map.
        :param id1: Id for first artifact.
        :param id2: Id for second artifact.
        :param relationship_score: The score of the relationship between the artifacts.
        :return: None.
        """
        DictUtil.initialize_value_if_not_in_dict(self._relationship_map, id1, dict())
        DictUtil.initialize_value_if_not_in_dict(self._relationship_map, id2, dict())
        self._relationship_map[id1][id2] = relationship_score
        self._relationship_map[id2][id1] = relationship_score

    def remove_relationship(self, id1: str, id2: str) -> None:
        """
        Removes the relationship between two artifacts to the map.
        :param id1: Id for first artifact.
        :param id2: Id for second artifact.
        :return: None.
        """
        if self.relationship_exists(id1, id2):
            self._relationship_map[id1].pop(id2)
        if self.relationship_exists(id2, id1):
            self._relationship_map[id2].pop(id1)

    def merge(self, other: "RelationshipsManager") -> None:
        """
        Combines the relationships and contents maps of the two managers.
        :param other: The manager to merge with.
        :return: None.
        """
        self.update_or_add_contents(other._content_map)
        self._relationship_map.update(other._relationship_map)

    def compare_artifacts(self, ids1: List[str], ids2: List[str] = None, **kwargs) -> np.array:
        """
        Calculates the similarities between two sets of artifacts.
        :param ids1: List of ids to compare with ids2.
        :param ids2: List of ids to compare with ids1.
        :return: The scores between each artifact in ids1 with those in ids2.
        """
        if not ids2:
            ids2 = ids1
        similarity_matrix = self._compare_artifacts(ids1, ids2, **kwargs)
        for i, id1 in enumerate(ids1):
            for j, id2 in enumerate(ids2):
                score = similarity_matrix[i, j]
                self.add_relationship(id1, id2, score)
        return similarity_matrix

    def get_artifact_contents(self, artifact_ids: List[str], include_ids: bool = False) -> List[str]:
        """
        Gets the content if each artifact.
        :param artifact_ids: List of ids of artifacts to get content for.
        :param include_ids: If True, includes the id as part of the content.
        :return: A list of the content corresponding to each artifact.
        """
        artifact_contents = [self._content_map[a_id] for a_id in artifact_ids]
        if include_ids:
            artifact_contents = [f"{FileUtil.convert_path_to_human_readable(a_id)} {content}"
                                 # converts code file paths to NL
                                 for a_id, content in zip(artifact_ids, artifact_contents)]
        return artifact_contents

    def compare_artifact(self, id1: str, id2: str, **kwargs) -> float:
        """
        Compares the two artifacts.
        :param id1: Id for first artifact.
        :param id2: Id for second artifact.
        :return: The comparison score.
        """
        if not (self.relationship_exists(id1, id2)):
            relationship_score = self._compare_artifacts([id1], [id2], **kwargs)[0][0]
            self.add_relationship(id1, id2, relationship_score)
        return self.get_relationship(id1, id2)

    def get_relationship(self, id1, id2):
        """
        Gets the relationship score between artifact with id1 and artifact with id2.
        :param id1: The id of the first artifact in the relationship.
        :param id2: The id of the second artifact in the relationship.
        :return: The relationship score between artifact with id1 and artifact with id2.
        """
        return self._relationship_map[id1][id2]

    def relationship_exists(self, id1: str, id2: str) -> bool:
        """
        Checks whether a relationship is already saved between two artifacts.
        :param id1: The first artifact id.
        :param id2: The second artifact id.
        :return: True if the relationships is already saved, else False.
        """
        return id1 in self._relationship_map and id2 in self._relationship_map[id1]

    def to_yaml(self, export_path: str, replacement_vars: dict = None) -> "AbstractRelationshipManager":
        """
        Creates a yaml savable embedding manager by saving the embeddings to a separate file
        :param export_path: The path to export everything to
        :param replacement_vars: Maps variable name to the replacement value for its saved version.
        :return: The yaml savable embedding manager
        """
        replacement_vars = {} if not replacement_vars else replacement_vars
        yaml_manager = self.__class__(content_map=self._content_map, model_name=self.model_name)
        model_var = ReflectionUtil.extract_name_of_variable(f"{self._model=}", is_self_property=True,
                                                            class_attr=AbstractRelationshipManager)
        content_map_var = ReflectionUtil.extract_name_of_variable(f"{self._content_map=}", is_self_property=True,
                                                                  class_attr=AbstractRelationshipManager)
        relationship_map_var = ReflectionUtil.extract_name_of_variable(f"{self._relationship_map=}", is_self_property=True,
                                                                       class_attr=AbstractRelationshipManager)
        replacement_vars.update({model_var: None, content_map_var: {}, relationship_map_var: {}})
        yaml_manager.__dict__ = {k: (replacement_vars[k] if k in replacement_vars else v) for k, v in
                                 self.__dict__.items()}
        return yaml_manager

    def from_yaml(self) -> bool:
        """
        Loads any saved embeddings into the object after being reloaded from yaml
        :return: Whether it was loaded.
        """
        if self._base_path:
            object_paths = self.get_object_paths()

            self._content_map = self.load_content_map_from_file(object_paths[RelationshipManagerObjects.CONTENT_MAP])
            self._content_map = StrUtil.convert_all_items_to_string(self._content_map)

            self._relationship_map = self.load_content_map_from_file(object_paths[RelationshipManagerObjects.RELATIONSHIP_MAP])
            return True
        return False

    @staticmethod
    def save_content_to_csv(output_path: str, content: Union[Dict, List]) -> None:
        """
        Saves content map as CSV file at given path.
        :param output_path: The path to store the CSV file to.
        :param content: The map being stored.
        :return: None
        """
        df_kwargs = {}
        if len(content) == 0:
            entries = []
            df_kwargs["columns"] = [ArtifactKeys.ID.value, ArtifactKeys.CONTENT.value]
        elif isinstance(content, dict):
            entries = [EnumDict({ArtifactKeys.ID: content_id, ArtifactKeys.CONTENT: content}) for content_id, content in
                       content.items()]
        else:
            entries = content
            df_kwargs["columns"] = [ArtifactKeys.ID.value]
        pd.DataFrame(entries, **df_kwargs).to_csv(output_path, index=False)

    def save_to_file(self, dir_path: str) -> None:
        """
        Saves contents to file to reduce yaml size.
        :param dir_path: The path to directory to save to
        :return: None.
        """
        base_path = os.path.join(dir_path, str(uuid.uuid4()))
        FileUtil.create_dir_safely(base_path)
        self._base_path = FileUtil.collapse_paths(base_path)
        object_paths = self.get_object_paths()
        logger.info(f"Saving {self.__class__.__name__} state to: {base_path}")
        content_map_path = object_paths[RelationshipManagerObjects.CONTENT_MAP]
        self.save_content_to_csv(content_map_path, self._content_map)
        relationship_map_path = object_paths[RelationshipManagerObjects.RELATIONSHIP_MAP]
        self.save_content_to_csv(relationship_map_path, self._relationship_map)
        self.__state_changed_since_last_save = False

    def get_object_paths(self) -> Dict[RelationshipManagerObjects, str]:
        """
        :return: Returns map of embedding object to its path.
        """
        base_path = FileUtil.expand_paths(self._base_path)
        return {object_type: self.get_save_path(base_path, object_type) for object_type in RelationshipManagerObjects}

    @staticmethod
    def load_content_map_from_file(file_path: str) -> Dict[Any, str]:
        """
        Loads content map data frame into a dictionary.
        :param file_path: The path to find CSV at.
        :return: Map of artifact ID to its content.
        """
        try:
            content_df = pd.read_csv(file_path)
            if ArtifactKeys.CONTENT.value in content_df.columns:
                content_map = {content_row[ArtifactKeys.ID.value]: content_row[ArtifactKeys.CONTENT.value]
                               for _, content_row in content_df.iterrows()}
            else:
                content_map = list(content_df[ArtifactKeys.ID.value])
        except Exception:
            content_map = {}
        return content_map

    @staticmethod
    def get_save_path(base_path: str, object_type: RelationshipManagerObjects, ext: str = FileUtil.CSV_EXT) -> str:
        """
        Creates a unique path to save the embeddings to
        :param base_path: Path to the directory to save to
        :param object_type: The type of content to be saved. One of embeddings or content_map.
        :param ext: The extension of the file.
        :return: The path containing the filename to save to
        """
        object_name = object_type.name.lower()
        save_path = FileUtil.add_ext(os.path.join(base_path, f"{object_name}"), ext)
        return save_path

    def need_saved(self, export_path: str) -> bool:
        """
        Returns whether if the embeddings need re-saved
        :param export_path: The path to save the embeddings to
        :return: True if the embeddings need re-saved
        """
        need_save = not self._base_path or self.__state_changed_since_last_save
        return need_save and len(self._content_map) > 0

    def _determine_show_progress_bar(self, artifact_contents: List[str], log_message: str,
                                     batch_size: int = DEFAULT_ENCODING_BATCH_SIZE) -> bool:
        """
        Determines if a progress bar should be shown.
        :param artifact_contents: The list of artifact content used to determine if the number of artifacts warrants a progress bar.
        :param log_message: The message to log in place of a progress bar if the bar should not be shown.
        :param batch_size: The size of the batch being used.
        :return: True if a progress bar should be shown else False.
        """
        show_progress_bar = self.show_progress_bar and math.ceil(len(artifact_contents) / batch_size) > 1
        if not show_progress_bar:
            logger.log_without_spam(msg=log_message, level=logging.INFO)
        return show_progress_bar

    def _get_default_artifact_ids(self, artifact_ids: List[str] = None):
        """
        Returns the artifact ids if not None otherwise return list of all artifact ids.
        :param artifact_ids: Inputted artifact ids to evaluate.
        :return: The artifact ids.
        """
        return artifact_ids if artifact_ids is not None else self._content_map.keys()

    @abstractmethod
    def _compare_artifacts(self, ids1: List[str], ids2: List[str], **kwargs) -> np.array:
        """
        Calculates the similarities between two sets of artifacts.
        :param ids1: List of ids to compare with ids2.
        :param ids2: List of ids to compare with ids1.
        :return: The scores between each artifact in ids1 with those in ids2 in a similarity matrix.
        """

    def __contains__(self, item: str) -> bool:
        """
        Returns True if the item is in the content map, else False.
        :param item: The artifact id to check if it is in the content map.
        :return: True if the item is in the content map, else False.
        """
        return item in self._content_map
