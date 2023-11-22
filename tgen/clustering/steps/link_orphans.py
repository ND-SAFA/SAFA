from typing import List, Set

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.clustering_algorithm_manager import ClusteringAlgorithmManager
from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from tgen.clustering.steps.condense_clusters import CondenseClusters
from tgen.clustering.steps.create_clusters_from_embeddings import CreateClustersFromEmbeddings
from tgen.common.constants.clustering_constants import ADD_ORPHAN_TO_CLUSTER_THRESHOLD
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.dict_util import DictUtil
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class LinkOrphans(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Attempts to link orphans to their best fit cluster, if minimum score is not reached then
        cluster containing singleton artifact is created.
        :param args: The arguments to the clustering pipeline.
        :param state: The current state of the clustering pipeline.
        :return: None, modifications done in place.
        """
        cluster_map: ClusterMapType = state.final_cluster_map
        clusters: List[Cluster] = list(cluster_map.values())

        seen_artifacts = self.collect_seen_artifacts(clusters)
        all_artifacts = set(args.dataset.artifact_df.index)
        orphan_artifact_id_set = all_artifacts.difference(seen_artifacts)

        adopted_orphans = self.place_orphans_in_homes(args, clusters, orphan_artifact_id_set)
        orphan_artifact_id_set = orphan_artifact_id_set.difference(adopted_orphans)
        self.cluster_orphans(args, state, cluster_map, orphan_artifact_id_set, args.min_orphan_similarity)
        for a in orphan_artifact_id_set:
            self.add_singleton_cluster(a, cluster_map, state.embedding_manager)

    @classmethod
    def cluster_orphans(cls, args: ClusteringArgs, state: ClusteringState, cluster_map: ClusterMapType,
                        orphan_artifact_id_set: Set[str], min_cluster_similarity: float):
        """
        Attempts to create clusters from the orphan artifacts.
        :param args: The arguments to the clustering pipeline
        :param cluster_map: The cluster map to add new clusters to.
        :param orphan_artifact_id_set:Set of orphan artifact ids.
        :param min_cluster_similarity: The minimum similarity score for a cluster to be accepted.
        High number default intended to create more clusters to capture sub-groups.
        :return: None. Cluster map modified in place.
        """
        if len(orphan_artifact_id_set) == 0:
            return
        cluster_min_size = min(args.cluster_min_size, len(orphan_artifact_id_set))
        orphan_args = ClusteringArgs(**DataclassUtil.convert_to_dict(args, cluster_min_size=cluster_min_size,
                                                                     dataset_creator=None,
                                                                     subset_ids=list(orphan_artifact_id_set)))
        orphan_state = ClusteringState(**DataclassUtil.convert_to_dict(state))
        CreateClustersFromEmbeddings().run(orphan_args, orphan_state, re_run=True)
        CondenseClusters().run(orphan_args, orphan_state, re_run=True)
        orphan_cluster_map = orphan_state.final_cluster_map
        clusters = [c for c in orphan_cluster_map.values() if c.avg_similarity >= min_cluster_similarity]
        for c in clusters:
            cls.add_cluster(cluster_map, c)
            for a in c:
                orphan_artifact_id_set.remove(a)

    @staticmethod
    def collect_seen_artifacts(clusters: List[Cluster]) -> Set[str]:
        """
        Gathers set of artifacts referenced in clusters.
        :param clusters: List of clusters referencing artifacts in set.
        :return: The set of artifacts referenced.
        """
        seen_artifacts = set()
        for cluster in clusters:
            for a in cluster.artifact_id_set:
                seen_artifacts.add(a)
        return seen_artifacts

    @staticmethod
    def place_orphans_in_homes(args: ClusteringArgs, clusters: List[Cluster], orphan_artifacts: Set[str]) -> Set[str]:
        """
        Attempts to add orphans to clusters
        :param args: The arguments to the clustering pipeline.
        :param clusters: The list of clusters to place orphans into.
        :param orphan_artifacts: List of artifact ids that need clusters.
        :return: set of orphans that found homes.
        """
        avg_similarity_threshold = 0 if args.add_orphans_to_best_home else ADD_ORPHAN_TO_CLUSTER_THRESHOLD
        adopted_orphans = set()
        best_clusters = {}
        for artifact_id in orphan_artifacts:
            best_cluster, sim_score = LinkOrphans.get_best_home_for_orphan(artifact_id, clusters)
            DictUtil.set_or_append_item(best_clusters, best_cluster, (artifact_id, sim_score))
        for cluster, orphans in best_clusters.items():
            sorted_orphans = sorted(orphans, key=lambda x: x[1])
            for (orphan_id, sim_score) in sorted_orphans:
                if sim_score >= avg_similarity_threshold and len(cluster) < args.cluster_max_size:
                    cluster.add_artifact(orphan_id)
                    adopted_orphans.add(orphan_id)
        return adopted_orphans

    @classmethod
    def get_best_home_for_orphan(cls, artifact_id: str, clusters: List[Cluster]) -> List[Cluster]:
        """
        Places orphan in cluster in which its similarity to the cluster is about the same as the average cluster distance.
        :param artifact_id: The artifact ID of the orphan.
        :param clusters: The clusters to check if want artifact.
        :return: The clusters accepting that artifacts.
        """
        similarities_to_clusters = [c.similarity_to_neighbors(artifact_id) for c in clusters]
        similarity_score, best_cluster = sorted(zip(similarities_to_clusters, clusters), key=lambda t: t[0], reverse=True)[0]

        return best_cluster, similarity_score

    @classmethod
    def add_singleton_cluster(cls, a_id: str, cluster_map: ClusterMapType, embeddings_manager: EmbeddingsManager) -> None:
        """
        Adds singleton cluster containing artifact id to cluster map.ngl
        :param a_id: The artifact to be contained by cluster.
        :param cluster_map: The cluster map to add cluster to.
        :param embeddings_manager: The embeddings manager used to update the cluster stats.
        :return: None. Map updated in place.
        """
        new_cluster = Cluster.from_artifacts([a_id], embeddings_manager)
        cls.add_cluster(cluster_map, new_cluster)

    @staticmethod
    def add_cluster(cluster_map: ClusterMapType, cluster: Cluster) -> None:
        """
        Adds cluster to cluster map at the next index.
        :param cluster_map: The map to add cluster to.
        :param cluster: The cluster to add.
        :return: None. Map modified in place.
        """
        next_cluster_index = len(cluster_map)
        cluster_map[next_cluster_index] = cluster
