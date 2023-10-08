import os
from typing import Dict, List

from sentence_transformers.SentenceTransformer import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing._data import minmax_scale
from tqdm import tqdm

from tgen.common.constants.environment_constants import IS_TEST
from tgen.common.util.list_util import ListUtil
from tgen.tracing.ranking.sorters.i_sorter import iSorter
from tgen.common.constants.ranking_constants import DEFAULT_EMBEDDING_MODEL


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
        cache_dir = os.environ.get("HF_DATASETS_CACHE", None)
        if cache_dir is None or IS_TEST or not os.path.exists(cache_dir):
            cache_dir = None
        model = SentenceTransformer(model_name, cache_folder=cache_dir)

        children_bodies = [artifact_map[a_id] for a_id in child_ids]
        children_embeddings = model.encode(children_bodies)

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
