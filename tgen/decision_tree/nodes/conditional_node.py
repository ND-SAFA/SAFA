from dataclasses import dataclass
from typing import Any, Callable

from tgen.common.util.dataclass_util import required_field
from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.pipeline.pipeline_args import PipelineArgs
from tgen.pipeline.state import State


@dataclass
class ConditionalNode(AbstractNode):
    conditional_statement: Callable[[PipelineArgs, State], Any] = required_field(field_name="conditional_statement")

    def _make_choice(self, args: PipelineArgs, state: State) -> Any:
        """
        Decides which path to take from the current node.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: The choice of the next branch or the input for the next node.
        """
        choice = self.conditional_statement(args, state)
        return choice
