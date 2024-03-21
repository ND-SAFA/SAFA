from abc import abstractmethod
from copy import deepcopy

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Any, Dict, List, Union

from tgen.common.util.dict_util import DictUtil
from tgen.relationship_manager.embedding_types import IdType
from tgen.relationship_manager.model_cache import ModelCache


class AbstractRelationshipManager:
    MODEL_MAP = {}

    def __init__(self, content_map: Dict[str, str], model_name: str = None, model: SentenceTransformer = None,
                 show_progress_bar: bool = True):
        """
        Initializes the relationship manager with the content used to create relationships between artifacts
        :param content_map: Maps id to the corresponding content
        :param model_name: Name of model to use for predicting relationship
        :param model: The model to use to predict on artifacts.
        :param show_progress_bar: Whether to show progress bar when calculating batches.
        """
        self.model_name = model_name
        self.show_progress_bar = show_progress_bar
        self._content_map = deepcopy(content_map)
        self._relationship_map = {}
        self._model = model
        self.__state_changed_since_last_save = False

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
            self._model = ModelCache.get_model(self.model_name)
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
