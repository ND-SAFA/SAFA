from tgen.clustering.base.cluster_type import MethodClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.clustering_algorithm_manager import ClusteringAlgorithmManager
from tgen.common.constants.clustering_constants import MIN_CLUSTER_SIZE
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateClustersFromEmbeddings(AbstractPipelineStep):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Creates clusters from the embeddings.
        :param args: Args containing embedding map.
        :param state: Used to store final clusters.
        :return: None
        """

        global_clusters: MethodClusterMapType = {}
        for clustering_method in args.cluster_methods:
            cluster_manager = ClusteringAlgorithmManager(clustering_method)
            clusters = cluster_manager.cluster(state.embedding_manager, args.cluster_reduction_factor, **args.clustering_method_args)
            clustering_method_name = cluster_manager.get_method_name()
            clusters = {f"{clustering_method_name}{k}": v for k, v in clusters.items()}
            global_clusters[clustering_method.name] = clusters

        state.multi_method_cluster_map = global_clusters
