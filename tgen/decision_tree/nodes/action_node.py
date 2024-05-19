from dataclasses import dataclass
from typing import Any, Callable

from tgen.common.util.dataclass_util import required_field
from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.pipeline.pipeline_args import PipelineArgs
from tgen.pipeline.state import State


@dataclass
class ActionNode(AbstractNode):
    action_method: Callable[[PipelineArgs, State], Any] = required_field(field_name="action_method")

    def _make_choice(self, args: PipelineArgs, state: State) -> Any:
        """
        Decides which path to take from the current node.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: The choice of the next branch or the input for the next node.
        """
        return self.action_method(args, state)
