from typing import List

from langgraph.constants import START

from common_resources.graph.branches.supported_branches import SupportedBranches
from common_resources.graph.edge import Edge
from common_resources.graph.graph_builder import GraphBuilder

from common_resources.graph.graph_definition import GraphDefinition
from common_resources.graph.io.graph_state import GraphState
from common_resources.graph.nodes.supported_nodes import SupportedNodes
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.graph.graph_test_util import get_io_without_data


class TestGraphBuilder(BaseTest):

    def test_build(self):
        builder = self.get_builder()
        graph = builder.build().get_graph()
        for node in builder.graph_definition.nodes:
            self.assertIn(node.name, graph.nodes)
        all_edges = {(edge.source, edge.target) for edge in graph.edges}
        for edge in builder.graph_definition.edges:
            if not edge.is_conditional_edge():
                self.assertIn((edge.start.name, edge.end.name), all_edges)
            else:
                path_map = builder.get_path_map(edge)
                for node_name, node_value in path_map.items():
                    self.assertIn((edge.start.name, node_value.name), all_edges)
        self.assertIn((START, builder.graph_definition.get_root_node().name), all_edges)

    def test_build_failure(self):
        builder = self.get_builder(additional_edges=[Edge(SupportedNodes.CONTINUE, "unknown node")])
        try:
            builder.build()
            self.fail("Should fail because of unknown node")
        except AssertionError as e:
            self.assertIn("Unknown node", e.args[0])

    def get_builder(self, additional_edges: List = None):
        additional_edges = [] if not additional_edges else additional_edges
        args, state = get_io_without_data()
        builder = GraphBuilder(
            GraphDefinition(
                nodes=[
                    SupportedNodes.GENERATE,
                    SupportedNodes.RETRIEVE,
                    SupportedNodes.CONTINUE,
                    SupportedNodes.EXPLORE_NEIGHBORS
                ],
                edges=[
                          Edge(SupportedNodes.GENERATE, SupportedBranches.DECIDE_NEXT),
                          Edge(SupportedNodes.CONTINUE, SupportedBranches.GRADE_GENERATION),
                          Edge(SupportedNodes.RETRIEVE, SupportedNodes.GENERATE),
                          Edge(SupportedNodes.EXPLORE_NEIGHBORS, SupportedNodes.GENERATE)] + additional_edges,
                state_type=GraphState),
            graph_args=args)
        return builder
