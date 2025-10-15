import abc
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict

from gen_common.pipeline.args import Args
from gen_common.pipeline.state import State

DEFAULT_BRANCH = str(uuid.uuid4())


@dataclass
class AbstractNode(abc.ABC):
    description: str
    branches: Dict[str, "AbstractNode"] | "AbstractNode" = field(default_factory=dict)
    state_setter: Callable[[str, State], None] | str = None  # either a callable to set the state or the name of the state var to set
    node_id: str = field(default_factory=uuid.uuid4)
    default_choice: str = None
    skip: bool = False  # if True, will skip running this node and go to the default choice next

    def __post_init__(self) -> None:
        """
        Ensures branches is in the correct format.
        :return: None.
        """
        if not isinstance(self.branches, dict):
            self.branches = {DEFAULT_BRANCH: self.branches}

        if not self.next_branch_depends_on_choice():
            self.default_choice = DEFAULT_BRANCH if not self.default_choice else self.default_choice

        if self.skip:
            self.skip_node()

    def select_branch(self, choice: Any = DEFAULT_BRANCH) -> "AbstractNode":
        """
        Returns which path should be selected based on the given reasoning.
        :param choice: The reasoning to decide the next node to go to.
        :return: The selected next node to visit.
        """
        default_branch = None if self.default_choice is None else self.branches.get(self.default_choice)
        if not self.next_branch_depends_on_choice():
            return default_branch

        if isinstance(choice, list):
            choice = choice[0]
        selected = self.branches.get(choice, default_branch)
        return selected

    def is_leaf(self) -> bool:
        """
        Returns whether the given node is a leaf node.
        :return: True if the given node is a leaf node else False.
        """
        return len(self.branches) == 0 or self.branches is None

    def make_choice(self, args: Args, state: State) -> Any:
        """
        Decides which path to take from the current node.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: The choice of the next branch or the input for the next node.
        """
        if self.skip:
            return DEFAULT_BRANCH
        return self._make_choice(args, state)

    def next_branch_depends_on_choice(self) -> bool:
        """
        True if the node has only more than one choice for the next node.
        :return: True if the node has only more than one choice for the next node else False.
        """
        return len(self.branches) > 1

    def skip_node(self) -> None:
        """
        Sets the node to be skipped.
        :return: None.
        """
        self.skip = True
        assert self.default_choice is not None, "Must provide a default branch to skip node."

    @abc.abstractmethod
    def _make_choice(self, args: Args, state: State) -> Any:
        """
        Decides which path to take from the current node.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: The choice of the next branch or the input for the next node.
        """
