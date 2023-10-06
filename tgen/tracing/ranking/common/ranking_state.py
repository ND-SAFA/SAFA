import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.override import overrides
from tgen.common.objects.trace import Trace
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.state.state import State

DEFAULT_EXPERIMENT_DIR = os.path.expanduser("~/desktop/safa/experiments/rankings")


@dataclass
class RankingState(State):
    # Summarizing
    project_summary: str = None
    # sorting
    sorted_parent2children: Optional[Dict[str, List[EnumDict]]] = None

    # Ranking
    ranking_responses: List[Dict] = field(default=None, repr=False)
    children_entries: List[Dict] = field(default=None, repr=False)
    selected_entries: List[Dict] = field(default=None, repr=False)  # filtered entries based on score

    # IO
    export_path: str = None
