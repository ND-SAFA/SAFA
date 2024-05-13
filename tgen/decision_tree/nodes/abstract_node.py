import abc
from dataclasses import dataclass, field
from typing import Dict, Any

from tgen.common.util.dict_util import DictUtil


@dataclass
class AbstractNode(abc.ABC):
    description: str
    branches: Dict[str, "AbstractNode"] | "AbstractNode" = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Ensures branches is in the correct format.
        :return: None.
        """
        if not isinstance(self.branches, dict):
            self.branches = {"next": self.branches}

    def select_branch(self, choice: str) -> "AbstractNode":
        """
        Returns which path should be selected based on the given reasoning.
        :param choice: The reasoning to decide the next node to go to.
        :return: The selected next node to visit.
        """
        if len(self.branches) > 1:
            return self.branches.get(choice)
        return DictUtil.get_value_by_index(self.branches)

    def is_leaf(self) -> bool:
        """
        Returns whether the given node is a leaf node.
        :return: True if the given node is a leaf node else False.
        """
        return len(self.branches) == 0 or self.branches is None

    @abc.abstractmethod
    def make_choice(self, input_: Any, **kwargs) -> str:
        """
        Decides which path to take from the current node.
        :param input_: The unique input to the node.
        :param kwargs: Any additional arguments needed to make choice.
        :return: The choice of the next branch.
        """
