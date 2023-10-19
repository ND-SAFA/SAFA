from tgen.clustering.clustering_state import ClusteringState
from tgen.clustering.methods.icluster_method import IClusterMethod
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep, ArgType


class ClusterEmbeddings(AbstractPipelineStep):
    def _run(self, args: ArgType, state: ClusteringState) -> None:
        """
        Creates clusters from the embeddings.
        :param args: Args containing embedding map.
        :param state: Used to store final clusters.
        :return: None
        """
        embedding_map = state.embedding_map

        cluster_method: IClusterMethod = args.cluster_method.value
        clusters = cluster_method.cluster(embedding_map, args.clustering_args)

        state.clusters = clusters
