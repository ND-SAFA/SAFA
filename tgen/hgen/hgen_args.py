from collections import Set
from dataclasses import dataclass, field
from typing import Union

from tgen.data.creators.clustering.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.creators.clustering.iclustering import Clusters
from tgen.data.creators.clustering.supported_clustering_method import SupportedClusteringMethod
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.base_object import BaseObject


@dataclass
class HGenArgs(BaseObject):
    """
    The layer of the source artifacts for which higher-level artifacts will be generated
    """
    source_layer_id: str
    """
    The type of higher-level artifact that will be generated
    """
    target_type: str
    """
    The trainer used to generate intra layer trace links between source artifacts
    """
    tgen_trainer: AbstractTrainer = None
    """
    Dataset creator used to make dataset containing source artifacts + links if tgen_trainer is not provide
    """
    dataset_creator_for_sources: PromptDatasetCreator = None
    """
    Dataset creator used to make dataset containing source artifacts + links if tgen_trainer is not provide
    """
    dataset_for_sources: PromptDataset = None
    """
    The method to use to cluster source artifacts. Hierarchy will be built from these clusters
    """
    clustering_method: Union[SupportedClusteringMethod, Set[SupportedClusteringMethod]] = SupportedClusteringMethod.LLM
    """
    Pre-created clusters to use
    """
    manual_clusters: Clusters = None
    """
    The method to use to cluster source artifacts. Hierarchy will be built from these clusters
    """
    clustering_params: dict = field(default_factory=dict)
    """
    The path to save checkpoints to if desired
    """
    export_path: str = None

    def __post_init__(self) -> None:
        """
        Asserts necessary params have been provided and converts Enum into the proper class
        :return: None
        """
        assert self.tgen_trainer or self.dataset_creator_for_sources or self.dataset_for_sources, \
            "Must provide either a dataset creator to make a dataset with traces between artifacts of the source layer, " \
            "a trace generation trainer to create one or a cluster dataset creator containing the traces dataset."
