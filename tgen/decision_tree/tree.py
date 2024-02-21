import abc
from typing import Any

from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.decision_tree.path import Path


class Tree(abc.ABC):

    def __init__(self, starting_node: AbstractNode):
        """
        Represents the decision tree.
        :param starting_node: The root node of the tree from which all other choices branch off.
        """
        self.starting_node = starting_node

    def traverse(self, input_: Any) -> Path:
        """
        Travels through the decision tree until a leaf node is reached.
        :return: The path taken to the final leaf node.
        """
        path_taken = Path(self.starting_node)
        node = self.starting_node
        while not node.is_leaf():
            choice = node.choose_branch(input_)
            node = path_taken.add_decision(choice)
        return path_taken
