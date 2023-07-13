import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from tgen.models.llm.llm_responses import GenerationResponse
from tgen.state.state import State

DEFAULT_RANKING_GOAL = "# Task\n\n" \
                       "You are a software engineer on a software project described under `# Software Specification`. " \
                       "You are tasked with finding the children of the parent artifact." \
                       "\n\nParent Artifact: "
DEFAULT_RANKING_INSTRUCTIONS = "# Instructions\n" \
                               "1. Describe the behavior of the parent relative to its role in the system. " \
                               "Enclose your answer in <context></context>." \
                               "\n2. Find the software artifacts that help implement the parent's behavior." \
                               "Provide the list of artifacts and a description of their relation to the parent. " \
                               "Enclose your answer in <related></related>." \
                               "\n3. Rank the relevant artifacts from most to least related to " \
                               "the implementation of the parent's behavior." \
                               "Provide the ranking as comma delimited list of artifact ids where the " \
                               "first element is the most related while the last element is the least. " \
                               "Enclose the list in <links></links>."

DEFAULT_EXPERIMENT_DIR = os.path.expanduser("~/desktop/safa/experiments/rankings")


@dataclass
class RankingState(State):
    # Summarizing
    project_summary: str = None
    # sorting
    sorted_parent2children: Optional[Dict[str, List[str]]] = None

    # Ranking
    ranking_responses: Optional[GenerationResponse] = field(default=None, repr=False)
    ranking_prompts: Optional[List[str]] = field(default=None, repr=False)  # the prompts given to the models
    ranking_goal: str = DEFAULT_RANKING_GOAL
    ranking_instructions: str = DEFAULT_RANKING_INSTRUCTIONS
    processed_ranking_response: Optional[List[List[str]]] = field(default=None, repr=False)

    # IO
    export_path: str = None
