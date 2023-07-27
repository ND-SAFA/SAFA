import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from tgen.models.llm.llm_responses import GenerationResponse
from tgen.state.state import State

DEFAULT_RANKING_GOAL = "# Task\n\n" \
                       "Below is a set of software artifacts of a project. You are the expert on this project. " \
                       "You are performing traceability by finding the children associated with a given parent artifact. " \
                       "You are focusing on a single parent artifact. " \
                       "Enclosed in <parent-artifact><parent-artifact> the parent artifact followed by " \
                       "description of the project and then by the list of potential children (formatted in XML)." \
                       "\n\n"
DEFAULT_RANKING_INSTRUCTIONS = "# Instructions\n" \
                               "1. Provide 2-3 sentences describing the job of the parent artifact. " \
                               "Include its responsibilities, its dependencies, and its purpose in the system. " \
                               "Enclose your answer in <function></function>" \
                               "\n2. Read each potential child artifact in order. " \
                               "Decide whether the artifact impacts, implements, or refines the parent artifact functionality. " \
                               "Format your answer as: ID - Yes/No. Enclose your answer in <classification></classification>." \
                               "\n3. For each selected artifact, " \
                               "provide a sentence describing how its role in the system helps the parent artifact achieve its job. " \
                               "Put each entry on different lines and follow the format: ID - DESCRIPTION. " \
                               "Work through one artifact at a time so that the IDs are in ascending order. " \
                               "Enclose your answer in <related></related>." \
                               "\n3. Rank the children by proximity to the parent artifact functionality." \
                               "Provide a comma delimited list of artifact ids where the " \
                               "first element is the most similar to the parent artifact while the last element is the least. " \
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
