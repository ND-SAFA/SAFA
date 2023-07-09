from dataclasses import dataclass
from typing import Dict, List

from tgen.pipeline.pipeline_state import PipelineArgs


@dataclass
class RankingArgs(PipelineArgs):
    """
    Maps artifact ids to content.
    """
    artifact_map: Dict  # map of artifact name to body
    """
    List of parent artifact ids.
    """
    parent_ids: List[str]  # enumerates order of prompts
    """
    Maps parent ids to their children ids.
    """
    parent2children: Dict  # Map parent ids to children ids.
