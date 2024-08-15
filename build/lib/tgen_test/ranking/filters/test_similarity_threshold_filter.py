from common_resources.data.objects.trace import Trace
from tgen.testres.base_tests.base_test import BaseTest
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.filters.similarity_threshold_filter import SimilarityThresholdFilter


class TestSimilarityThresholdFilter(BaseTest):

    def test_filter(self):
        sim_matrix = [[0.7, 0.4, 0.6], [0.9, 0.4, 0.7], [0.8, 0.5, 0.3], [0.7, 0.5, 0.4]]
        children = [f"c_{i}" for i in range(len(sim_matrix[0]))]
        parent2traces = {f"p_{i}": [Trace(source=children[j], target=f"p_{i}", score=score) for j, score in enumerate(scores)]
                         for i, scores in enumerate(sim_matrix)}
        result = SimilarityThresholdFilter.filter(parent2traces, children_ids=children, parent_ids=list(parent2traces.keys()))
        for i, (p_id, traces) in enumerate(result.items()):
            scores = RankingUtil.get_scores(traces)
            self.assertGreater(max(scores), 0)
            self.assertEqual(min(scores), 0)

        for i in range(len(sim_matrix[0])):
            traces = [p[i] for p in parent2traces.values()]
            all_scores = [p[i] for p in sim_matrix]
            scores = RankingUtil.get_scores(traces)
            self.assertTrue(min(scores) == 0 or min(scores) == min(all_scores))
            self.assertEqual(max(scores), max(all_scores))
