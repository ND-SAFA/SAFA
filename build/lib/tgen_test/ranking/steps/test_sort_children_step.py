from common_resources.data.keys.structure_keys import TraceKeys
from common_resources.tools.constants.model_constants import DEFAULT_TEST_EMBEDDING_MODEL

from tgen.testres.base_tests.base_test import BaseTest
from tgen.tracing.ranking.steps.sort_children_step import SortChildrenStep
from tgen_test.ranking.steps.ranking_pipeline_test import RankingPipelineTest


class TestSortChildrenStep(BaseTest):
    """
    Requirements: https://www.notion.so/nd-safa/sort_children-9ced80762601400a82266080e8e547c9?pvs=4
    """

    def test_accept_pre_ranked_children(self):
        """
        Accepts a set of ranked children
        """
        expected = {"s1": ["t1", "t3", "t2"]}
        args, state = RankingPipelineTest.create_ranking_structures(parent_ids=["s1"],
                                                                    children_ids=["t1", "t2", "t3"],
                                                                    pre_sorted_parent2children=expected)
        step = SortChildrenStep()
        step.run(args, state)
        parent2entries = state.sorted_parent2children
        result = {p: [entry[TraceKeys.SOURCE] for entry in entries] for p, entries in parent2entries.items()}
        self.assertDictEqual(expected, result)

    def test_rank_according_to_supported_algorithm(self):
        """
        Sorts the children according to some supported sorting algorithm.
        """
        before = ["t6", "t3", "t1"]
        after = ["t1", "t3", "t6"]
        parent_id = "s1"
        args, state = RankingPipelineTest.create_ranking_structures(parent_ids=[parent_id],
                                                                    children_ids=before,
                                                                    sorter="transformer",
                                                                    embedding_model_name=DEFAULT_TEST_EMBEDDING_MODEL)
        step = SortChildrenStep()
        step.run(args, state)
        self.assertEqual([entry[TraceKeys.SOURCE] for entry in state.sorted_parent2children[parent_id]], after)
