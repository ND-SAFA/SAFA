import abc
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AbstractNode(abc.ABC):
    description: str
    branches: Dict[str, "AbstractNode"] = field(default_factory=dict)

    def select_branch(self, choice: str) -> "AbstractNode":
        """
        Returns which path should be selected based on the given reasoning.
        :param choice: The reasoning to decide the next node to go to.
        :return: The selected next node to visit.
        """
        return self.branches.get(choice)

    def is_leaf(self) -> bool:
        """
        Returns whether the given node is a leaf node.
        :return: True if the given node is a leaf node else False.
        """
        return len(self.branches) == 0 or self.branches is None

    @abc.abstractmethod
    def choose_branch(self, input_: Any) -> str:
        """
        Decides which path to take from the current node.
        :param input_: The unique input to the node.
        :return: The choice of the next branch.
        """
