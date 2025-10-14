from collections import Counter
from typing import Any, Callable, Dict, List, Set, Tuple, Type

from gen_common.clustering.base.cluster import Cluster
from gen_common.clustering.base.cluster_type import ClusterMapType
from gen_common.traceability.ranking.sorters.i_sorter import iSorter
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from gen_common.util.dict_util import DictUtil
from gen_common.util.override import overrides
from gen_common.util.ranking_util import RankingUtil


class ClusterVotingSorter(iSorter):

    @staticmethod
    @overrides(iSorter)
    def sort(parent_ids: List[str], child_ids: List[str], embedding_manager: EmbeddingsManager,
             initial_clusters: ClusterMapType, final_clusters: ClusterMapType,
             return_scores: bool = False, **kwargs) -> Dict[str, List]:
        """
        Sorts the children artifacts from most to least similar to the parent artifacts based on what cluster they fall into.
        :param parent_ids: The artifact ids of the parents.
        :param child_ids: The artifact ids of the children.
        :param initial_clusters: Maps id to cluster from the initial clusters across algorithms.
        :param final_clusters: Maps id to cluster from the initial clusters from only the selected clusters.
        :param embedding_manager: Contains a map of ID to artifact bodies and the model to use and stores already created embeddings.
        :param return_scores: Whether to return the similarity scores (after min-max scaling per parent).
        :return: Map of parent to list of sorted children.
        """
        parent_ids, child_ids = set(parent_ids), set(child_ids)
        votes = ClusterVotingSorter.iterate_through_cluster(clusters=initial_clusters, results_type=Counter,
                                                            method2perform=ClusterVotingSorter.count_co_occurrences,
                                                            child_ids=child_ids, parent_ids=parent_ids)
        parent_child_scores = ClusterVotingSorter.iterate_through_cluster(
            clusters=final_clusters, child_ids=child_ids, parent_ids=parent_ids,
            method2perform=lambda results_store, child, parent:
            ClusterVotingSorter.score_parent_child_relationship(votes, embedding_manager, results_store, child, parent))

        parent2rankings = {parent: RankingUtil.create_parent_child_ranking(children_scores=list(children2scores.items()),
                                                                           all_child_ids=child_ids, return_scores=return_scores)
                           for parent, children2scores in parent_child_scores.items()}
        return parent2rankings

    @staticmethod
    def score_parent_child_relationship(votes: Counter, embedding_manager: EmbeddingsManager,
                                        results_store: Dict, child: str, parent: str) -> None:
        """
        Scores the relationship between child and parent based on co-occurrences.
        :param votes: Counter with the number of co-occurrences between child and parent.
        :param embedding_manager: Contains embeddings to compare parent and child meaning similarity.
        :param results_store: Stores the results.
        :param child: The child id.
        :param parent:The parent id.
        :return: None
        """
        max_count = votes.most_common(1).pop()[1]
        count = votes.get(ClusterVotingSorter._get_parent_child_key(parent, child), 1)
        score = ClusterVotingSorter._calculate_score(embedding_manager=embedding_manager, votes=count,
                                                     max_votes=max_count, parent=parent, child=child)
        DictUtil.set_or_append_item(results_store, parent, (child, score), iterable_type=dict)

    @staticmethod
    def count_co_occurrences(results_store: Dict, child: str, parent: str) -> None:
        """
        Updates the count of times the child and parent co-occur
        :param results_store: Stores the counts.
        :param child: The child id.
        :param parent: The parent id.
        :return: None.
        """
        DictUtil.set_or_increment_count(results_store, ClusterVotingSorter._get_parent_child_key(parent, child))

    @staticmethod
    def iterate_through_cluster(clusters: ClusterMapType, method2perform: Callable,
                                child_ids: Set[str], parent_ids: Set[str], results_type: Type = dict) -> Any:
        """
        Iterates through each parent and child pair in a cluster.
        :param clusters: The clusters to iterate through.
        :param method2perform: Method to perform on each parent, child pair.
        :param child_ids: Set of ids of all children.
        :param parent_ids: Set of ids of all parents.
        :param results_type: The type of iterable to store the result in.
        :return: The results in whatever type of storage requested.
        """
        results_store = results_type()
        for cluster in clusters.values():
            parents, children = ClusterVotingSorter._find_parent_and_children_in_cluster(cluster, child_ids, parent_ids)
            for parent in parents:
                for child in children:
                    method2perform(results_store, child, parent)
        return results_store

    @staticmethod
    def _find_parent_and_children_in_cluster(cluster: Cluster, all_child_ids: Set[str],
                                             all_parent_ids: Set[str]) -> Tuple[Set[str], Set[str]]:
        """
        Identifies the parents versus children in a clusters artifacts.
        :param cluster: The cluster to find parents and children in.
        :param all_child_ids: List of all possible children.
        :param all_parent_ids: List of all possible parents.
        :return: Set of parent ids and set of children ids in cluster.
        """
        parents = cluster.artifact_id_set.difference(all_child_ids)
        children = cluster.artifact_id_set.difference(all_parent_ids)
        return parents, children

    @staticmethod
    def _get_parent_child_key(parent: str, child: str) -> str:
        """
        Creates a unique key for the parent and child pair.
        :param parent: The parent id.
        :param child: The child id.
        :return: A unique key for the parent and child pair.
        """
        return f"{child}-{parent}"

    @staticmethod
    def _calculate_score(embedding_manager: EmbeddingsManager, votes: int, max_votes: int, parent: str, child: str) -> float:
        """
        Scores the relationship between parent and child.
        :param embedding_manager: The embedding manager to use for comparing child and parent meaning similarity.
        :param votes: Number of co-occurrences between child and parents in clusters. 
        :param max_votes: Maximum number of times that a parent and child occurred together in the clusters.
        :param parent: The id of the parent.
        :param child: The id of the child.
        :return: The score between child and parent.
        """
        sim_score = embedding_manager.compare_artifact(parent, child)
        vote_score = (votes / max_votes)
        score = 0 * sim_score + 1 * vote_score
        return score
