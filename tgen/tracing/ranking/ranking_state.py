import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.override import overrides
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
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
    prompt_builder: Optional[PromptBuilder] = field(default=None, repr=False)
    ranking_responses: Optional[GenerationResponse] = field(default=None, repr=False)
    children_entries: List[Dict] = field(default=None, repr=False)

    # IO
    export_path: str = None

    @overrides(State)
    def save(self, step_name: str, run_num: int = 1, attrs2ignore: Set = None) -> bool:
        """
        Saves the current state
        :param step_name: The step name that the pipeline is currently at
        :param run_num: The number of times the step has been run
        :param attrs2ignore: The attributes to ignore when saving
        :return: True if saved successfully else False
        """
        if not attrs2ignore:
            attrs2ignore = set()
        attrs2ignore.add("prompt_builder")
        return super().save(step_name=step_name, run_num=run_num, attrs2ignore=attrs2ignore)

