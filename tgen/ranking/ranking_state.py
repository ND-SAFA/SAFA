import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from tgen.jobs.components.job_result import JobResult
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.state.state import State

DEFAULT_RANKING_GOAL = "# Task\n\n" \
                       "You are a software engineer on a software system. " \
                       "Below is a source query followed by the software artifacts in the system." \
                       "Find and rank artifacts from most to least related to the operation of the source's functionality." \
                       "\n\nSource: "
DEFAULT_RANKING_INSTRUCTIONS = "# Instructions\n" \
                               "Rank the artifacts from most to least related" \
                               " to the fulfillment of the source's functionality. " \
                               "Provide the ranking as comma delimited list of artifact ids where the " \
                               "first element is the most related while the last element is the least. " \
                               "Enclose the list in <links></links>."

DEFAULT_EXPERIMENT_DIR = os.path.expanduser("~/desktop/safa/experiments/rankings")


@dataclass
class RankingState(State):
    # Instructions
    project_path: str = None  # path to original dataset
    experiment_id: str = None  # The UUID of the run on the dataset.

    # Metrics
    map_instructions: Optional[List[Dict]] = field(default=None, repr=False)
    metrics: Optional[Dict] = field(default=None, repr=False)

    # Instructions (optional)
    sorter: str = None  # The name of the sorter to use

    # Reasoning
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
    traced_ids: Optional[List[str]] = field(default=None, repr=False)  # determines label of model responses
    all_target_ids: Optional[List[str]] = field(default=None, repr=False)  # helps find missing artifact ids in model responses
    trace_entries: Optional[List[Dict]] = field(default=None, repr=False)  # determines what links get included in source queries

    # Jobs
    job_result: Optional[JobResult] = None
