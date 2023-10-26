import os
import uuid
from typing import Any, Dict, List, Optional, Union

import numpy as np
from sentence_transformers import SentenceTransformer

from tgen.common.constants.environment_constants import IS_TEST
from tgen.common.util.file_util import FileUtil
from tgen.common.util.reflection_util import ReflectionUtil

EmbeddingType = np.array


class EmbeddingsManager:

    def __init__(self, content_map: Dict[str, str], model_name: str):
        """
        Initializes the embedding manager with the content used to create embeddings
        :param content_map: Maps id to the corresponding content
        :param model_name: Name of model to use for creating embeddings
        """
        self.model_name = model_name
        self._content_map = content_map
        self._embedding_map = {}
        self.__ordered_ids = []
        self.__saved_embeddings_path = None
        self.__model = None
        self.__state_changed_since_last_save = False

    def create_artifact_embeddings(self, artifact_ids: List[str] = None, **kwargs) -> List[EmbeddingType]:
        """
        Creates list of embeddings for each artifact.
        :param artifact_ids: The artifact ids to embed.
        :return: List of embeddings in same order as artifact ids.
        """
        embedding_map = self.create_embedding_map(subset_ids=artifact_ids, **kwargs)
        embeddings = [embedding_map[entry_id] for entry_id in artifact_ids]
        return embeddings

    def create_embedding_map(self, subset_ids: List[str] = None, **kwargs) -> Dict[str, EmbeddingType]:
        """
        Creates embeddings for entries in map.
        :param subset_ids: The IDs of the set of the entries to use.
        :return: Map of id to embedding.
        """
        if subset_ids is None:
            subset_ids = self._content_map.keys()
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

    def update_or_add_content(self, a_id: Any, content: str, create_embedding: bool = False) -> Optional[EmbeddingType]:
        """
        Updates or adds new content for an id
        :param a_id: The id to update the content of
        :param content: The new content
        :param create_embedding: If True, automatically creates a new embedding
        :return: The embedding if one was created, else None
        """
        self._content_map[a_id] = content
        if a_id in self._embedding_map:
            self.__state_changed_since_last_save = True
            self._embedding_map.pop(a_id)
        if create_embedding:
            return self.get_embedding(a_id)

    def update_or_add_contents(self, content_map: Dict[Any, str], create_embedding: bool = False) -> Optional[
        EmbeddingType]:
        """
        Updates or adds new content for all artifacts in teh map
        :param content_map: Maps the id of the new or existing artifact to the its content
        :param create_embedding: If True, automatically creates a new embedding
        :return: The embeddings if created, else None
        """
        for a_id, content in content_map.items():
            if a_id not in self._content_map or self._content_map[a_id] != content:
                self.update_or_add_content(a_id=a_id, content=content, create_embedding=False)
        if create_embedding:
            return self.create_embedding_map(list(content_map.keys()))

    def remove_from_content_map(self, a_id: Any) -> None:
        """
        Removes existing id and content from map
        :param a_id: The id to remove
        :return: None
        """
        if a_id in self._content_map:
            self._content_map.pop(a_id)
        if a_id in self._embedding_map:
            self._embedding_map.pop(a_id)
            self.__state_changed_since_last_save = a_id in self.__ordered_ids

    def get_model(self) -> SentenceTransformer:
        """
        Returns sentence transformer model.
        :return: The model.
        """
        if self.__model is None:
            cache_dir = EmbeddingsManager.get_cache_dir()
            self.__model = SentenceTransformer(self.model_name, cache_folder=cache_dir)
        return self.__model

    @staticmethod
    def get_cache_dir() -> str:
        """
        :return: Returns path to cache directory for the models.
        """
        cache_dir = os.environ.get("HF_DATASETS_CACHE", None)
        if cache_dir is None or IS_TEST or not os.path.exists(cache_dir):
            cache_dir = None
        return cache_dir

    def to_yaml(self, export_path: str) -> "EmbeddingsManager":
        """
        Creates a yaml savable embedding manager by saving the embeddings to a separate file
        :param export_path: The path to export everything to
        :return: The yaml savable embedding manager
        """
        yaml_embeddings_manager = EmbeddingsManager(content_map=self._content_map, model_name=self.model_name)
        if self.embeddings_need_saved(export_path):
            self.save_embeddings_to_file(export_path)
        embedding_map_var = ReflectionUtil.extract_name_of_variable(f"{self._embedding_map=}", is_self_property=True)
        model_var = ReflectionUtil.extract_name_of_variable(f"{self.__model=}", is_self_property=True,
                                                            class_attr=EmbeddingsManager)
        replacements = {embedding_map_var: {}, model_var: None}
        yaml_embeddings_manager.__dict__ = {k: (replacements[k] if k in replacements else v) for k, v in
                                            self.__dict__.items()}
        return yaml_embeddings_manager

    def from_yaml(self) -> None:
        """
        Loads any saved embeddings into the object after being reloaded from yaml
        :return: None
        """
        if self.__saved_embeddings_path and self.__ordered_ids:
            file_path = FileUtil.expand_paths(self.__saved_embeddings_path)
            self._embedding_map = self.load_embeddings_from_file(file_path=file_path,
                                                                 ordered_ids=self.__ordered_ids)

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

    def save_embeddings_to_file(self, dir_path: str) -> None:
        """
        Stores the current embeddings to a file
        :param dir_path: The path to directory to save to
        :return: None
        """
        file_path = self.get_save_path(dir_path)
        FileUtil.save_numpy(list(self._embedding_map.values()), file_path)
        self.__set_embedding_order()
        self.__saved_embeddings_path = FileUtil.collapse_paths(file_path)
        self.__state_changed_since_last_save = False

    @staticmethod
    def get_save_path(dir_path: str) -> str:
        """
        Creates a unique path to save the embeddings to
        :param dir_path: Path to the directory to save to
        :return: The path containing the filename to save to
        """
        return FileUtil.add_ext(os.path.join(dir_path, f"embeddings_{uuid.uuid4()}"), FileUtil.NUMPY_EXT)

    def embeddings_need_saved(self, export_path: str) -> bool:
        """
        Returns whether if the embeddings need re-saved
        :param export_path: The path to save the embeddings to
        :return: True if the embeddings need re-saved
        """
        return not self.__saved_embeddings_path or self.__state_changed_since_last_save \
            or FileUtil.collapse_paths(export_path) != FileUtil.get_directory_path(self.__saved_embeddings_path)

    def calculate_centroid(self, cluster: List[str]):
        """
        Calculates the embedding pointing at the center of the cluster.
        :param cluster: The artifacts whose embeddings are used to calculate the centroid.
        :param embedding_manager: Contains the artifacts embeddings.
        :return: Embedding pointing at center of cluster.
        """
        if len(cluster) == 0:
            raise Exception("Cannot calculate center of empty cluster.")
        embeddings = [self.get_embedding(a_id) for a_id in cluster]
        centroid = np.sum(embeddings, axis=0) / len(cluster)
        return centroid

    def __encode(self, subset_ids: Union[List[Any], Any], include_ids: bool = False, **kwargs):
        return_as_list = True
        if not isinstance(subset_ids, list):
            subset_ids = [subset_ids]
            return_as_list = False
        artifact_contents = [self._content_map[a_id] for a_id in subset_ids]
        if include_ids:
            artifact_contents = [f"{a_id}: {content}" for a_id, content in zip(subset_ids, artifact_contents)]
        embeddings = self.get_model().encode(artifact_contents, show_progress_bar=True)
        return embeddings if return_as_list else embeddings[0]

    def __set_embedding_order(self) -> None:
        """
        Stores the current order of the embeddings as a list of ids in the same order as their saved embeddings
        :return: None
        """
        self.__ordered_ids = list(self._embedding_map.keys())
