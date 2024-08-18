import math
from typing import Any, Dict, List

from gen_common.clustering.base.cluster import Cluster
from gen_common.clustering.base.cluster_type import ClusterMapType
from gen_common.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from gen_common.constants.clustering_constants import CLUSTER_METHOD_INIT_PARAMS, \
    DEFAULT_RANDOM_STATE, NO_CLUSTER_LABEL, N_CLUSTERS_PARAM, RANDOM_STATE_PARAM
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from gen_common.util.dict_util import DictUtil
from gen_common.util.file_util import FileUtil
from gen_common.util.param_specs import ParamSpecs


class ClusteringAlgorithmManager:

    def __init__(self, method: SupportedClusteringMethods):
        """
        Constructs clustering method for the given algorithm.
        :param method:
        """
        self.method = method

    def cluster(self, embedding_manager: EmbeddingsManager, min_cluster_size: int,
                max_cluster_size: int, subset_ids: List[str] = None,
                **kwargs) -> ClusterMapType:
        """
        Clusters embeddings in map and creates sets of links.
        :param embedding_manager: Proxy for managing project embeddings, including retrieving them.
        :param min_cluster_size: The minimum number of artifacts in a cluster.
        :param max_cluster_size: The maximum number of artifacts in a cluster.
        :param kwargs: Clustering method arguments.
        :param subset_ids: Subset of artifacts to considering in clustering method.
        :return: Map of cluster ID to artifact ids in cluster.
        """
        if subset_ids is not None and len(subset_ids) == 0:
            raise Exception("Expected at least one artifact defined in subset ids.")
        embedding_map = embedding_manager.create_embedding_map(subset_ids)
        artifact_ids = sorted(list(embedding_map.keys()))
        embeddings = [embedding_map[artifact_id] for artifact_id in artifact_ids]
        expected_avg_cluster_size = (max_cluster_size + min_cluster_size) / 2
        n_clusters = max(math.ceil(len(embeddings) / expected_avg_cluster_size), 1)
        kwargs = self.add_internal_kwargs(kwargs, n_clusters, min_cluster_size, max_cluster_size)

        try:
            clustering_algo = self.method.value(**kwargs)
            clustering_algo.fit(embeddings)
            embedding_labels = clustering_algo.labels_
            clusters = self.create_clusters_from_labels(artifact_ids, embedding_labels, embedding_manager)
        except Exception as e:
            logger.warning(f"Clustering failed for {self.method.name}: {str(e)}")
            clusters = {}
        return clusters

    def add_internal_kwargs(self, kwargs: Dict, n_clusters: int, min_cluster_size: int,
                            max_cluster_size: int) -> Dict:
        """
        Creates kwargs internally defined for the algorithm.
        :param kwargs: Starting kwargs.
        :param n_clusters: The expected number of clusters to produce.
           :param min_cluster_size: The minimum number of artifacts in a cluster.
        :param max_cluster_size: The maximum number of artifacts in a cluster.
        :return: None, kwargs modified in place.
        """
        internal_init_params = CLUSTER_METHOD_INIT_PARAMS.get(self.method, {})
        kwargs.update(internal_init_params)

        param_specs = ParamSpecs.create_from_method(self.method.value.__init__)

        if N_CLUSTERS_PARAM in param_specs.param_names:
            DictUtil.update_kwarg_values(kwargs, n_clusters=n_clusters)
        if RANDOM_STATE_PARAM in param_specs.param_names:
            DictUtil.update_kwarg_values(kwargs, random_state=DEFAULT_RANDOM_STATE)

        kwargs = FileUtil.expand_paths(paths=kwargs, use_abs_paths=False,
                                       replacements={"[MIN_CLUSTER_SIZE]": min_cluster_size, "[MAX_CLUSTER_SIZE]": max_cluster_size})
        return kwargs

    @staticmethod
    def create_clusters_from_labels(artifact_ids: List[str], cluster_labels: List[int],
                                    embeddings_manager: EmbeddingsManager) -> ClusterMapType:
        """
        Creates cluster by linking cluster labels associated to each artifact.
        :param artifact_ids: The artifacts to cluster.
        :param cluster_labels: The cluster ID associated with each artifact.
        :param embeddings_manager: The embeddings manager used to update the statistics of the cluster.
        :return: Map of cluster to their corresponding artifacts.
        """
        clusters: Dict[Any, List[str]] = {}
        for cluster_label, artifact_id in zip(cluster_labels, artifact_ids):
            if cluster_label == NO_CLUSTER_LABEL:
                continue
            if cluster_label not in clusters:
                clusters[cluster_label] = []
            clusters[cluster_label].append(artifact_id)

        cluster_map = {cluster_id: Cluster.from_artifacts(artifact_ids, embeddings_manager)
                       for cluster_id, artifact_ids in clusters.items()}
        return cluster_map

    def get_method_name(self) -> str:
        """
        :return: Returns the method associated with the manager.
        """
        return self.method.name
