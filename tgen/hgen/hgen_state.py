from dataclasses import dataclass
from typing import Union, List, Dict, Any

from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.state.state import State
from tgen.summarizer.summary import Summary


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
    Optional Step - Break project into parts and generate for each part
    """
    id_to_cluster_artifacts: Dict[Any, List[EnumDict]] = None  # maps cluster id to the list of artifacts in that cluster
    cluster_dataset: PromptDataset = None  # contains all the clusters and their links to the artifacts

    """
    Step 3 - Artifact generation
    """
    generation_predictions: Dict[str, List[str]] = None  # dictionary mapping generated content to a list of related source ids
    n_generations: int = 0  # number of runs of artifact generation

    """
    Optional Step - Refine content on rerun of hgen
    """
    all_generated_content: Dict[str, List[str]] = None  # All generated content across all runs
    refined_content: Dict[str, List[str]] = None  # The final selected artifact content

    """
    Step 4 - Dataset Construction
    """
    new_artifact_df: ArtifactDataFrame = None  # Contains the new generated artifacts
    final_dataset: PromptDataset = None  # The final dataset with generated artifacts.
