from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.icluster_method import IClusterMethod
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
            cluster_method: IClusterMethod = cluster_method_class.value()
            clusters = cluster_method.cluster(embedding_map, args.cluster_reduction_factor, **args.clustering_method_args)
            clustering_method_id = cluster_method.get_id()
            clusters = {f"{clustering_method_id}{k}": v for k, v in clusters.items()}
            global_clusters.update(clusters)

        state.multi_method_cluster_map = global_clusters
