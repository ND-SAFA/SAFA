from dataclasses import dataclass
from typing import Any, Callable

from gen_common.pipeline.args import Args
from gen_common.pipeline.state import State
from gen_common.util.dataclass_util import required_field

from gen.chat.decision_tree.nodes.abstract_node import AbstractNode


@dataclass
class ActionNode(AbstractNode):
    action_method: Callable[[Args, State], Any] = required_field(field_name="action_method")

    def _make_choice(self, args: Args, state: State) -> Any:
        """
        Decides which path to take from the current node.
        :param args: The arguments to the node.
        :param state: The current state.
        :return: The choice of the next branch or the input for the next node.
        """
        return self.action_method(args, state)
