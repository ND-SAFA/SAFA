from dataclasses import dataclass
from typing import Any, Callable

from tgen.common.util.dataclass_util import required_field
from tgen.decision_tree.abstract_node import AbstractNode


@dataclass
class ConditionalNode(AbstractNode):
    conditional_statement: Callable = required_field(field_name="conditional_statement")

    def choose_branch(self, input_: Any) -> str:
        """
        Decides which path to take from the current node.
        :param input_: The unique input to the node.
        :return: The choice of the next branch.
        """
        choice = self.conditional_statement(input_)
        return choice
