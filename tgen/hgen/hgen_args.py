from collections import Set
from dataclasses import dataclass
from typing import Union

from tgen.data.creators.clustering.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.creators.clustering.supported_clustering_method import SupportedClusteringMethod
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.base_object import BaseObject


@dataclass
class HGenArgs(BaseObject):
    """
    The layer of the source artifacts for which higher-level artifacts will be generated
    """
    source_layer_id: str
    """
    The trainer used to generate intra layer trace links between source artifacts
    """
    tgen_trainer: AbstractTrainer = None
    """
    Dataset creator used to make dataset containing source artifacts + links if tgen_trainer is not provide
    """
    dataset_creator_for_sources: TraceDatasetCreator = None
    """
    Dataset creator used to make clusters grouping the source artifacts
    """
    dataset_creator_for_clusters: ClusterDatasetCreator = None
    """
    The base prompt to use for generation.
    """
    hgen_base_prompt: Union[str, SupportedPrompts] = SupportedPrompts.SYSTEM_REQUIREMENT_CREATION
    """
    The method to use to cluster source artifacts. Hierarchy will be built from these clusters
    """
    cluster_method: Union[SupportedClusteringMethod, Set[SupportedClusteringMethod]] = SupportedClusteringMethod.LOUVAIN

    def __post_init__(self) -> None:
        """
        Asserts necessary params have been provided and converts Enum into the proper class
        :return: None
        """
        assert self.tgen_trainer or self.dataset_creator_for_sources or self.dataset_creator_for_clusters, \
            "Must provide either a dataset creator to make a dataset with traces between artifacts of the source layer, " \
            "a trace generation trainer to create one or a cluster dataset creator containing the traces dataset."
