from langchain_core.documents.base import Document

from common_resources.graph.nodes.retrieve_node import RetrieveNode
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.graph.graph_test_util import get_io_without_data


class TestRetrieveNode(BaseTest):

    def test_perform_action(self):
        queries = ["query1", "query2"]
        arg, state = get_io_without_data(retrieval_query=queries)
        updated_state = RetrieveNode(arg).perform_action(state)
        for query in queries:
            self.assertIn(query, updated_state["documents"])
            self.assertIsInstance(updated_state["documents"][query][0], Document)
