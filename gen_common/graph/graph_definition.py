from dataclasses import dataclass
from typing import List, Type

from gen_common.graph.edge import Edge
from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.nodes.supported_nodes import SupportedNodes


@dataclass(frozen=True)
class GraphDefinition:
    nodes: List[SupportedNodes]
    edges: List[Edge]
    state_type: Type[GraphState]
    root: SupportedNodes = None

    def __post_init__(self):
        """
        Runs additional processing after initializing
        """
        assert len(self.nodes) >= 1, "Must provide at least one node to create a graph"

    def get_root_node(self) -> SupportedNodes:
        """
        Gets the starting node of the graph.
        :return: The starting node of the graph.
        """
        return self.root if self.root is not None else self.nodes[0]
