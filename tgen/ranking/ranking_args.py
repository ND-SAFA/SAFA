from dataclasses import dataclass
from typing import Dict, List, Optional

from tgen.constants.tgen_constants import DEFAULT_MAX_N_CHILDREN
from tgen.state.pipeline.pipeline_args import PipelineArgs


@dataclass
class RankingArgs(PipelineArgs):
    """
    Path to export various checkpoints
    """
    export_dir: str
    """
    Maps artifact ids to content.
    """
    artifact_map: Dict
    """
    List of parent artifact ids.
    """
    parent_ids: List[str]
    """
    Optional.List of children ids to compare to each parent.
    """
    children_ids: Optional[List[str]] = None
    """
    Maps parent ids to their children ids.
    """
    parent2children: Optional[Dict[str, List[str]]] = None
    """
    The number of maximum children to give to claude
    """
    n_max_children: int = DEFAULT_MAX_N_CHILDREN
    """
    The sorting algorithm to use before ranking with claude
    """
    sorter: str = None
    """
    Whether to load previous responses.
    """
    load_response: bool = False
    """
    The maximum number of tokens to use for summarizing project
    """
    n_summary_tokens = 5000
    """
    The maximum number of tokens per source artifacts.
    """
    n_completion_tokens = 5000
