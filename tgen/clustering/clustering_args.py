from typing import Dict, List

from tgen.clustering.methods.cluster_method import ClusterMethod
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.state.pipeline.pipeline_args import PipelineArgs

ClusterType = Dict[int, List[str]]


class ClusteringArgs(PipelineArgs):
    """
    :param: clustering_method: How the embeddings are clustered together.
    :param embedding_model: The name of the model to use to create the embeddings.
    :param dataset_creator: The creator used to get the dataset.
    :param dataset: The dataset to cluster.
    :param artifact_types: List of artifact types to cluster.
    """
    cluster_method: ClusterMethod = None
    clustering_args: Dict = None
    embedding_model: str = None
    dataset_creator: PromptDatasetCreator = None
    dataset: PromptDataset = None
    artifact_types: List[str] = None

    def __post_init__(self) -> None:
        """
        Creates dataset if creator is defined, sets optional artifact types.
        :return: None
        """
        if self.clustering_args is None:
            self.clustering_args = {}
        if self.dataset_creator:
            self.dataset = self.dataset_creator.create()
        if self.artifact_types is None:
            self.artifact_types = self.dataset.artifact_df.get_types()
