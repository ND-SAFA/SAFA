import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.state.state import State

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

    ranked_children: Optional[List[List[str]]] = field(default=None, repr=False)
    ranked_children_explanations: Optional[List[List[str]]] = field(default=None, repr=False)

    # IO
    export_path: str = None

    # Prompt building and parsing
    prompt_builder: PromptBuilder = None
