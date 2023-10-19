from typing import Type

from tgen.clustering.clustering_args import ClusteringArgs
from tgen.clustering.clustering_state import ClusteringState
from tgen.clustering.steps.cluster_embeddings import ClusterEmbeddings
from tgen.clustering.steps.create_embeddings import CreateEmbeddings
from tgen.common.util.base_object import BaseObject
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline


class ClusteringPipeline(AbstractPipeline[ClusteringArgs, ClusteringState], BaseObject):
    """
    Pipeline transforming dataset into clusters via embeddings.
    """
    steps = [CreateEmbeddings, ClusterEmbeddings]

    def __init__(self, args: ClusteringArgs):
        """
        :param args: The starting arguments including the dataset.
        """
        super().__init__(args, self.steps)

    def state_class(self) -> Type[ClusteringState]:
        """
        :return: Returns the state of the clustering pipeline.
        """
        return ClusteringState
