import logging
import math
import os
import uuid
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from tgen.common.constants.hugging_face_constants import DEFAULT_ENCODING_BATCH_SIZE
from tgen.common.logging.logger_manager import logger
from tgen.common.util.embedding_util import EmbeddingType, EmbeddingUtil, IdType
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.common.util.str_util import StrUtil
from tgen.common.util.supported_enum import SupportedEnum
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.embeddings.model_cache import ModelCache


class EmbeddingsManagerObjects(SupportedEnum):
    EMBEDDINGS = "embeddings"
    CONTENT_MAP = "content_map"
    ORDERED_IDS = "ordered_ids"


class EmbeddingsManager:
    MODEL_MAP = {}

    def __init__(self, content_map: Dict[str, str], model_name: str = None, model: SentenceTransformer = None,
                 show_progress_bar: bool = True):
        """
        Initializes the embedding manager with the content used to create embeddings
        :param content_map: Maps id to the corresponding content
        :param model_name: Name of model to use for creating embeddings
        :param model: The model to use to embed artifacts.
        :param show_progress_bar: Whether to show progress bar when calculating batches.
        """
        assert model_name is not None or model is not None, f"Expected model or model name to be defined but got None for both."
        self.model_name = model_name
        self.show_progress_bar = show_progress_bar
        self._content_map = content_map
        self._embedding_map = {}
        self.__ordered_ids = []
        self._base_path = None
        self.__model = model
        self.__state_changed_since_last_save = False

    @staticmethod
    def create_from_content(content_list: List[str], **kwargs) -> "EmbeddingsManager":
        """
        Creates embeddings manager mapping content in list to its embeddings.
        :param content_list: The content list to create embeddings for.
        :param kwargs: Keyword arguments passed to embeddings manager.
        :return: EmbeddingsManager.
        """
        content_list = list(set(content_list))
        content_map = {c: c for c in content_list}
        embeddings_manager = EmbeddingsManager(content_map, **kwargs)
        embeddings_manager.create_artifact_embeddings()
        return embeddings_manager

    def create_artifact_embeddings(self, artifact_ids: List[str] = None, **kwargs) -> List[EmbeddingType]:
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

    def remove_artifacts(self, a_ids: Union[IdType, List[IdType]]) -> None:
        """
        Removes artifacts with ids from embeddings manager.
        :param a_ids: IDs of the artifact to remove.
        :return: None
        """
        if isinstance(a_ids, str):
            a_ids = [a_ids]
        for a_id in a_ids:
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
            self.__model = ModelCache.get_model(self.model_name)
        return self.__model

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
        content_map_var = ReflectionUtil.extract_name_of_variable(f"{self._content_map=}", is_self_property=True,
                                                                  class_attr=EmbeddingsManager)
        ordered_ids_var = ReflectionUtil.extract_name_of_variable(f"{self.__ordered_ids=}", is_self_property=True,
                                                                  class_attr=EmbeddingsManager)
        replacements = {embedding_map_var: {}, model_var: None, content_map_var: {}, ordered_ids_var: []}
        yaml_embeddings_manager.__dict__ = {k: (replacements[k] if k in replacements else v) for k, v in
                                            self.__dict__.items()}
        return yaml_embeddings_manager

    def from_yaml(self) -> None:
        """
        Loads any saved embeddings into the object after being reloaded from yaml
        :return: None
        """
        if self._base_path:
            object_paths = self.get_object_paths()
            ordered_ids = self.load_content_map_from_file(object_paths[EmbeddingsManagerObjects.ORDERED_IDS])
            self.__set_embedding_order(StrUtil.convert_all_items_to_string(ordered_ids))
            self._embedding_map = self.load_embeddings_from_file(file_path=object_paths[EmbeddingsManagerObjects.EMBEDDINGS],
                                                                 ordered_ids=self.__ordered_ids)
            self._embedding_map = StrUtil.convert_all_items_to_string(self._embedding_map, keys_only=True)
            self._content_map = self.load_content_map_from_file(object_paths[EmbeddingsManagerObjects.CONTENT_MAP])
            self._content_map = StrUtil.convert_all_items_to_string(self._content_map)

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

    @staticmethod
    def load_content_map_from_file(file_path: str) -> Dict[Any, str]:
        """
        Loads content map data frame into a dictionary.
        :param file_path: The path to find CSV at.
        :return: Map of artifact ID to its content.
        """
        content_df = pd.read_csv(file_path)
        if ArtifactKeys.CONTENT.value in content_df.columns:
            content_map = {content_row[ArtifactKeys.ID.value]: content_row[ArtifactKeys.CONTENT.value]
                           for _, content_row in content_df.iterrows()}
        else:
            content_map = list(content_df[ArtifactKeys.ID.value])
        return content_map

    def save_embeddings_to_file(self, dir_path: str) -> None:
        """
        Stores the current embeddings to a file
        :param dir_path: The path to directory to save to
        :return: None
        """

        base_path = os.path.join(dir_path, str(uuid.uuid4()))
        FileUtil.create_dir_safely(base_path)
        self._base_path = FileUtil.collapse_paths(base_path)
        object_paths = self.get_object_paths()
        logger.info(f"Saving embedding manager state to: {base_path}")

        ordered_ids_path = object_paths[EmbeddingsManagerObjects.ORDERED_IDS]
        content_map_path = object_paths[EmbeddingsManagerObjects.CONTENT_MAP]
        embedding_map_path = object_paths[EmbeddingsManagerObjects.EMBEDDINGS]

        self.__set_embedding_order()
        self.save_content_to_csv(ordered_ids_path, self.__ordered_ids)
        self.save_content_to_csv(content_map_path, self._content_map)
        FileUtil.save_numpy(list(self._embedding_map.values()), embedding_map_path)

        self.__state_changed_since_last_save = False

    def get_object_paths(self) -> Dict[EmbeddingsManagerObjects, str]:
        """
        :return: Returns map of embedding object to its path.
        """
        base_path = FileUtil.expand_paths(self._base_path)
        return {object_type: self.get_save_path(base_path, object_type) for object_type in EmbeddingsManagerObjects}

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
            return

        if isinstance(content, dict):
            entries = [EnumDict({ArtifactKeys.ID: content_id, ArtifactKeys.CONTENT: content}) for content_id, content in
                       content.items()]
        else:
            entries = content
            df_kwargs["columns"] = [ArtifactKeys.ID.value]
        pd.DataFrame(entries, **df_kwargs).to_csv(output_path, index=False)

    @staticmethod
    def get_save_path(base_path: str, object_type: EmbeddingsManagerObjects) -> str:
        """
        Creates a unique path to save the embeddings to
        :param base_path: Path to the directory to save to
        :param object_type: The type of content to be saved. One of embeddings or content_map.
        :return: The path containing the filename to save to
        """
        ext = FileUtil.NUMPY_EXT if object_type == EmbeddingsManagerObjects.EMBEDDINGS else FileUtil.CSV_EXT
        object_name = object_type.name.lower()
        save_path = FileUtil.add_ext(os.path.join(base_path, f"{object_name}"), ext)
        return save_path

    def embeddings_need_saved(self, export_path: str) -> bool:
        """
        Returns whether if the embeddings need re-saved
        :param export_path: The path to save the embeddings to
        :return: True if the embeddings need re-saved
        """
        need_save = not self._base_path or self.__state_changed_since_last_save
        return need_save

    def compare_embeddings(self, id1: str, id2: str) -> float:
        """
        Calculates the similarities between two embeddings.
        :param id1: Id for first embedding.
        :param id2: Id for second embedding.
        :return: The similarity.
        """
        score = EmbeddingUtil.calculate_similarities([self.get_embedding(id1)], [self.get_embedding(id2)])[0][0]
        return score

    def calculate_centroid(self, cluster: List[str]):
        """
        Calculates the embedding pointing at the center of the cluster.
        :param cluster: The artifacts whose embeddings are used to calculate the centroid.
        :return: Embedding pointing at center of cluster.
        """
        if len(cluster) == 0:
            raise Exception("Cannot calculate center of empty cluster.")
        embeddings = [self.get_embedding(a_id) for a_id in cluster]
        centroid = np.sum(embeddings, axis=0) / len(cluster)
        return centroid

    def merge(self, other: "EmbeddingsManager") -> None:
        """
        Combines the embeddings and contents maps of the two embedding managers.
        :param other: The embedding manager to merge with.
        :return: None.
        """
        self.update_or_add_contents(other._content_map, create_embedding=False)
        self._embedding_map.update(other._embedding_map)

    def _get_default_artifact_ids(self, artifact_ids: List[str] = None):
        """
        Returns the artifact ids if not None otherwise return list of all artifact ids.
        :param artifact_ids: Inputted artifact ids to evaluate.
        :return: The artifact ids.
        """
        return artifact_ids if artifact_ids is not None else self._content_map.keys()

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
        artifact_contents = [self._content_map[a_id] for a_id in subset_ids]
        if include_ids:
            artifact_contents = [f"{FileUtil.convert_path_to_human_readable(a_id)} {content}"
                                 # converts code file paths to NL
                                 for a_id, content in zip(subset_ids, artifact_contents)]
        show_progress_bar = self.show_progress_bar and math.ceil(len(artifact_contents) / DEFAULT_ENCODING_BATCH_SIZE) > 1
        if not show_progress_bar:
            logger.log_without_spam(msg="Calculating embeddings for artifacts...", level=logging.INFO)
        embeddings = self.get_model().encode(artifact_contents, batch_size=DEFAULT_ENCODING_BATCH_SIZE,
                                             show_progress_bar=show_progress_bar)
        return embeddings if return_as_list else embeddings[0]

    def __set_embedding_order(self, ordered_ids: List[Any] = None) -> None:
        """
        Stores the current order of the embeddings as a list of ids in the same order as their saved embeddings
        :param ordered_ids: If provided, saves the order to match, other it is based on this order
        :return: None
        """
        ordered_ids = list(self._embedding_map.keys()) if not ordered_ids else ordered_ids
        self.__ordered_ids = ordered_ids

    def __contains__(self, item: str) -> bool:
        """
        Returns True if the item is in the content map, else False.
        :param item: The artifact id to check if it is in the content map.
        :return: True if the item is in the content map, else False.
        """
        return item in self._content_map
