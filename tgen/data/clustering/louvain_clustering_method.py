import community

from tgen.data.clustering.i_clustering import Clusters, iClusteringMethod
from tgen.data.tdatasets.trace_dataset import TraceDataset


class LouvainClusteringMethod(iClusteringMethod):

    @staticmethod
    def cluster(trace_dataset: TraceDataset) -> Clusters:
        """
        Creates clusters of artifacts in the dataset using the Louvain Method
        :return: A dictionary mapping artifact id to its cluster num
        """
        return community.best_partition(trace_dataset.construct_graph_from_traces())
