from dataclasses import field
from typing import Dict, List

from tgen.clustering.methods.cluster_method import ClusterMethod
from tgen.common.util.dataclass_util import DataclassUtil
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
    clustering_method_args: Dict = field(default_factory=dict)
    embedding_model: str = None
    dataset_creator: PromptDatasetCreator = None
    dataset: PromptDataset = None
    artifact_types: List[str] = None

    def __post_init__(self) -> None:
        """
        Creates dataset if creator is defined, sets optional artifact types.
        :return: None
        """
        self.dataset = DataclassUtil.post_initialize_datasets(self.dataset, self.dataset_creator)
        if self.artifact_types is None:
            self.artifact_types = self.dataset.artifact_df.get_types()
