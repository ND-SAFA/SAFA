from typing import List

from tqdm import tqdm

from gen_common.clustering.base.cluster import Cluster
from gen_common.clustering.base.cluster_condenser import ClusterCondenser
from gen_common.clustering.base.cluster_type import ClusterMapType
from gen_common.clustering.base.clustering_args import ClusteringArgs
from gen_common.clustering.base.clustering_state import ClusteringState
from gen_common.clustering.methods.clustering_algorithm_manager import ClusteringAlgorithmManager
from gen_common.constants.logging_constants import TQDM_NCOLS
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from gen_common.util.list_util import ListUtil


class CreateClustersFromEmbeddings(AbstractPipelineStep):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Creates clusters from the embeddings.
        :param args: Args containing embedding map.
        :param state: Used to store final clusters.
        :return: None
        """
        batches = state.artifact_batches if state.artifact_batches else [args.get_artifact_ids()]
        seeds = list(state.seed2artifacts.keys()) if state.seed2artifacts else []
        cluster_id_to_seed = {}
        global_clusters = {}
        initial_clusters = {}
        for i, batch_ids in enumerate(batches):
            initial_cluster_map = self.create_clusters(args, state.embedding_manager, batch_ids)
            initial_clusters.update(initial_cluster_map)
            debugging_cluster = {k: [args.dataset.artifact_df.get_artifact(a)["content"] for a in b] for k, b in
                                 initial_cluster_map.items()}
            batch_cluster_map = self.process_clusters(args, state.embedding_manager, initial_cluster_map, prefix=str(i))
            if i < len(seeds):
                cluster_id_to_seed.update({c_id: seeds[i] for c_id in batch_cluster_map.keys()})
            global_clusters.update(batch_cluster_map)

        state.cluster_id_2seeds = cluster_id_to_seed
        logger.info(f"Found {len(global_clusters)} clusters in the source artifacts.")
        state.final_cluster_map = global_clusters
        if args.save_initial_clusters:
            state.initial_cluster_map = initial_clusters

    @staticmethod
    def create_clusters(args: ClusteringArgs, embeddings_manager: EmbeddingsManager, batch_ids: List[str]) -> ClusterMapType:
        """
        Creates list of candidate batches of clusters them.
        :param args: Configuration of the clustering pipeline used to construct clusters.
        :param embeddings_manager: Contains the embeddings used to create clusters.
        :param batch_ids: IDs of subset of artifacts to cluster. If none, all artifacts in embeddings manager are used.
        :return: Map of cluster ID to clusters.
        """
        if len(batch_ids) <= args.cluster_max_size:
            batch_cluster_map = {0: Cluster.from_artifacts(batch_ids, embeddings_manager)}
        else:
            batch_cluster_map = CreateClustersFromEmbeddings.get_batch_clusters(args,
                                                                                embeddings_manager,
                                                                                batch_artifact_ids=batch_ids)
        return batch_cluster_map

    @staticmethod
    def process_clusters(args: ClusteringArgs, embeddings_manager: EmbeddingsManager,
                         batch_cluster_map: ClusterMapType, prefix: str = None) -> ClusterMapType:
        """
        Creates list of candidate batches and condenses them.
        :param args: Configuration of the clustering pipeline used to construct clusters.
        :param embeddings_manager: Contains the embeddings used to create clusters.
        :param batch_cluster_map: Map of cluster ID to clusters from batch.
        :param prefix: The prefix to append to the final cluster map.
        :return: Map of the selected cluster ID to clusters.
        """
        batch_cluster_map = CreateClustersFromEmbeddings.condense_clusters(args, embeddings_manager, batch_cluster_map)
        if prefix:
            batch_cluster_map = {f"{prefix}: {k}": v for k, v in batch_cluster_map.items()}
        batch_cluster_map = CreateClustersFromEmbeddings.reduce_large_clusters(args,
                                                                               batch_cluster_map)
        return batch_cluster_map

    @staticmethod
    def reduce_large_clusters(args: ClusteringArgs, cluster_map: ClusterMapType) -> ClusterMapType:
        """
        Recursively clusters exceeding the maximum size defined by the clustering args.
        :param args: Define clustering pipeline configuration to use for clustering large clusters.
        :param cluster_map: The cluster map containing clusters to filter.
        :return: Cluster map containing valid clusters and the children of those that got broken down.
        """
        final_cluster_map = {}
        for c_key, c in cluster_map.items():
            if len(c) > args.cluster_max_size:
                pairwise_sims = c.calculate_avg_pairwise_sim_for_artifacts(c.artifact_ids)
                ranked_artifacts = ListUtil.zip_sort(c.artifact_ids, pairwise_sims, list_to_sort_on=1, return_both=False)
                n_artifacts_to_remove = len(c) - args.cluster_max_size
                c.remove_artifacts(ranked_artifacts[:n_artifacts_to_remove])
            else:
                final_cluster_map[c_key] = c
        return final_cluster_map

    @staticmethod
    def condense_clusters(args: ClusteringArgs, embeddings_manager: EmbeddingsManager, cluster_map: ClusterMapType) -> ClusterMapType:
        """
        Condenses the clusters in the given map.
        :param args: Arguments of clustering pipeline.
        :param embeddings_manager: Contains the embeddings used to cluster.
        :param cluster_map: Map of method name to cluster to condense.
        :param i: The unique ID for this cluster.
        :return: The new cluster map.
        """
        unique_cluster_map = ClusterCondenser(embeddings_manager,
                                              threshold=args.cluster_intersection_threshold,
                                              min_cluster_size=args.cluster_min_size,
                                              max_cluster_size=args.cluster_max_size,
                                              filter_cohesiveness=args.filter_by_cohesiveness,
                                              sort_metric=args.metric_to_order_clusters,
                                              allow_overlapping_clusters=args.allow_duplicates_between_clusters)
        clusters = list(cluster_map.values())
        unique_cluster_map.add_all(clusters)

        cluster_map = unique_cluster_map.get_clusters(args.cluster_min_votes)
        return cluster_map

    @staticmethod
    def get_batch_clusters(args: ClusteringArgs, embeddings_manager: EmbeddingsManager,
                           batch_artifact_ids: List[str]) -> ClusterMapType:
        """
        Creates the clusters for a subset of artifacts.
        :param args: The clustering arguments / configuration.
        :param embeddings_manager: Contains the artifact embeddings to cluster.
        :param batch_artifact_ids: The artifacts ids to cluster.
        :return: Map of clustering method name to clusters produced by that method.
        """
        if isinstance(batch_artifact_ids, list) and len(batch_artifact_ids) == 0:
            return {}
        global_clusters: ClusterMapType = {}
        for clustering_method in tqdm(args.cluster_methods, desc="Running Clustering Algorithms...", ncols=TQDM_NCOLS):
            cluster_manager = ClusteringAlgorithmManager(clustering_method)
            max_cluster_size = min(len(batch_artifact_ids), args.cluster_max_size)
            clusters = cluster_manager.cluster(embeddings_manager,
                                               min_cluster_size=args.cluster_min_size, max_cluster_size=max_cluster_size,
                                               subset_ids=batch_artifact_ids,
                                               **args.clustering_method_args)
            clustering_method_name = cluster_manager.get_method_name()
            clusters = {f"{clustering_method_name}{k}": v for k, v in clusters.items()}
            global_clusters.update(clusters)
        return global_clusters
