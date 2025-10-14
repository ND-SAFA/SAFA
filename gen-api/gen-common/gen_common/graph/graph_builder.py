from copy import deepcopy
from typing import Any, Callable, Tuple, Type

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.state import StateGraph

from gen_common.graph.branches.supported_branches import SupportedBranches
from gen_common.graph.edge import Edge, PathMapType
from gen_common.graph.graph_definition import GraphDefinition
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.nodes.abstract_node import AbstractNode
from gen_common.graph.nodes.supported_nodes import SupportedNodes
from gen_common.util.param_specs import ParamSpecs
from gen_common.util.reflection_util import ReflectionUtil
from gen_common.util.supported_enum import SupportedEnum


class GraphBuilder:

    def __init__(self, graph_definition: GraphDefinition, graph_args: GraphArgs):
        """
        Responsible for constructing the graph.
        :param graph_definition: Contains all nodes and edges in the graph.
        :param graph_args: Starting args to the graph.
        """
        self.graph_args = graph_args
        self.graph_definition = graph_definition
        self.nodes_in_graph = set(self.graph_definition.nodes + [SupportedNodes.END_COMMAND])
        self.node_map = {}

    def build(self) -> CompiledGraph:
        """
        Builds and compiles the graph.
        :return: Compiled graph.
        """
        graph = StateGraph(self.graph_definition.state_type)
        self.add_nodes(graph)
        self.add_edges(graph)
        graph.set_entry_point(self.graph_definition.get_root_node().name)
        return graph.compile(checkpointer=MemorySaver())

    def add_nodes(self, graph: StateGraph) -> None:
        """
        Adds nodes to the graph.
        :param graph: The graph to add nodes to.
        :return: None.
        """
        for node in self.graph_definition.nodes:
            graph.add_node(node.name, self.get_node_representation(node, return_type=AbstractNode))

    def add_edges(self, graph: StateGraph) -> None:
        """
        Adds edges to the graph.
        :param graph: THe graph to add edges to.
        :return: None.
        """
        for edge in self.graph_definition.edges:
            start, end = self.assert_valid_edge(edge)

            if edge.is_conditional_edge():
                path_map = self.get_path_map(edge)
                path_map = {self.assert_valid_node(k, allow_by_default=True):
                                self.assert_valid_node(v) for k, v in path_map.items()}
                graph.add_conditional_edges(start, end, path_map)
            else:
                graph.add_edge(start, end)

    def get_path_map(self, edge: Edge) -> PathMapType:
        """
        Gets the mapping between branch output and the next node to go to based on that output.
        :param edge: The edge to get the path map for.
        :return: The mapping between branch output and the next node to go to based on that output.
        """
        path_map = deepcopy(edge.path_map)
        if isinstance(edge.end, SupportedBranches) and path_map is None:
            path_map = edge.end.value(self.graph_args).get_node_choices()
        if path_map and not isinstance(path_map, dict):
            path_map = {n: n for n in path_map}
        return path_map

    def get_node_instance(self, node: SupportedEnum) -> AbstractNode:
        """
        Gets the instantiated node.
        :param node: The node enum containing name + class.
        :return: The instantiated node.
        """
        if node.name not in self.node_map:
            value = node.value
            if ReflectionUtil.is_instance_or_subclass(value, AbstractNode):
                params = ParamSpecs.create_from_method(value.__init__).get_accepted_params(self.graph_definition.node_args)
                value = value(self.graph_args, **params)
            self.node_map[node.name] = value
        return self.node_map[node.name]

    def assert_valid_edge(self, edge: Edge) -> Tuple[str, str]:
        """
        Asserts that both nodes in the edge exist in the graph.
        :param edge: The edge to evaluate.
        :return: The start and end node names.
        """
        start = self.assert_valid_node(edge.start)
        return_type = AbstractNode if edge.is_conditional_edge() else str
        end = self.assert_valid_node(edge.end, allow_by_default=edge.is_conditional_edge(), return_type=return_type)
        return start, end

    def assert_valid_node(self, node: SupportedNodes | str | Callable, allow_by_default: bool = False,
                          return_type: Type = str) -> str:
        """
        Asserts node exists in the graph.
        :param node: The node.
        :param allow_by_default: If True, node can be a  string/callable and will be accepted as valid automatically.
        :param return_type: The type to use to represent the node.
        :return: The node name.
        """
        assert allow_by_default or node in self.nodes_in_graph, f"Unknown node in edge: {node}"

        return self.get_node_representation(node, return_type)

    def get_node_representation(self, node: SupportedEnum | Any, return_type: Type) -> AbstractNode | str | Any:
        """
        Gets the expected representation of the node (node object, name of the name, etc).
        :param node: The node enum.
        :param return_type: The type to use to represent the node.
        :return: The expected representation of the node (node object, name of the name, etc)
        """
        if isinstance(node, SupportedEnum):
            if issubclass(return_type, AbstractNode):
                assert isinstance(node, SupportedEnum), f"Unexpected node type {type(node)}"
                return self.get_node_instance(node)
            elif issubclass(return_type, str):
                return node.name
        return node
