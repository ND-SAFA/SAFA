from typing import Dict, List

from sklearn.preprocessing import _data
from tqdm import tqdm

from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.common.util.list_util import ListUtil
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.tracing.ranking.sorters.i_sorter import iSorter


class EmbeddingSorter(iSorter):

    @staticmethod
    def sort(parent_ids: List[str], child_ids: List[str], embedding_manager: EmbeddingsManager,
             return_scores: bool = False, **kwargs) -> Dict[str, List]:
        """
        Sorts the children artifacts from most to least similar to the parent artifacts using embeddings.
        :param parent_ids: The artifact ids of the parents.
        :param child_ids: The artifact ids of the children.
        :param embedding_manager: Contains a map of ID to artifact bodies and the model to use and stores already created embeddings
        :param return_scores: Whether to return the similarity scores (after min-max scaling per parent).
        :return: Map of parent to list of sorted children.
        """
        if len(child_ids) == 0:
            return {p: [] for p in parent_ids}
        children_embeddings = embedding_manager.create_artifact_embeddings(artifact_ids=child_ids)

        parent2rankings = {}
        iterable = tqdm(parent_ids, desc="Performing Ranking Via Embeddings") if len(parent_ids) >= 5 else parent_ids
        for parent_id in iterable:
            parent_embedding = embedding_manager.get_embedding(parent_id)
            scores = EmbeddingUtil.calculate_similarities([parent_embedding], children_embeddings)[0]
            sorted_children = sorted(zip(scores, child_ids), reverse=True, key=lambda k: k[0])
            sorted_artifact_ids = [c[1] for c in sorted_children]
            sorted_artifact_scores = [c[0] for c in sorted_children]

            if return_scores:
                sorted_artifact_scores = ListUtil.convert_numpy_array_to_native_types(sorted_artifact_scores)
                parent2rankings[parent_id] = (sorted_artifact_ids, sorted_artifact_scores)
            else:
                parent2rankings[parent_id] = sorted_artifact_ids
        return parent2rankings
