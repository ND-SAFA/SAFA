from typing import Dict, Callable, Set

from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.decision_tree.tree import Tree


class TreeBuilder:

    def __init__(self, root_node_id: str, node_constructor_map: Dict[str, Callable[[], AbstractNode]], nodes2skip: Set[str] = None):
        """
        Responsible for constructing decision trees.
        :param root_node_id: The id of the root (starting) node.
        :param node_constructor_map: Dictionary mapping node id to the method used to construct it.
        :param nodes2skip: Set of node ids that should be skipped.
        """
        self.built_nodes = {}
        self.node_constructor_map = node_constructor_map
        self.root_node_id = root_node_id
        self.nodes2skip = nodes2skip if nodes2skip else set()

    def build_tree(self) -> Tree:
        """
        Builds the tree.
        :return: The decision tree.
        """
        return Tree(self.get_node(self.root_node_id))

    def get_node(self, node_id: str) -> AbstractNode:
        """
        Gets the pre-requisite node needed to build current node.
        :param node_id: The id of the pre-requisite node.
        :return: The pre-requisite node needed to build current node.
        """
        if node_id not in self.built_nodes:
            assert node_id in self.node_constructor_map, f"Please register {node_id} in constructor map to build tree."
            node: AbstractNode = self.node_constructor_map[node_id]()
            if node_id in self.nodes2skip:
                node.skip_node()
            self.built_nodes[node_id] = node
        return self.built_nodes[node_id]
