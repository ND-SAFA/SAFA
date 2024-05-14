import abc
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Callable

from tgen.common.util.dict_util import DictUtil
from tgen.pipeline.pipeline_args import PipelineArgs
from tgen.pipeline.state import State


@dataclass
class AbstractNode(abc.ABC):
    description: str
    branches: Dict[str, "AbstractNode"] | "AbstractNode" = field(default_factory=dict)
    state_setter: Callable[[str, State], None] | str = None
    node_id: str = field(default_factory=uuid.uuid4)

    def __post_init__(self) -> None:
        """
        Ensures branches is in the correct format.
        :return: None.
        """
        if not isinstance(self.branches, dict):
            self.branches = {"next": self.branches}

    def select_branch(self, choice: Any) -> "AbstractNode":
        """
        Returns which path should be selected based on the given reasoning.
        :param choice: The reasoning to decide the next node to go to.
        :return: The selected next node to visit.
        """
        if len(self.branches) > 1:
            if isinstance(choice, list):
                choice = choice[0]
            return self.branches.get(choice)
        return DictUtil.get_value_by_index(self.branches)

    def is_leaf(self) -> bool:
        """
        Returns whether the given node is a leaf node.
        :return: True if the given node is a leaf node else False.
        """
        return len(self.branches) == 0 or self.branches is None

    @abc.abstractmethod
    def make_choice(self, args: PipelineArgs, state: State) -> Any:
        """
        Decides which path to take from the current node.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: The choice of the next branch or the input for the next node.
        """
