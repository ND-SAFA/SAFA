from dataclasses import dataclass, field
from typing import List, Optional, Any

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.logging.logger_manager import logger
from tgen.common.util.list_util import ListUtil
from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.pipeline.state import State


@dataclass
class Path:
    starting_node: AbstractNode
    args: Any
    state: State
    __choices: List[str] = field(default_factory=list, init=False)
    __path_taken: List[AbstractNode] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        """
        Performs post initialization tasks on the Path.
        :return: None
        """
        self.__path_taken.append(self.starting_node)

    def get_choice(self, chosen_node_index: int = -1) -> str:
        """
        Gets a choice for the chosen node at the given index.
        :param chosen_node_index: The index of the node that resulted from the desired choice.
        :return: The
        """
        chosen_node_index = chosen_node_index - 1 if chosen_node_index != -1 else chosen_node_index
        return ListUtil.safely_get_item(chosen_node_index, self.__choices)

    def get_node(self, node_index: int = -1) -> AbstractNode:
        """
        Gets a node in the tree (by default is the last).
        :param node_index: The index of the node.
        :return: The node that was decided upon at the given index.
        """
        return ListUtil.safely_get_item(node_index, self.__path_taken)

    def get_nodes(self) -> List[AbstractNode]:
        """
        Gets all nodes in the tree.
        :return: All nodes in the tree.
        """
        return self.__path_taken

    def add_decision(self, choice: str) -> AbstractNode:
        """
        Adds a new decision on which branch of the tree to explore next.
        :param choice: The reason that branch was chosen.
        :return: The node chosen to explore next.
        """
        current_node = self.get_node()
        next_selected_node = current_node.select_branch(choice)
        logger.log_with_title(title="Finished traversing next node",
                              message=f"Node: {current_node.description}{NEW_LINE}Choice: " + "%.200s" % choice)
        if current_node.state_setter:
            if isinstance(current_node.state_setter, str):
                setattr(self.state, current_node.state_setter, choice)
            else:
                current_node.state_setter(choice, self.state)
        if next_selected_node:
            self.__path_taken.append(next_selected_node)
        self.__choices.append(choice)
        return next_selected_node

    def get_final_decision(self) -> Optional[str]:
        """
        Gets the description of the final node at the end of the path.
        :return: The description of the final node at the end of the path.
        """
        last_node = self.get_node(-1)
        if last_node.is_leaf():
            return last_node.description

    def __len__(self) -> int:
        """
        Returns the depth of the path.
        :return: The depth of the path.
        """
        return len(self.__path_taken)
