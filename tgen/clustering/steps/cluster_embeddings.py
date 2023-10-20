from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.cluster_algorithm_manager import ClusterAlgorithmManager
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class ClusterEmbeddings(AbstractPipelineStep):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Creates clusters from the embeddings.
        :param args: Args containing embedding map.
        :param state: Used to store final clusters.
        :return: None
        """
        embedding_map = state.embedding_map

        global_clusters = {}
        for cluster_method_class in args.cluster_methods:
            cluster_manager = ClusterAlgorithmManager(cluster_method_class)
            clusters = cluster_manager.cluster(embedding_map, args.cluster_reduction_factor, **args.clustering_method_args)
            clustering_method_id = cluster_manager.get_id()
            clusters = {f"{clustering_method_id}{k}": v for k, v in clusters.items()}
            global_clusters[clustering_method_id] = clusters

        state.multi_method_cluster_map = global_clusters
