from typing import Any, Dict, List, Union

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from gen_common.constants import DEFAULT_EMBEDDING_MODEL, DEFAULT_ENCODING_BATCH_SIZE, EMPTY_STRING
from gen_common.traceability.relationship_manager.abstract_relationship_manager import AbstractRelationshipManager
from gen_common.traceability.relationship_manager.embedding_types import EmbeddingType, IdType
from gen_common.util import EnumDict, FileUtil, StrUtil
from gen_common.util.override import overrides
from gen_common.util.reflection_util import ReflectionUtil
from gen_common.util.supported_enum import SupportedEnum


class EmbeddingsManagerObjects(SupportedEnum):
    EMBEDDINGS = "embeddings"
    ORDERED_IDS = "ordered_ids"


class EmbeddingsManager(AbstractRelationshipManager):
    MODEL_MAP = {}

    def __init__(self, content_map: Dict[str, str] = None, model_name: str = DEFAULT_EMBEDDING_MODEL,
                 model: SentenceTransformer = None,
                 show_progress_bar: bool = True, create_embeddings_on_init: bool = False, as_tensors: bool = False):
        """
        Initializes the embedding manager with the content used to create embeddings
        :param content_map: Maps id to the corresponding content
        :param model_name: Name of model to use for creating embeddings
        :param model: The model to use to embed artifacts.
        :param show_progress_bar: Whether to show progress bar when calculating batches.
        :param create_embeddings_on_init: If True, creates embeddings for all items in the content map.
        :param as_tensors: Converts embeddings to tensors.
        """
        self._embedding_map = {}
        self.__ordered_ids = []
        self._as_tensors = as_tensors
        super().__init__(model_name=model_name, show_progress_bar=show_progress_bar, content_map=content_map, model=model)

        if create_embeddings_on_init:
            self.create_embeddings()

    def create_embeddings(self, artifact_ids: List[str] = None, **kwargs) -> List[EmbeddingType]:
        """
        Creates list of embeddings for each artifact.
        :param artifact_ids: The artifact ids to embed.
        :return: List of embeddings in same order as artifact ids.
        """
        subset_ids = list(self._content_map.keys()) if not artifact_ids else artifact_ids
        embedding_map = self.create_embedding_map(subset_ids=subset_ids, **kwargs)
        embeddings = [embedding_map[entry_id] for entry_id in subset_ids]
        return embeddings

    def create_embedding_map(self, subset_ids: List[str] = None, **kwargs) -> Dict[str, EmbeddingType]:
        """
        Creates embeddings for entries in map.
        :param subset_ids: The IDs of the set of the entries to use.
        :return: Map of id to embedding.
        """
        subset_ids = self._get_default_artifact_ids(subset_ids)
        artifact_embeddings = self.get_embeddings(subset_ids, **kwargs)
        embedding_map = {a_id: a_embedding for a_id, a_embedding in zip(subset_ids, artifact_embeddings)}

        return embedding_map

    def get_embeddings(self, a_ids: List[Any], **kwargs) -> List[EmbeddingType]:
        """
        Gets embeddings for list of artifact ids, creates embeddings if they do not exist yet.
        :param a_ids: Artifact ids whose embeddings are returned.
        :return: Artifact embeddings, returned in the same order as ids.
        """
        ids_without_embeddings = [a_id for a_id in a_ids if a_id not in self._embedding_map]
        if len(ids_without_embeddings) > 0:
            artifact_embeddings = self.__encode(ids_without_embeddings, **kwargs)
            new_embedding_map = {a_id: embedding for a_id, embedding in
                                 zip(ids_without_embeddings, artifact_embeddings)}
            self._embedding_map.update(new_embedding_map)
            self.__state_changed_since_last_save = True
        return [self.get_embedding(a_id) for a_id in a_ids]

    def get_embedding(self, a_id: Any, **kwargs) -> EmbeddingType:
        """
        Gets an embedding for a given id
        :param a_id: The id to get an embedding for (corresponding to the ids in the content map)
        :return: The embedding for the content corresponding to the a_id
        """
        if a_id not in self._embedding_map:
            self.__state_changed_since_last_save = True
            self._embedding_map[a_id] = self.__encode(a_id, **kwargs)
        return self._embedding_map[a_id]

    def get_current_embeddings(self) -> Dict[Any, EmbeddingType]:
        """
        Gets all embeddings currently created
        :return: A dictionary mapping id to the embedding created for all embeddings currently created
        """
        return self._embedding_map

    @overrides(AbstractRelationshipManager)
    def update_or_add_content(self, a_id: Any = None, content: str = None, artifact: EnumDict = None) -> bool:
        """
        Updates or adds new content for an id
        :param a_id: The id to update the content of
        :param content: The new content
        :param artifact: Artifact may be specified in place of id and content.
        :return: None
        """
        updated_artifact = super().update_or_add_content(a_id, content)
        if a_id in self._embedding_map and updated_artifact:
            self.__state_changed_since_last_save = True
            self._embedding_map.pop(a_id)
        return updated_artifact

    @overrides(AbstractRelationshipManager)
    def remove_artifact(self, a_id: IdType) -> bool:
        """
        Removes an artifact with ids from the manager.
        :param a_id: ID of the artifact to remove.
        :return: None
        """
        removed = super().remove_artifact(a_id)
        if a_id in self._embedding_map:
            self._embedding_map.pop(a_id)
            self.__state_changed_since_last_save = True
        return removed

    @overrides(AbstractRelationshipManager)
    def to_yaml(self, export_path: str, **kwargs) -> "EmbeddingsManager":
        """
        Creates a yaml savable embedding manager by saving the embeddings to a separate file
        :param export_path: The path to export everything to
        :return: The yaml savable embedding manager
        """
        if self.need_saved(export_path):
            self.save_to_file(export_path)
        embedding_map_var = ReflectionUtil.extract_name_of_variable(f"{self._embedding_map=}", is_self_property=True)

        ordered_ids_var = ReflectionUtil.extract_name_of_variable(f"{self.__ordered_ids=}", is_self_property=True,
                                                                  class_attr=AbstractRelationshipManager)
        replacements = {embedding_map_var: {}, ordered_ids_var: []}
        return super().to_yaml(export_path, replacement_vars=replacements)

    @overrides(AbstractRelationshipManager)
    def from_yaml(self) -> bool:
        """
        Loads any saved embeddings into the object after being reloaded from yaml
        :return: Whether it loaded.
        """
        if super().from_yaml():
            object_paths = self.get_embeddings_paths()
            ordered_ids = self.load_content_map_from_file(object_paths[EmbeddingsManagerObjects.ORDERED_IDS])
            self.__set_embedding_order(StrUtil.convert_all_items_to_string(ordered_ids))
            self._embedding_map = self.load_embeddings_from_file(file_path=object_paths[EmbeddingsManagerObjects.EMBEDDINGS],
                                                                 ordered_ids=self.__ordered_ids)
            self._embedding_map = StrUtil.convert_all_items_to_string(self._embedding_map, keys_only=True)
            return True
        return False

    @staticmethod
    def load_embeddings_from_file(file_path: str, ordered_ids: List[Any]) -> Dict[Any, EmbeddingType]:
        """
        Loads embeddings from a file
        :param file_path: The file to load from
        :param ordered_ids: Optional ordering of the ids corresponding to the order of embeddings in the file
        :return: A dictionary mapping id to the loaded embeddings
        """
        embeddings = FileUtil.load_numpy(file_path)
        assert len(ordered_ids) == len(
            embeddings), "The ordered ids must correspond to the embeddings but they are different lengths."
        return {a_id: embedding for a_id, embedding in zip(ordered_ids, embeddings)}

    @overrides(AbstractRelationshipManager)
    def save_to_file(self, dir_path: str) -> None:
        """
        Stores the current embeddings to a file
        :param dir_path: The path to directory to save to
        :return: None
        """
        super().save_to_file(dir_path)

        object_paths = self.get_embeddings_paths()
        ordered_ids_path = object_paths[EmbeddingsManagerObjects.ORDERED_IDS]
        embedding_map_path = object_paths[EmbeddingsManagerObjects.EMBEDDINGS]

        self.__set_embedding_order()
        self.save_content_to_csv(ordered_ids_path, self.__ordered_ids)
        FileUtil.save_numpy(list(self._embedding_map.values()), embedding_map_path)

    def get_embeddings_paths(self) -> Dict[EmbeddingsManagerObjects, str]:
        """
        :return: Returns map of embedding object to its path.
        """
        base_path = FileUtil.expand_paths(self._base_path)
        return {object_type: self.get_save_path(base_path, object_type,
                                                ext=FileUtil.NUMPY_EXT if object_type == EmbeddingsManagerObjects.EMBEDDINGS
                                                else FileUtil.CSV_EXT)
                for object_type in EmbeddingsManagerObjects}

    def calculate_centroid(self, cluster: List[str], key_to_add_to_map: str = None):
        """
        Calculates the embedding pointing at the center of the cluster.
        :param cluster: The artifacts whose embeddings are used to calculate the centroid.
        :param key_to_add_to_map: If provided, adds the centroid to the embedding and cluster map.
        :return: Embedding pointing at center of cluster.
        """
        if len(cluster) == 0:
            raise Exception("Cannot calculate center of empty cluster.")
        embeddings = [self.get_embedding(a_id) for a_id in cluster]
        centroid = np.sum(embeddings, axis=0) / len(cluster)
        if key_to_add_to_map:
            self._content_map[key_to_add_to_map] = EMPTY_STRING
            self._embedding_map[key_to_add_to_map] = centroid
        return centroid

    @overrides(AbstractRelationshipManager)
    def merge(self, other: "EmbeddingsManager") -> None:
        """
        Combines the embeddings and contents maps of the two embedding managers.
        :param other: The embedding manager to merge with.
        :return: None.
        """
        super().merge(other)
        self._embedding_map.update(other._embedding_map)

    def _compare_artifacts(self, ids1: List[str], ids2: List[str], **kwargs) -> float:
        """
        Calculates the similarities between two sets of artifacts.
        :param ids1: List of ids to compare with ids2.
        :param ids2: List of ids to compare with ids1.
        :return: The scores between each artifact in ids1 with those in ids2.
        """
        source_embeddings = self.get_embeddings(ids1, **kwargs)
        target_embeddings = self.get_embeddings(ids2, **kwargs)
        source_matrix = np.asarray(source_embeddings)
        target_matrix = np.asarray(target_embeddings)
        if source_matrix.shape[0] == 0:
            raise Exception("Source matrix has no examples.")
        if target_matrix.shape[0] == 0:
            raise Exception("Target matrix has no examples.")
        cluster_similarities = cosine_similarity(source_matrix, target_matrix)
        return cluster_similarities

    def __encode(self, subset_ids: Union[List[Any], Any], include_ids: bool = False, **kwargs) -> List:
        """
        Encodes the artifacts corresponding to the ids in the list
        :param subset_ids: The subset of artifacts to create embeddings for
        :param include_ids: If True, includes the id in the embedding
        :param kwargs: Not used
        :return: The embedding(s)
        """
        return_as_list = True
        if not isinstance(subset_ids, list):
            subset_ids = [subset_ids]
            return_as_list = False
        batch_size = DEFAULT_ENCODING_BATCH_SIZE
        artifact_contents = self.get_artifact_contents(subset_ids, include_ids)
        show_progress_bar = self._determine_show_progress_bar(artifact_contents, "Calculating embeddings for artifacts...", batch_size)
        embeddings = self.get_model().encode(artifact_contents, batch_size=batch_size,
                                             show_progress_bar=show_progress_bar, convert_to_tensor=self._as_tensors)
        return embeddings if return_as_list else embeddings[0]

    def __set_embedding_order(self, ordered_ids: List[Any] = None) -> None:
        """
        Stores the current order of the embeddings as a list of ids in the same order as their saved embeddings
        :param ordered_ids: If provided, saves the order to match, other it is based on this order
        :return: None
        """
        ordered_ids = list(self._embedding_map.keys()) if not ordered_ids else ordered_ids
        self.__ordered_ids = ordered_ids
