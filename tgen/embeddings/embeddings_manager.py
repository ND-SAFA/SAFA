import os
from typing import Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer

from tgen.common.constants.environment_constants import IS_TEST

EmbeddingType = np.array


class EmbeddingsManager:
    @staticmethod
    def create_artifact_embeddings(artifact_map: Dict[str, str], model: SentenceTransformer, artifact_ids: List[str] = None) -> \
            List[EmbeddingType]:
        """
        Creates list of embeddings for each artifact.
        :param artifact_map: Map of artifact ids to content.
        :param model: The model to use to embed artifact content.
        :param artifact_ids: The artifact ids to embed.
        :return: List of embeddings in same order as artifact ids.
        """
        artifact_ids_set = set(artifact_ids)
        subset_content_map = {k: v for k, v in artifact_map.items() if k in artifact_ids_set}
        embedding_map = EmbeddingsManager.create_embedding_map(subset_content_map, model)
        embeddings = [embedding_map[entry_id] for entry_id in artifact_ids]
        return embeddings

    @staticmethod
    def create_embedding_map(content_map: Dict[str, str], model: SentenceTransformer, subset_ids: List[str] = None) -> \
            Dict[str, EmbeddingType]:
        """
        Creates embeddings for entries in map.
        :param content_map: The entries in the map to embed.
        :param model: The model to use to embed the entries.
        :param subset_ids: The IDs of the set of the entries to use.
        :return: Map of id to embedding.
        """
        if subset_ids is None:
            subset_ids = content_map.keys()
        embedding_map = {a_id: model.encode(content_map[a_id]) for a_id in subset_ids}
        return embedding_map

    @staticmethod
    def get_model(model_name: str) -> SentenceTransformer:
        """
        Returns sentence transformer model.
        :param model_name: The name of the model to load.
        :return: The model.
        """
        cache_dir = EmbeddingsManager.get_cache_dir()
        return SentenceTransformer(model_name, cache_folder=cache_dir)

    @staticmethod
    def get_cache_dir() -> str:
        """
        :return: Returns path to cache directory for the models.
        """
        cache_dir = os.environ.get("HF_DATASETS_CACHE", None)
        if cache_dir is None or IS_TEST or not os.path.exists(cache_dir):
            cache_dir = None
        return cache_dir
