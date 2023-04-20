from dataclasses import dataclass
from typing import Type, Dict, Any

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.train.trainers.abstract_trainer import AbstractTrainer


@dataclass
class HGenArgs:
    """
    The trainer class used to generate the higher-level artifacts
    """
    hgen_trainer_class: Type[AbstractTrainer]
    """
    Any necessary params needed to initializing trainer to generate the higher-level artifacts
    """
    hgen_trainer_params: Dict[str, Any]
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

    def __post_init__(self) -> None:
        """
        Asserts necessary params have been provided
        :return: None
        """
        assert self.tgen_trainer or self.dataset_creator_for_sources, "Must provide either a dataset creator to make a " \
                                                                      "dataset with traces between artifacts of the source layer " \
                                                                      "or a trace generation trainer to create one."
