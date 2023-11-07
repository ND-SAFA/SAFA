from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

from tgen.common.util.enum_util import EnumDict
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.embeddings.embeddings_manager import EmbeddingsManager
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
    Optional Step 3 - Break project into parts and generate for each part
    """
    id_to_cluster_artifacts: Dict[Any, List[EnumDict]] = None  # maps cluster id to the list of artifacts in that cluster
    cluster_dataset: Optional[PromptDataset] = None  # contains prompt dataset with just the artifact df of the clusters.
    embedding_manager: EmbeddingsManager = None  # allows embeddings to be reused

    """
    Step 4 - Artifact generation
    """
    generation_predictions: Dict[str, Set[str]] = None  # dictionary mapping generated content to a list of related source ids
    cluster2generation: Dict[Any, List[str]] = None  # Maps cluster id to the generation that was produced for that cluster
    n_generations: int = 0  # number of runs of artifact generation

    """
    Optional Step 5 - Refine content on rerun of hgen
    """
    all_generated_content: Dict[str, Set[str]] = None  # All generated content across all runs
    refined_content: Dict[str, Set[str]] = None  # The final selected artifact content

    """
    Step 6 - Rename the artifacts generated.
    """
    new_artifact_dataset: PromptDataset = None  # Dataset containing only the new generated artifacts.
    id_to_related_children: Dict[str, Set[str]] = None  # Maps new artifact names to the artifacts in their cluster.
    all_artifacts_dataset: PromptDataset = None  # Dataset containing source and new artifacts.

    """
    Optional Step 7 - generate trace links between source and target artifacts
    """
    trace_predictions: List[EnumDict] = None  # list of traces between source and target artifacts
    selected_predictions: List[EnumDict] = None  # met the criteria required to count as a trace

    """
    Step 8 - Dataset Construction
    """
    final_dataset: PromptDataset = None  # The final dataset with generated artifacts.
