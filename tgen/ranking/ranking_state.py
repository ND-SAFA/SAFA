import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from tgen.models.llm.llm_responses import GenerationResponse
from tgen.state.state import State

DEFAULT_RANKING_GOAL = "# Task\n\n" \
                       "You are a software engineer on a software project. " \
                       "You are given a parent software artifact and a list of potential children. " \
                       "You task is to find the children that help implement or refine the parent functionality." \
                       "The children are sorted from most to least matching words with the parent. " \
                       "Consider the top entries of this list." \
                       "\n\n"
DEFAULT_RANKING_INSTRUCTIONS = "# Instructions\n" \
                               "1. Provide a concise 3 word title describing the unique functionality this parent provides to the overall system. " \
                               "Let this be the `value prop`. " \
                               "Enclose your answer in <function></function>" \
                               "\n2. Select the artifacts from related to the parent's value prop. " \
                               "Provide the list of artifacts along with a sentence of how they help the parent achieve" \
                               "the shared functionality. " \
                               "Put each entry on different lines and follow the format: ID - RELATIONSHIP. " \
                               "Enclose your answer in <related></related>." \
                               "\n3. Rank the artifacts by the order in which they provide value to the parent, from most to least. " \
                               "Provide the ranking as comma delimited list of artifact ids. " \
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
    ranked_children: Optional[List[List[str]]] = field(default=None, repr=False)
    ranked_children_explanations: Optional[List[List[str]]] = field(default=None, repr=False)

    # IO
    export_path: str = None
