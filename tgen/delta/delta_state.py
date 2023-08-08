from dataclasses import dataclass

from tgen.state.state import State


@dataclass
class DeltaState(State):
    project_summary: str = None  # The summary of the project
