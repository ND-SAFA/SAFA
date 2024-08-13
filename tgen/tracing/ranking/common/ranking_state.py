import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from tgen.common.objects.trace import Trace
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.state_management.state import State

DEFAULT_EXPERIMENT_DIR = os.path.expanduser("~/desktop/safa/experiments/rankings")


@dataclass
class RankingState(State):
    artifact_map: Dict[str, str] = None

    # sorting
    sorted_parent2children: Optional[Dict[str, List[EnumDict]]] = None

    # filtering
    filtered_parent2children: Optional[Dict[str, List[EnumDict]]] = None

    # composite (for chunks)
    composite_parent2children: Optional[Dict[str, List[EnumDict]]] = None

    # Ranking
    ranking_responses: List[List[Dict]] = field(default=None, repr=False)

    # Entries
    candidate_entries: List[Union[Trace, EnumDict]] = field(default=None, repr=False)
    selected_entries: List[Union[Trace, EnumDict]] = field(default=None, repr=False)  # filtered entries based on score

    # IO
    export_path: str = None

    def get_current_parent2children(self) -> Dict[str, List[EnumDict]]:
        """
        Gets the latest parent version of the parent2children.
        :return: Dictionary mapping parent id to a list of the traces related to that parent.
        """
        last2first = [self.composite_parent2children, self.filtered_parent2children, self.sorted_parent2children]
        for parent2children in last2first:
            if parent2children:
                return parent2children

    def get_current_entries(self) -> Optional[List[Dict]]:
        """
        Gets the current children entries
        :return: The current children entries
        """
        if self.selected_entries:
            return self.selected_entries
        elif self.candidate_entries:
            return self.candidate_entries
        elif self.get_current_parent2children():
            self.candidate_entries = [entry for entries in self.get_current_parent2children().values() for entry in entries]
            return self.candidate_entries
        else:
            raise Exception(
                "Could not identify the current entries from `selected_entries`, `candidate_entries`, `sorted_parent2children`.")
