from collections import OrderedDict

import numpy as np
from typing import List, Dict, Tuple, Set

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType
from common_resources.tools.util.list_util import ListUtil
from common_resources.tools.util.np_util import NpUtil
from common_resources.tools.util.override import overrides
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.sorters.i_sorter import iSorter


class ClusterChildrenSorter(iSorter):

    @staticmethod
    @overrides(iSorter)
    def sort(parent_ids: List[str], child_ids: List[str], embedding_manager: EmbeddingsManager,
             final_clusters: ClusterMapType, return_scores: bool = False, **kwargs) -> Dict[str, List]:
        """
        Sorts the children artifacts from most to least similar to the parent artifacts based on what cluster they fall into.
        :param parent_ids: The artifact ids of the parents.
        :param child_ids: The artifact ids of the children.
        :param final_clusters: Maps id to cluster from the initial clusters from only the selected clusters.
        :param embedding_manager: Contains a map of ID to artifact bodies and the model to use and stores already created embeddings.
        :param return_scores: Whether to return the similarity scores.
        :return: Map of parent to list of sorted children.
        """
        parent2clusters = ClusterChildrenSorter._trace_parent_to_cluster(final_clusters, parent_ids, embedding_manager)
        return ClusterChildrenSorter._rank_children_predictions(set(child_ids), parent2clusters, return_scores)

    @staticmethod
    def _rank_children_predictions(child_ids: Set[str], parent2clusters: Dict[str, List[Cluster]],
                                   return_scores: bool) -> Dict[str, List]:
        """
        Ranks each of the related children.
        :param child_ids: List of children ids.
        :param parent2clusters: Maps parent to related clusters of children.
        :param return_scores: Whether to return the similarity scores.
        :return: Mapping parent to ranked related children.
        """
        parent2rankings = {}
        for parent, clusters in parent2clusters.items():
            children, scores = [], []
            if len(clusters) > 0:
                cluster = clusters.pop(0)
                for c in clusters:
                    cluster.add_artifacts(c.artifact_ids, update_stats=True)
                children = cluster.artifact_ids
                scores = [ClusterChildrenSorter._calculate_score(cluster, parent, c) for c in children]

            parent2rankings[parent] = RankingUtil.create_parent_child_ranking(zip(children, scores), all_child_ids=child_ids,
                                                                              return_scores=return_scores)
        return parent2rankings

    @staticmethod
    def _trace_parent_to_cluster(final_clusters: ClusterMapType, parent_ids: List[str],
                                 embedding_manager: EmbeddingsManager, ) -> Dict[str, List[Cluster]]:
        """
        Traces each parent to the best clusters.
        :param embedding_manager: The embedding manager to use for similarity comparisons.
        :param final_clusters: The clusters to use in the tracing.
        :param parent_ids: The parents to use in the tracing.
        :return: Mapping parent id to the related clusters.
        """
        parent2clusters = OrderedDict({p: [] for p in parent_ids})
        all_clusters = list(final_clusters.values())
        similarity_matrix = NpUtil.convert_to_np_matrix([
            ClusterChildrenSorter._get_parent_similarities_to_cluster(cluster, parent_ids, embedding_manager)
            for cluster in all_clusters])
        threshold = NpUtil.get_similarity_matrix_outliers(similarity_matrix, sigma=3)[1]
        for i, (cluster_id, cluster) in enumerate(final_clusters.items()):
            parent_relationships = similarity_matrix[i, :]
            top_parent_index = np.argmax(parent_relationships)
            top_parent, top_score = parent_ids[top_parent_index], parent_relationships[top_parent_index]
            parent2clusters[top_parent].append((cluster, top_score))
        parent2clusters = {
            p: ClusterChildrenSorter._select_best_clusters_for_parent(clusters, all_clusters, similarity_matrix[:, i], threshold)
            for i, (p, clusters) in enumerate(parent2clusters.items())}
        return parent2clusters

    @staticmethod
    def _calculate_score(cluster: Cluster, parent_id: str, child_id: str) -> float:
        """
        Calculates the score for the trace link made from the cluster.
        :param cluster: The cluster used to make the trace link.
        :param parent_id: The parent id.
        :param child_id: The child id.
        :return: The score for the trace link made from the cluster.
        """
        parent_cluster_score = cluster.similarity_to_neighbors(parent_id)
        child_cluster_score = cluster.similarity_to_neighbors(child_id)
        child_parent_score = cluster.embedding_manager.compare_artifact(parent_id, child_id)
        score = .25 * parent_cluster_score + .25 * child_cluster_score + .5 * child_parent_score
        return score

    @staticmethod
    def _select_best_clusters_for_parent(cluster_relationships: List[Tuple[Cluster, float]], all_clusters: List[Cluster],
                                         parent_cluster_sim_scores: np.ndarray, threshold: float) -> List[Cluster]:
        """
        Selects the best clusters (those above the threshold or the top option if none are above threshold).
        :param cluster_relationships: Selected clusters for parent - contains pairs of cluster and the cluster's sim score with parent.
        :param all_clusters: All possible clusters.
        :param parent_cluster_sim_scores: All similarity scores between the parent and each cluster.
        :param threshold: Threshold, above which clusters are accepted.
        :return: The best clusters.
        """
        cluster_relationships = sorted(cluster_relationships, key=lambda item: item[1], reverse=True)
        sorted_clusters, sorted_scores = ListUtil.unzip(cluster_relationships)
        best_clusters = [c for i, c in enumerate(sorted_clusters) if sorted_scores[i] >= threshold]
        best_cluster = all_clusters[np.argmax(parent_cluster_sim_scores)]  # just select the closest match to the parent
        return best_clusters if len(best_clusters) > 0 else [best_cluster]

    @staticmethod
    def _get_parent_similarities_to_cluster(cluster: Cluster, parent_ids: List[str], embedding_manager: EmbeddingsManager):
        """
        Gets the similarity of each parent to the cluster.
        :param cluster: The cluster to compare to parents.
        :param parent_ids: The ids of each parent to compare to cluster.
        :param embedding_manager: The embedding manager to use for embedding comparison.
        :return: The similarity of each parent to the cluster.
        """
        cluster.embedding_manager = embedding_manager
        return [cluster.similarity_to_neighbors(p) for p in parent_ids]
