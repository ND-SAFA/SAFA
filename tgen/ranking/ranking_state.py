import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from tgen.models.llm.llm_responses import GenerationResponse
from tgen.state.state import State

DEFAULT_RANKING_GOAL = "# Task\n\n" \
                       "Below is a project you created. " \
                       "You task is to find the children of each in the system parent artifact." \
                       "This task is separated so that you are focusing on a single parent at a time. " \
                       "Below is the parent software artifact and a list of potential children." \
                       "\n\n"
DEFAULT_RANKING_INSTRUCTIONS = "# Instructions\n" \
                               "1. Concisely describe the functionality of the parent within the context of the system. " \
                               "Describe the system functionality that lies directly within the responsibility of the parent." \
                               "Enclose your answer in <function></function>" \
                               "\n2. List the children who lie directly within the scope of parent's functionality." \
                               "Provide the list of children artifacts along with a sentence describing how it " \
                               "helps the parent achieve its functionality. " \
                               "Put each entry on different lines and follow the format: ID - DESCRIPTION. " \
                               "Enclose your answer in <related></related>." \
                               "\n3. Rank all the artifacts from most to least related to the parent's functionality. " \
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
    ranked_children: Optional[List[List[str]]] = field(default=None, repr=False)
    ranked_children_explanations: Optional[List[List[str]]] = field(default=None, repr=False)

    # IO
    export_path: str = None
