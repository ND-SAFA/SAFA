from test.ranking.steps.ranking_pipeline_util import RankingPipelineTest
from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.ranking.steps.sort_children_step import SortChildren
from tgen.testres.base_tests.base_test import BaseTest


class TestSortChildrenStep(BaseTest):
    """
    Requirements: https://www.notion.so/nd-safa/sort_children-9ced80762601400a82266080e8e547c9?pvs=4
    """

    def test_accept_pre_ranked_children(self):
        """
        Accepts a set of ranked children
        """
        pre_ranked = {}
        args, state = RankingPipelineTest.create_ranking_structures(sorter=None, parent2children=pre_ranked)
        step = SortChildren()
        step.run(args, state)
        self.assertEqual(state.sorted_parent2children, pre_ranked)

    def test_rank_according_to_supported_algorithm(self):
        """
        Sorts the children according to some supported sorting algorithm.
        """
        before = ["t6", "t3", "t1"]
        after = ["t1", "t3", "t6"]
        parent_id = "s1"
        args, state = RankingPipelineTest.create_ranking_structures(parent_ids=[parent_id],
                                                                    children_ids=before,
                                                                    sorter="embedding",
                                                                    embedding_model=SMALL_EMBEDDING_MODEL)
        step = SortChildren()
        step.run(args, state)
        self.assertEqual(state.sorted_parent2children[parent_id], after)

    def test_denies_request_if_both_defined(self):
        """
        Denies request if both pre-ranked children and sorting algorithm are defined. This prevents mistakes.
        """
        args, state = RankingPipelineTest.create_ranking_structures(parent2children={}, sorter="embedding")
        step = SortChildren()
        self.assert_error(lambda: step.run(args, state), AssertionError, "sorter or parent2children")
