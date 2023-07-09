from dataclasses import dataclass

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.summarizer.summarizer import Summarizer
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.pipeline.pipeline_state import PipelineState


@dataclass
class LLMTrainerState(PipelineState):
    """
    Represents a state of the LLMTrainer in time
    """

    """
    :param prompt_builder: Creates the prompts for trace link prediction.
    """
    prompt_builder: PromptBuilder
    """
    :param trainer_dataset_manager: The dataset manager for training and prediction
    """
    trainer_dataset_manager: TrainerDatasetManager
    """
    :param llm_manager: The manager incharge of the lLM being used
    """
    llm_manager: AbstractLLMManager
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
            self.summarizer = Summarizer(self.llm_manager, model_for_token_limit=self.llm_manager.llm_args.model,
                                         code_or_exceeds_limit_only=False,
                                         max_tokens_for_token_limit=self.llm_manager.llm_args.get_max_tokens())
