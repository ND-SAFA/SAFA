from dataclasses import dataclass
from typing import Any

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

    def make_choice(self, input_: Any) -> str:
        """
        Here to maintain consistency with other nodes.
        :param input_: Input to the node.
        :return: None (raises exception if called).
        """
        raise Exception("Can't choose a branch from a leaf node")
