from dataclasses import dataclass

from tgen.constants.open_ai_constants import GENERATION_MODEL_DEFAULT
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.train.trainers.supported_trainer import SupportedTrainer


@dataclass
class HGenArgs:
    """
    The trainer class used to generate the higher-level artifacts
    """
    hgen_trainer_type: SupportedTrainer
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
    The model to use to generate the higher-level artifacts
    """
    hgen_base_model: str = GENERATION_MODEL_DEFAULT
    """
    Any necessary params needed to initializing trainer to generate the higher-level artifacts
    """
    hgen_trainer_args: OpenAIArgs = OpenAIArgs()
    """
    The base prompt to use for generation.
    """
    hgen_base_prompt: SupportedPrompts = SupportedPrompts.SYSTEM_REQUIREMENT_CREATION

    def __post_init__(self) -> None:
        """
        Asserts necessary params have been provided and converts Enum into the proper class
        :return: None
        """

        assert self.tgen_trainer or self.dataset_creator_for_sources, "Must provide either a dataset creator to make a " \
                                                                      "dataset with traces between artifacts of the source layer " \
                                                                      "or a trace generation trainer to create one."
