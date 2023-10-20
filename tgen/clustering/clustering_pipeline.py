from typing import Type

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.steps.add_clusters_to_dataset import AddClustersToDataset
from tgen.clustering.steps.cluster_embeddings import ClusterEmbeddings
from tgen.clustering.steps.condense_clusters import CondenseClusters
from tgen.clustering.steps.create_embeddings import CreateEmbeddings
from tgen.common.util.base_object import BaseObject
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline


class ClusteringPipeline(AbstractPipeline[ClusteringArgs, ClusteringState], BaseObject):
    """
    Pipeline transforming dataset into clusters via embeddings.
    """
    steps = [CreateEmbeddings, ClusterEmbeddings, CondenseClusters, AddClustersToDataset]

    def __init__(self, args: ClusteringArgs, **kwargs):
        """
        :param args: The starting arguments including the dataset.
        """
        super().__init__(args, self.steps, project_summary_sections=[], **kwargs)

    def state_class(self) -> Type[ClusteringState]:
        """
        :return: Returns the state of the clustering pipeline.
        """
        return ClusteringState
