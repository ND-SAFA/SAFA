import uuid

from cdlib import algorithms

from tgen.data.clustering.iclustering import iClustering, Clusters
from tgen.data.tdatasets.trace_dataset import TraceDataset


class GraphClustering(iClustering):

    @staticmethod
    def cluster(trace_dataset: TraceDataset, resolution: float = 1.2, **kwargs) -> Clusters:
        """
        Performs clustering by using the graph-based method
        :param trace_dataset: The dataset to create clusters from
        :param resolution: The resolution to use for Louvain
        :return: The mapping of cluster names to list of artifacts in the cluster
        """
        graph = trace_dataset.construct_graph_from_traces()
        communities = algorithms.louvain(graph, resolution=resolution).communities
        return {uuid.uuid4(): community for community in communities if len(community) >= 1}
