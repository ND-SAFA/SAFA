from collections.abc import Set
from dataclasses import dataclass, field

from tgen.common.util.base_object import BaseObject


@dataclass
class State(BaseObject):
    """
    Represents a state of an object in time
    """

    completed_steps: set = field(default_factory=set)

    def __post_init__(self):
        """
        Performs any operations after initialization
        :return: None
        """
        if not isinstance(self.completed_steps, Set):
            self.completed_steps = set(self.completed_steps)

    def step_is_complete(self, step_name: str) -> bool:
        """
        Checks whether the step is complete
        :param step_name: The name of the step completed
        :return: True if the step was already completed
        """
        return step_name in self.completed_steps

    def on_step_complete(self, step_name: str) -> None:
        """
        Performs all tasks required after step complete
        :param step_name: The name of the step completed
        :return: None
        """
        self.completed_steps.add(step_name)
        # TODO add saving
