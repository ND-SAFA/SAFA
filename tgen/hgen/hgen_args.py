from dataclasses import dataclass, field
from typing import List, Union

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.constants.model_constants import get_best_default_llm_manager, get_efficient_default_llm_manager
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.base_object import BaseObject
from tgen.util.state.state.pipelinestate import PipelineArgs, PipelineState

SUMMARY_INSTRUCTIONS = "First, write a in-depth, comprehensive summary " \
                       "describing the system by focusing on the high level features the system provides its users. " \
                       "Consider the following in your response: "
TASK_PREFACE = f"{NEW_LINE} # TASKS:{NEW_LINE}"
GENERATION_INSTRUCTIONS = "Complete the following steps using your knowledge of the system:"


@dataclass
class HGenState(PipelineState):
    export_path: str = None  # Path to output of current run
    """
    Step 1 - Artifact generation
    """
    generated_artifact_content: List[str] = None  # The content generated from the questionnaire.
    summary: str = None  # The summary of all the source artifacts.
    generation_questionnaire: QuestionnairePrompt = None
    """
    Step 2 - Refine 1
    """
    refinement_number: int = 1  # The current refinement step
    refinement_questionnaire: QuestionnairePrompt = SupportedPrompts.HGEN_REFINE_QUESTIONNAIRE_CONTEXT.value  # The questionnaire containing all the artifacts.
    refined_content: List[str] = None  # The refined output.

    """
    Step 4 - Dataset Construction
    """
    source_dataset: PromptDataset = None  # The dataset containing the original artifacts.
    original_dataset: Union[PromptDataset, TraceDataset] = None

    dataset: TraceDataset = None  # The final dataset with generated artifacts.


@dataclass
class HGenArgs(PipelineArgs, BaseObject):
    """
    The layer of the source artifacts for which higher-level artifacts will be generated
    """
    source_layer_id: str
    """
    The type of higher-level artifact that will be generated
    """
    target_type: str
    """
    The type of source artifacts for which higher-level artifacts will be generated
    """
    source_type: str = "code"
    """
    The LLM manager to use to generate the new artifact content
    """
    hgen_llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager)
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
    The path to save checkpoints to if desired
    """
    export_dir: str = None
    """
    Max tokens to use for generating questionnaire.
    """
    questionnaire_tokens = 3000
    """
    Max number of tokens to use for artifact generation.
    """
    artifact_generation_tokens = 2000
    """
    Max number of tokens to use for refinement.
    """
    refinement_tokens = 2000
    """
    Max number of tokens to use for generating artifact names.
    """
    artifact_name_tokens = 1000
    """
    Format of """
    format_of_artifacts: str = None

    def __post_init__(self) -> None:
        """
        Asserts necessary params have been provided and converts Enum into the proper class
        :return: None
        """
        assert self.tgen_trainer or self.dataset_creator_for_sources or self.dataset_for_sources, \
            "Must provide either a dataset creator to make a dataset with traces between artifacts of the source layer, " \
            "a trace generation trainer to create one or a cluster dataset creator containing the traces dataset."
        self.target_type = self.target_type.capitalize()
