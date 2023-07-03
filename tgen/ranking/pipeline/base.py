import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from tgen.jobs.components.job_result import JobResult
from tgen.models.llm.llm_responses import GenerationResponse

DEFAULT_REASONING_GOAL = " # Task\n\n" \
                         "For each artifact, reason whether the artifact is related to the source below and why." \
                         "\n\nSource:"
DEFAULT_REASONING_INSTRUCTIONS = "# Instructions\n\nFor each artifact provide whether you think its related to the source and why. " \
                                 "Enclose your answer in <relation>ID - Reason</relation>"
DEFAULT_RANKING_GOAL = "# Task\n\n" \
                       "You are a software engineer on a software system. You are tasked with linking all related documentation. " \
                       "Below is a source query followed by the software artifacts in the system." \
                       "Find and rank all related artifacts from most to least related to the source.\n\nSource: "
DEFAULT_RANKING_INSTRUCTIONS = "# Instructions\n" \
                               "Rank the artifacts from most to least related" \
                               " to the source's functionality within the context of the system. " \
                               "Provide the ranking as comma delimited list of artifact ids where the " \
                               "first element is the most related the functionality of the source " \
                               "while the last element is the least related. " \
                               "Enclose the list in <links></links>."

DEFAULT_EXPERIMENT_DIR = os.path.expanduser("~/desktop/safa/experiments/rankings")


@dataclass
class RankingStore:
    # Instructions
    project_path: str = None  # path to original dataset
    experiment_id: str = None  # The UUID of the run on the dataset.

    # Metrics
    map_instructions: Optional[List[Dict]] = field(default=None, repr=False)
    metrics: Optional[Dict] = field(default=None, repr=False)

    # Instructions (optional)
    sorter: str = None  # The name of the sorter to use

    # Reasoning
    reasoning_goal: str = DEFAULT_REASONING_GOAL  # The prompt used to rank artifacts.
    reasoning_instructions: str = DEFAULT_REASONING_INSTRUCTIONS
    reasoning_prompts: Optional[List[str]] = field(default=None, repr=False)  # the prompts given to the models
    reasoning_responses: Optional[GenerationResponse] = field(default=None, repr=False)

    # Ranking
    reasoning_prompts2source: Optional[Dict] = field(default_factory=dict)
    ranking_responses: Optional[GenerationResponse] = field(default=None, repr=False)
    ranking_prompts: Optional[List[str]] = field(default=None, repr=False)  # the prompts given to the models
    ranking_goal: str = DEFAULT_RANKING_GOAL
    ranking_instructions: str = DEFAULT_RANKING_INSTRUCTIONS
    processed_ranking_response: Optional[List[List[str]]] = field(default=None, repr=False)
    source2reason: Dict = field(default_factory=dict)

    # IO
    run_path: str = None  # path to predictions on dataset
    export_path: str = None
    experiment: bool = False

    # Project
    artifact_map: Dict = field(default=None, repr=False)  # map of artifact name to body
    parent_ids: Optional[List[str]] = field(default=None, repr=False)  # enumerates order of prompts
    traced_ids: Optional[List[str]] = field(default=None, repr=False)  # determines label of model responses
    all_target_ids: Optional[List[str]] = field(default=None, repr=False)  # helps find missing artifact ids in model responses
    trace_entries: Optional[List[Dict]] = field(default=None, repr=False)  # determines what links get included in source queries

    # Models
    parent2children: Dict = field(default_factory=dict)

    # Jobs
    job_result: Optional[JobResult] = None
