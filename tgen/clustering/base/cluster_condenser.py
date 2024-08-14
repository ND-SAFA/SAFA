from collections import Counter
from typing import List, Optional, Set

import numpy as np

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType, ClusterType
from tgen.common.constants.clustering_constants import DEFAULT_ALLOW_OVERLAPPING_CLUSTERS, DEFAULT_CLUSTERING_MIN_NEW_ARTIFACTS_RATION, \
    DEFAULT_CLUSTER_MIN_VOTES, DEFAULT_CLUSTER_SIMILARITY_THRESHOLD, DEFAULT_FILTER_BY_COHESIVENESS, DEFAULT_MAX_CLUSTER_SIZE, \
    DEFAULT_MIN_CLUSTER_SIZE, DEFAULT_SORT_METRIC, MIN_ARTIFACT_SIM_TO_MERGE, MIN_CLUSTER_SIM_TO_MERGE, MIN_PAIRWISE_AVG_PERCENTILE, \
    MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING
from common_resources.tools.util.dict_util import DictUtil
from common_resources.tools.util.list_util import ListUtil
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager


class ClusterCondenser:
    """
    Condenses clusters into single unique set.
    """

    def __init__(self, embeddings_manager: EmbeddingsManager,
                 threshold=DEFAULT_CLUSTER_SIMILARITY_THRESHOLD,
                 min_cluster_size: int = DEFAULT_MIN_CLUSTER_SIZE,
                 max_cluster_size: int = DEFAULT_MAX_CLUSTER_SIZE,
                 filter_cohesiveness: bool = DEFAULT_FILTER_BY_COHESIVENESS,
                 sort_metric: str = DEFAULT_SORT_METRIC,
                 allow_overlapping_clusters: bool = DEFAULT_ALLOW_OVERLAPPING_CLUSTERS):
        """
        Creates map with similarity threshold.
        :param embeddings_manager: Manages embeddings used to calculate distances between artifacts and clusters.
        :param threshold: The percentage of overlap to which consider sets are the same.
        :param min_cluster_size: The minimum size of a cluster.
        :param max_cluster_size: The maximum size of a cluster.
        :param filter_cohesiveness: If True, first filters the clusters by their cohesiveness.
        :param sort_metric: The metric to prioritize clusters by.
        :param allow_overlapping_clusters: If True, artifacts may exist in multiple clusters.
        """
        self.embeddings_manager = embeddings_manager
        self.cluster_map = {}
        self.seen_artifacts = set()
        self.threshold = threshold
        self.min_cluster_size = min_cluster_size
        self.max_cluster_size = max_cluster_size
        self.filter_cohesiveness = filter_cohesiveness
        self.sort_metric = sort_metric
        self.allow_overlapping_clusters = allow_overlapping_clusters

    def get_clusters(self, min_votes: int = DEFAULT_CLUSTER_MIN_VOTES) -> ClusterMapType:
        """
        Constructs cluster map from the clusters reaching the minimum number of votes.
        :param min_votes: The minimum number of votes to include in cluster map.
        :return: Cluster map.
        """
        selected_cluster_ids = [c_id for c_id, cluster in self.cluster_map.items() if cluster.votes >= min_votes]
        selected_cluster_ids = set(selected_cluster_ids)
        cluster_map = {i: self.cluster_map[c_id] for i, c_id in enumerate(selected_cluster_ids)}
        return cluster_map

    def add_all(self, clusters: List[ClusterType]) -> None:
        """
        Adds all clusters to the map.
        :param clusters: List of clusters to add.
        :return: None
        """
        filtered_clusters = ClusterCondenser._filter_by_size(clusters, self.min_cluster_size, self.max_cluster_size)
        if filtered_clusters:
            min_pairwise_avg = ClusterCondenser._calculate_min_pairwise_avg_threshold(filtered_clusters)
            clusters = self.filter_and_prioritize_clusters(filtered_clusters, min_pairwise_avg)
            for c in ListUtil.selective_tqdm(clusters, desc="Condensing clusters..."):
                self._add_cluster(c, min_pairwise_avg)

    def should_add(self, cluster: Cluster, min_pairwise_avg: float = None) -> bool:
        """
        Processes cluster and determines if we should add it to the set.
        :param cluster: The candidate cluster to add.
        :param min_pairwise_avg: Minimal acceptable pairwise average for clusters.
        :return: Whether cluster should be added to map.
        """
        cluster.remove_outliers()
        contains_cluster = self.contains_cluster(cluster)
        did_merge = self.try_merge(cluster)
        if not self.allow_overlapping_clusters:
            overlapping_artifacts = [a for a in cluster if a in self.seen_artifacts]
            if len(cluster) - len(overlapping_artifacts) < self.min_cluster_size:
                return False
            cluster.remove_artifacts(overlapping_artifacts, update_stats=True)
            if min_pairwise_avg and cluster.avg_pairwise_sim < min_pairwise_avg:
                return False
        contains_new_artifacts = self.contains_new_artifacts(cluster)
        if len(cluster) == 1 and not contains_new_artifacts:
            return False
        return (contains_new_artifacts or not contains_cluster) and not did_merge

    def try_merge(self, cluster: Cluster, min_similarity_score: float = MIN_CLUSTER_SIM_TO_MERGE):
        """
        Tries to merge cluster into those similar enough to it.
        :param cluster: The cluster to try to merge.
        :param min_similarity_score: The minimum score for a cluster to be deemed similar enough to another to merge them.
        :return: Whether the cluster was merged into any others.
        """
        clusters = list(self.cluster_map.values())
        clusters_to_merge_into: List[Cluster] = sorted(clusters, reverse=True, key=lambda c: cluster.similarity_to(c))
        most_similar_cluster = clusters_to_merge_into[0] if len(clusters_to_merge_into) > 0 else None
        if most_similar_cluster and cluster.similarity_to(most_similar_cluster) > min_similarity_score:
            removed_artifacts = most_similar_cluster.artifact_id_set.difference(cluster.artifact_id_set)
            added_artifacts = cluster.artifact_id_set.difference(most_similar_cluster.artifact_id_set)
            if not (len(removed_artifacts) and len(added_artifacts)):
                return True  # cluster already exists
            if not removed_artifacts:
                added_artifacts = self.merge_clusters(most_similar_cluster, cluster)
                return len(added_artifacts) > 0
        return False

    def merge_clusters(self, source_cluster: Cluster, new_cluster: Cluster,
                       min_similarity_score: float = MIN_ARTIFACT_SIM_TO_MERGE) -> List[str]:
        """
        Adds the artifacts of the new cluster to the source. Source is updated after being modified.
        :param source_cluster: The existing cluster to add new cluster to.
        :param new_cluster: The cluster whose add to source.
        :param min_similarity_score: The minimum score for a cluster to be deemed similar enough to another to merge them.
        :return: None. Updates are done in place.
        """
        artifacts_to_add = []
        for a_id in new_cluster.artifact_id_set:
            if a_id in source_cluster:
                continue
            similarity = source_cluster.similarity_to_neighbors(a_id)
            if similarity >= min_similarity_score:
                artifacts_to_add.append(a_id)
                self.seen_artifacts.add(a_id)
        source_cluster.add_artifacts(artifacts_to_add)
        return artifacts_to_add

    def contains_cluster(self, other_cluster: ClusterType) -> bool:
        """
        Calculated whether given cluster is contained within current map.
        :param other_cluster: The cluster to evaluate if contained.
        :return: True if cluster in map, false otherwise.
        """
        is_hit = False
        cluster_similarities = {}
        for c_id, source_cluster in self.cluster_map.items():
            similarity_to_cluster = self.calculate_intersection(source_cluster.artifact_id_set, other_cluster.artifact_id_set)
            if similarity_to_cluster >= self.threshold:
                is_hit = True
            cluster_similarities[source_cluster] = similarity_to_cluster
        return is_hit

    def contains_new_artifacts(self, cluster: ClusterType,
                               min_new_artifact_ratio: float = DEFAULT_CLUSTERING_MIN_NEW_ARTIFACTS_RATION) -> bool:
        """
        Calculates whether cluster has enough or new artifacts to be accepted.
        :param cluster: The cluster to evaluate if it contains enough new artifacts.
        :param min_new_artifact_ratio: The minimum acceptable ratio of new artifacts to seen artifacts in the cluster.
        :return: Whether cluster contains a ratio of new artifacts greater or equal to the default value.
        """
        unseen_artifacts = [a for a in cluster if a not in self.seen_artifacts]
        new_artifact_ratio = len(unseen_artifacts) / len(cluster)
        return new_artifact_ratio >= min_new_artifact_ratio

    def replace(self, cluster: Cluster, new_cluster: Cluster) -> None:
        """
        Replaces first cluster with the new cluster.
        :param cluster: The cluster to replace.
        :param new_cluster: The new cluster to store instead.
        :return: None, new cluster stored in place.
        """
        cluster_ids = [k for k, v in self.cluster_map.items() if v == cluster]
        if len(cluster_ids) > 1:
            raise Exception(f"Found too many clusters matching: {cluster}")
        if len(cluster_ids) == 0:
            raise Exception(f"Could not find cluster: {cluster}")
        cluster_id = cluster_ids[0]
        old_cluster = self.cluster_map[cluster_id]
        self.cluster_map[cluster_id] = new_cluster
        for a in old_cluster:
            self.seen_artifacts.remove(a)
        for a in new_cluster:
            self.seen_artifacts.add(a)
        new_cluster.votes += old_cluster.votes

    def filter_and_prioritize_clusters(self, clusters: List[Cluster], min_pairwise_avg: float = None):
        """
        Filters clusters by their cohesiveness relative to the average cohesiveness of all clusters.
        :param clusters: The clusters to filter.
        :param min_pairwise_avg: The minimum acceptable pairwise average for clusters.
        :return: List of filtered clusters.
        """
        self.vote_for_clusters(clusters)

        if min_pairwise_avg is not None:
            if self.filter_cohesiveness:
                clusters: List[Cluster] = list(filter(lambda c: c.avg_pairwise_sim >= min_pairwise_avg, clusters))

        clusters = list(sorted(clusters,
                               key=lambda c: c.calculate_importance(self.sort_metric), reverse=True))
        debugging = [cluster.get_content_of_artifacts_in_cluster() for cluster in clusters]
        return clusters

    def remove_duplicate_artifacts(self) -> None:
        """
        Ensures that there are no duplicated artifacts between clusters.
        :return: None
        """
        artifact2cluster = {}
        for cluster_id, cluster in self.cluster_map.items():
            for a_id in cluster.artifact_id_set:
                art_cluster_relationship = (cluster_id, cluster.calculate_avg_pairwise_sim_for_artifact(a_id))
                DictUtil.set_or_append_item(artifact2cluster, a_id, art_cluster_relationship)
        for a_id, cluster_relationship in artifact2cluster.items():
            if len(cluster_relationship) == 1:
                continue
            sorted_cluster_ids = ListUtil.unzip(sorted(cluster_relationship, key=lambda item: item[1]), 0)
            for cluster_id in sorted_cluster_ids[1:]:  # remove from all but the top cluster
                self.cluster_map[cluster_id].remove_artifacts([a_id])

    def _add_cluster(self, cluster: Cluster, min_pairwise_avg: float = None) -> Optional[ClusterType]:
        """
        Adds single cluster to the map.
        :param cluster: The cluster to add.
        :param min_pairwise_avg: Minimal acceptable pairwise average for clusters.
        :return: Cluster if added, None if cluster is duplicate.
        """
        should_add = self.should_add(cluster, min_pairwise_avg)
        if not should_add:
            return
        cluster_id = self.__get_next_cluster_id()
        self.cluster_map[cluster_id] = cluster
        for a in cluster.artifact_ids:
            self.seen_artifacts.add(a)
        return cluster

    @staticmethod
    def vote_for_clusters(clusters: List[Cluster]):
        """
        Votes for clusters for each time a cluster consists of the same artifact set.
        :param clusters: All possible clusters.
        :return: None.
        """
        artifacts_list = [tuple(sorted(cluster.artifact_id_set)) for cluster in clusters]
        artifacts2cluster = {}
        for cluster_index, artifacts in enumerate(artifacts_list):
            DictUtil.set_or_append_item(artifacts2cluster, artifacts, cluster_index)
        cluster_votes = Counter(artifacts_list)
        for artifacts, votes in cluster_votes.items():
            for cluster_index in artifacts2cluster[artifacts]:
                clusters[cluster_index].votes = votes

    @staticmethod
    def calculate_intersection(source: Set, target: Set) -> float:
        """
        Calculates the percentage the two sets intersect.
        :param source: Set one.
        :param target: Set two.
        :return: The ratio between the number of intersection elements vs the total union.
        """
        c_intersection = source.intersection(target)
        c1_intersection_amount = len(c_intersection) / len(source)
        c2_intersection_amount = len(c_intersection) / len(target)
        avg_intersection_amount = (c1_intersection_amount + c2_intersection_amount) / 2
        return avg_intersection_amount

    @staticmethod
    def _filter_by_size(clusters: List[Cluster], min_size: int, max_size: int):
        """
        Filters list of clusters by min and max size. If there are no resulting clusters then original list if returned.
        :param clusters: The clusters to filter.
        :param min_size: The minimum size of a cluster.
        :param max_size: The maximum size of a cluster.
        :return: The filtered clusters within the size bounds.
        """
        filter_clusters = [c for c in clusters if min_size <= len(c) <= max_size]
        return filter_clusters

    @staticmethod
    def _calculate_min_pairwise_avg_threshold(clusters: List[Cluster]) -> Optional[float]:
        """
        Calculates the minimum acceptable pairwise similarity for a cluster based on the minimum avg of the artifacts in all clusters
        :param clusters: List of the clusters to base the threshold on
        :return: The threshold for the minimum acceptable pairwise similarity
        """
        unique_clusters = set(clusters)
        cluster_scores = [cluster.avg_pairwise_sim for cluster in unique_clusters if cluster.avg_pairwise_sim is not None]
        if not cluster_scores:
            return None
        percentile_score = np.quantile(cluster_scores, MIN_PAIRWISE_AVG_PERCENTILE)
        final_score = min(percentile_score, MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING)
        return final_score

    def __get_next_cluster_id(self) -> int:
        """
        Gets the id of the next new cluster.
        :return: Next available index.
        """
        return len(self.cluster_map)
