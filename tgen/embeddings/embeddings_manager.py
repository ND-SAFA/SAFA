import os
from typing import Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer

from tgen.common.constants.environment_constants import IS_TEST

EmbeddingType = np.array


class EmbeddingsManager:
    model_map = {}

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
        embedding_map = EmbeddingsManager.create_embedding_map(artifact_map, model, artifact_ids)
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
        contents = [content_map[c_id] for c_id in subset_ids]
        embeddings = model.encode(contents)
        embedding_map = {a_id: embedding for a_id, embedding in zip(subset_ids, embeddings)}
        return embedding_map

    @staticmethod
    def get_model(model_name: str) -> SentenceTransformer:
        """
        Returns sentence transformer model.
        :param model_name: The name of the model to load.
        :return: The model.
        """
        cache_dir = EmbeddingsManager.get_cache_dir()
        if model_name not in EmbeddingsManager.model_map:
            EmbeddingsManager.model_map[model_name] = SentenceTransformer(model_name, cache_folder=cache_dir)
        model = EmbeddingsManager.model_map[model_name]
        return model

    @staticmethod
    def get_cache_dir() -> str:
        """
        :return: Returns path to cache directory for the models.
        """
        cache_dir = os.environ.get("HF_DATASETS_CACHE", None)
        if cache_dir is None or IS_TEST or not os.path.exists(cache_dir):
            cache_dir = None
        return cache_dir
