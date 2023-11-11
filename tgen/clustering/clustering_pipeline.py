from typing import Type, Dict

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.steps.add_clusters_to_dataset import AddClustersToDataset
from tgen.clustering.steps.condense_clusters import CondenseClusters
from tgen.clustering.steps.create_clusters_from_embeddings import CreateClustersFromEmbeddings
from tgen.clustering.steps.create_embeddings import CreateEmbeddings
from tgen.clustering.steps.link_orphans import LinkOrphans
from tgen.common.util.base_object import BaseObject
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline


class ClusteringPipeline(AbstractPipeline[ClusteringArgs, ClusteringState], BaseObject):
    """
    Pipeline transforming dataset into clusters via embeddings.
    """
    steps = [CreateEmbeddings, CreateClustersFromEmbeddings, CondenseClusters, LinkOrphans, AddClustersToDataset]

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

    def get_input_output_counts(self) -> Dict[str, int]:
        """
        Returns an empty dict because there are no inputs or outputs to the LLM
        :return: An empty dict because there are no inputs or outputs to the LLM
        """
        return {}
