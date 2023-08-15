from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Union

from tgen.common.util.base_object import BaseObject
from tgen.common.util.dataclass_util import required_field, DataclassUtil
from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.constants.model_constants import get_best_default_llm_manager, get_efficient_default_llm_manager
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.core.trainers.abstract_trainer import AbstractTrainer
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.state.pipeline.pipeline_args import PipelineArgs
from tgen.state.state import State


class PredictionStep(Enum):
    INSTRUCTIONS = auto()
    FORMAT = auto()
    GENERATION = auto()
    REFINEMENT = auto()
    NAME = auto()


DEFAULT_MAX_TOKENS = 50000
DEFAULT_MAX_TOKENS_SMALL = 2000


@dataclass
class HGenState(State):
    export_path: str = None  # Path to output of current run
    """
    Step 1 - Dataset Construction
    """
    source_dataset: PromptDataset = None  # The dataset containing the original artifacts.
    original_dataset: Union[PromptDataset, TraceDataset] = None

    """
    Step 2 - Input generation
    """
    description_of_artifact: str = None  # describes what the target type is
    format_of_artifacts: str = None  # The format to use for the generated artifacts
    questions: List[str] = None  # The questions to use to probe the model for a good summary

    """
    Step 3 - Artifact generation
    """
    generated_artifact_content: List[str] = None  # The content generated from the questionnaire.
    summary: str = None  # The summary of all the source artifacts.
    generation_questionnaire: QuestionnairePrompt = None

    """
    Optional Step - Refine 1
    """
    refinement_number: int = 1  # The current refinement step
    refinement_questionnaire: QuestionnairePrompt = SupportedPrompts.HGEN_REFINE_QUESTIONNAIRE.value
    # The questionnaire containing all the artifacts.
    refined_content: List[str] = None  # The refined output.

    """
    Step 4 - Dataset Construction
    """
    dataset: TraceDataset = None  # The final dataset with generated artifacts.


@dataclass
class HGenArgs(PipelineArgs, BaseObject):
    """
    The layer of the source artifacts for which higher-level artifacts will be generated
    """
    source_layer_id: str = required_field(field_name="source_layer_id")
    """
    The type of higher-level artifact that will be generated
    """
    target_type: str = required_field(field_name="target_type")
    """
    The type of source artifacts for which higher-level artifacts will be generated
    """
    source_type: str = "code"
    """
    The LLM manager to use to generate the new artifact content and other more complex tasks
    """
    hgen_llm_manager_best: AbstractLLMManager = field(default_factory=get_best_default_llm_manager)
    """
    The LLM manager to use to generate the artifact names and less complex tasks
    """
    hgen_llm_manager_efficient: AbstractLLMManager = field(default_factory=get_efficient_default_llm_manager)
    """
    The trainer used to generate intra layer trace links between source artifacts
    """
    tgen_trainer: AbstractTrainer = field(default_factory=get_efficient_default_llm_manager)
    """
    Dataset creator used to make dataset containing source artifacts + links if tgen_trainer is not provide
    """
    dataset_creator_for_sources: PromptDatasetCreator = None
    """
    Dataset creator used to make dataset containing source artifacts + links if tgen_trainer is not provide
    """
    dataset_for_sources: PromptDataset = None
    """
    Max tokens to use for predictions.
    """
    max_tokens: Dict[int, int] = field(default_factory=dict)
    """
    Summary of the system 
    """
    system_summary: str = None
    """
    The llm manager to use for each prediction step
    """
    llm_managers: Dict[int, AbstractLLMManager] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        """
        Asserts necessary params have been provided and converts Enum into the proper class
        :return: None
        """
        assert self.tgen_trainer or self.dataset_creator_for_sources or self.dataset_for_sources, \
            "Must provide either a dataset creator to make a dataset with traces between artifacts of the source layer, " \
            "a trace generation trainer to create one or a cluster dataset creator containing the traces dataset."
        self.llm_managers = {e.value: (self.hgen_llm_manager_best if e != PredictionStep.NAME
                                       else self.hgen_llm_manager_efficient) for e in PredictionStep}
        self.llm_managers[PredictionStep.FORMAT.value] = OpenAIManager(OpenAIArgs(model='gpt-4-0314'))
        for e in PredictionStep:
            if e.value not in self.max_tokens:
                if e in [PredictionStep.NAME, PredictionStep.FORMAT]:
                    self.max_tokens[e.value] = DEFAULT_MAX_TOKENS_SMALL
                else:
                    self.max_tokens[e.value] = DEFAULT_MAX_TOKENS
