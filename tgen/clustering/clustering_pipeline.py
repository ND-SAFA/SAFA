from typing import Type

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.steps.add_clusters_to_dataset import AddClustersToDataset
from tgen.clustering.steps.cluster_embeddings_from_embeddings import CreateClustersFromEmbeddings
from tgen.clustering.steps.condense_clusters import CondenseClusters
from tgen.clustering.steps.create_embeddings import CreateEmbeddings
from tgen.clustering.steps.link_orphans import LinkOrphans
from tgen.common.constants.deliminator_constants import EMPTY_STRING
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
        args.export_dir = EMPTY_STRING  # TODO: Remove before committing!
        super().__init__(args, self.steps, project_summary_sections=[], **kwargs)

    def state_class(self) -> Type[ClusteringState]:
        """
        :return: Returns the state of the clustering pipeline.
        """
        return ClusteringState
