from typing import List, Set

from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.dataclass_util import DataclassUtil
from common_resources.tools.util.list_util import ListUtil
from common_resources.traceability.relationship_manager.embeddings_manager import EmbeddingsManager

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.steps.create_clusters_from_embeddings import CreateClustersFromEmbeddings
from tgen.common.constants.hgen_constants import ALLOWED_ORPHAN_CLUSTER_SIZE_DELTA, ALLOWED_ORPHAN_SIMILARITY_DELTA, \
    MIN_ORPHAN_HOME_SIMILARITY
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class AddOrphansToClusters(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Attempts to link orphans to their best fit cluster, if minimum score is not reached then
        cluster containing singleton artifact is created.
        :param args: The arguments to the clustering pipeline.
        :param state: The current state of the clustering pipeline.
        :return: None, modifications done in place.
        """
        if not args.add_orphans_to_homes:
            return
        cluster_map: ClusterMapType = state.final_cluster_map
        clusters: List[Cluster] = list(filter(lambda cluster: len(cluster) > 1, cluster_map.values()))

        seen_artifacts = self.collect_seen_artifacts(clusters)
        all_artifacts = set(args.get_artifact_ids())
        orphan_artifact_id_set = all_artifacts.difference(seen_artifacts)

        logger.info(f"{len(orphan_artifact_id_set)} artifacts were not clustered.")

        if len(orphan_artifact_id_set) > args.cluster_min_size and not args.add_orphans_to_best_home:
            self.cluster_orphans(args, state, cluster_map, orphan_artifact_id_set, args.min_orphan_similarity)
        self.place_orphans_in_homes(args, clusters, orphan_artifact_id_set)

        if args.allow_singleton_clusters:
            for a in orphan_artifact_id_set:
                self.add_singleton_cluster(a, cluster_map, state.embedding_manager)

    @classmethod
    def cluster_orphans(cls, args: ClusteringArgs, state: ClusteringState, cluster_map: ClusterMapType,
                        orphan_artifact_id_set: Set[str], min_cluster_similarity: float):
        """
        Attempts to create clusters from the orphan artifacts.
        :param args: The arguments to the clustering pipeline
        :param state: State of clustering pipeline.
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
        orphan_state.artifact_batches = [orphan_artifact_id_set]
        CreateClustersFromEmbeddings().run(orphan_args, orphan_state, re_run=True)
        orphan_cluster_map = orphan_state.final_cluster_map
        clusters = [c for c in orphan_cluster_map.values() if c.avg_similarity >= min_cluster_similarity]
        for c in clusters:
            cls.add_cluster(cluster_map, c)
            for a in c:
                if a in orphan_artifact_id_set:  # could be in multiple clusters, and handled before this.
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
    def place_orphans_in_homes(args: ClusteringArgs, clusters: List[Cluster], orphan_artifacts: Set[str]) -> None:
        """
        Attempts to house orphans from best to worst houses for them.
        :param args: The arguments to the clustering pipeline.
        :param clusters: The list of clusters to place orphans into.
        :param orphan_artifacts: List of artifact ids that need clusters.
        :return: set of orphans that found homes.
        """
        adopted_orphans = set()
        best_clusters = []
        for artifact_id in ListUtil.selective_tqdm(orphan_artifacts, desc="Placing orphans in homes."):
            similarities_to_clusters = [c.similarity_to_neighbors(artifact_id) for c in clusters]
            artifact_iterable = [(artifact_id, t[0], t[1]) for t in zip(clusters, similarities_to_clusters)]
            best_clusters.extend(artifact_iterable)

        best_clusters = sorted(best_clusters, key=lambda t: t[-1], reverse=True)

        for i, (artifact, cluster, cluster_similarity) in enumerate(best_clusters):
            delta = cluster.min_sim - cluster_similarity if len(cluster) > 1 else 0
            within_similarity_threshold = delta < ALLOWED_ORPHAN_SIMILARITY_DELTA
            within_cluster_size = len(cluster) < args.cluster_max_size + ALLOWED_ORPHAN_CLUSTER_SIZE_DELTA
            above_minimum_score = cluster_similarity >= MIN_ORPHAN_HOME_SIMILARITY
            not_seen = artifact not in adopted_orphans
            if args.add_orphans_to_best_home or (within_similarity_threshold and above_minimum_score):
                if not (within_cluster_size and not_seen):
                    continue
                cluster.add_artifacts(artifact)
                adopted_orphans.add(artifact)
                orphan_artifacts.remove(artifact)

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
        cluster_map[str(next_cluster_index)] = cluster
