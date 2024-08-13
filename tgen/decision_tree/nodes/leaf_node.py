from dataclasses import dataclass
from typing import Any

from common_resources.tools.state_management.args import Args
from common_resources.tools.state_management.state import State

from tgen.decision_tree.nodes.abstract_node import AbstractNode


@dataclass
class LeafNode(AbstractNode):

    def __post_init__(self):
        """
        Checks that this is indeed a leaf node.
        :return: None
        """
        if not self.is_leaf():
            raise Exception("Leaf node cannot have branches.")

    def _make_choice(self, args: Args, state: State) -> Any:
        """
        Here for node api, should not be used for leaf.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: The choice of the next branch or the input for the next node.
        """
        raise Exception("Can't choose a branch from a leaf node")
