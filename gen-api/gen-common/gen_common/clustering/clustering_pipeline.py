from typing import Dict, Type

from gen_common.clustering.base.clustering_args import ClusteringArgs
from gen_common.clustering.base.clustering_state import ClusteringState
from gen_common.clustering.steps.add_clusters_to_dataset import AddClustersToDataset
from gen_common.clustering.steps.add_orphans_to_clusters import AddOrphansToClusters
from gen_common.clustering.steps.create_batches import CreateBatches
from gen_common.clustering.steps.create_clusters_from_embeddings import CreateClustersFromEmbeddings
from gen_common.clustering.steps.create_embeddings import CreateEmbeddings
from gen_common.infra.base_object import BaseObject
from gen_common.pipeline.abstract_pipeline import AbstractPipeline


class ClusteringPipeline(AbstractPipeline[ClusteringArgs, ClusteringState], BaseObject):
    """
    Pipeline transforming dataset into clusters via embeddings.
    """
    steps = [
        CreateEmbeddings,
        CreateBatches,
        CreateClustersFromEmbeddings,
        AddOrphansToClusters,
        AddClustersToDataset
    ]

    def __init__(self, args: ClusteringArgs, **kwargs):
        """
        :param args: The starting arguments including the dataset.
        """
        super().__init__(args, self.steps, no_project_summary=True, **kwargs)

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
