import os
from typing import Dict, List

import numpy as np
from sentence_transformers.SentenceTransformer import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing._data import minmax_scale
from tqdm import tqdm

from tgen.common.constants.environment_constants import IS_TEST
from tgen.common.constants.ranking_constants import DEFAULT_EMBEDDING_MODEL
from tgen.common.util.list_util import ListUtil
from tgen.tracing.ranking.sorters.i_sorter import iSorter

EmbeddingType = np.array


class EmbeddingSorter(iSorter):

    @staticmethod
    def sort(parent_ids: List[str], child_ids: List[str], artifact_map: Dict[str, str],
             model_name=DEFAULT_EMBEDDING_MODEL, return_scores: bool = False, **kwargs) -> Dict[str, List]:
        """
        Sorts the children artifacts from most to least similar to the parent artifacts using embeddings.
        :param parent_ids: The artifact ids of the parents.
        :param child_ids: The artifact ids of the children.
        :param artifact_map: Map of ID to artifact bodies.
        :param model_name: The name of the embedding model to use.
        :param return_scores: Whether to return the similarity scores (after min-max scaling per parent).
        :return: Map of parent to list of sorted children.
        """
        model = EmbeddingSorter.get_model(model_name)
        children_embeddings = EmbeddingSorter.create_artifact_embeddings(artifact_map, model, artifact_ids=child_ids)

        parent2rankings = {}
        for parent_id in tqdm(parent_ids, desc="Performing Ranking Via Embeddings"):
            parent_body = artifact_map[parent_id]
            parent_embedding = model.encode([parent_body])
            scores = cosine_similarity(parent_embedding, children_embeddings)[0]
            sorted_children = sorted(zip(scores, child_ids), reverse=True, key=lambda k: k[0])
            sorted_artifact_ids = [c[1] for c in sorted_children]
            sorted_artifact_scores = [c[0] for c in sorted_children]

            if return_scores:
                sorted_artifact_scores = minmax_scale(sorted_artifact_scores)
                sorted_artifact_scores = ListUtil.convert_numpy_array_to_native_types(sorted_artifact_scores)
                parent2rankings[parent_id] = (sorted_artifact_ids, sorted_artifact_scores)
            else:
                parent2rankings[parent_id] = sorted_artifact_ids
        return parent2rankings

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
        embedding_map = EmbeddingSorter.create_embedding_map(subset_content_map, model)
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
        cache_dir = EmbeddingSorter.get_cache_dir()
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
