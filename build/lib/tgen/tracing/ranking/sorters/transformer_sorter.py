from typing import Dict, List

from common_resources.tools.util.list_util import ListUtil
from common_resources.traceability.relationship_manager.abstract_relationship_manager import AbstractRelationshipManager

from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.sorters.i_sorter import iSorter


class TransformerSorter(iSorter):

    @staticmethod
    def sort(parent_ids: List[str], child_ids: List[str], relationship_manager: AbstractRelationshipManager,
             return_scores: bool = False, **kwargs) -> Dict[str, List]:
        """
        Sorts the children artifacts from most to least similar to the parent artifacts using output from a transformer model.
        :param parent_ids: The artifact ids of the parents.
        :param child_ids: The artifact ids of the children.
        :param relationship_manager: Manages the relationship scores between each artifact pair.
        :param return_scores: Whether to return the similarity scores (after min-max scaling per parent).
        :return: Map of parent to list of sorted children.
        """
        if len(child_ids) == 0:
            return {p: [] for p in parent_ids}
        parent2rankings = {}
        iterable = ListUtil.selective_tqdm(parent_ids, desc="Performing Ranking")
        scores = relationship_manager.compare_artifacts(parent_ids, child_ids)
        for i, parent_id in enumerate(iterable):
            parent_scores = ListUtil.convert_numpy_array_to_native_types(scores[i, :])
            parent2rankings[parent_id] = RankingUtil.create_parent_child_ranking(zip(child_ids, parent_scores),
                                                                                 all_child_ids=set(child_ids),
                                                                                 return_scores=return_scores)

        return parent2rankings
