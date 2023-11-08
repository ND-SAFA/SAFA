from dataclasses import dataclass

from tgen.common.util.dataclass_util import required_field
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.pipeline.state import State
from tgen.summarizer.summarizer_args import SummarizerArgs


@dataclass
class LLMTrainerState(State):
    """
    Represents a state of the LLMTrainer in time
    """
    """
    :param prompt_builder: Creates the prompts for trace link prediction.
    """
    prompt_builder: PromptBuilder = required_field(field_name="prompt_builder")
    """
    :param trainer_dataset_manager: The dataset manager for training and prediction
    """
    trainer_dataset_manager: TrainerDatasetManager = required_field(field_name="trainer_dataset_manager")
    """
    :param llm_manager: The manager incharge of the lLM being used
    """
    llm_manager: AbstractLLMManager = required_field(field_name="llm_manager")
    """
    :param completion_type: The type of completion (either generation or completion)
    """
    completion_type: LLMCompletionType = LLMCompletionType.GENERATION

