from dataclasses import dataclass
from typing import Union, List

from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.state.state import State


@dataclass
class HGenState(State):
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

    """
    Optional Step - Refine 1
    """
    # refinement_number: int = 1  # The current refinement step
    # refinement_questionnaire: QuestionnairePrompt = SupportedPrompts.HGEN_REFINE_QUESTIONNAIRE.value
    # # The questionnaire containing all the artifacts.

    refined_content: List[str] = None  # The refined output.

    """
    Step 4 - Dataset Construction
    """
    dataset: TraceDataset = None  # The final dataset with generated artifacts.
