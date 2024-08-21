from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Type

from gen_common.graph.branches.paths.path_selector import PathSelector
from gen_common.graph.edge import Edge
from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.nodes.supported_nodes import SupportedNodes


@dataclass(frozen=True)
class GraphDefinition:
    nodes: List[SupportedNodes]
    edges: List[Edge]
    state_type: Type[GraphState]
    root: SupportedNodes = None
    node_args: Dict = field(default_factory=dict)
    output_converter: Callable[[GraphState], Any] | PathSelector = None

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
