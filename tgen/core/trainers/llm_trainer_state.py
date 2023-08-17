from dataclasses import dataclass

from tgen.common.util.dataclass_util import required_field
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.summarizer.summarizer import Summarizer
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.state.state import State


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
    :param summarizer: The summarizer to use for shortening artifacts over the token limit.
    """
    summarizer: Summarizer = None
    """
    :param completion_type: The type of completion (either generation or completion)
    """
    completion_type: LLMCompletionType = LLMCompletionType.GENERATION

    def __post_init__(self):
        if self.summarizer is None:
            self.summarizer = Summarizer(self.llm_manager, model_name=self.llm_manager.llm_args.model,
                                         code_or_exceeds_limit_only=False,
                                         max_completion_tokens=self.llm_manager.llm_args.get_max_tokens())
