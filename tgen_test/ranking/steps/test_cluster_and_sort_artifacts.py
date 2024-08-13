from tgen_test.ranking.steps.ranking_pipeline_test import RankingPipelineTest
from common_resources.data.keys.structure_keys import TraceKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.tracing.ranking.steps.cluster_and_sort_artifacts_step import ClusterAndSortArtifactsStep


class TestClusterAndSortArtifacts(BaseTest):

    def test_run(self):
        args, state = RankingPipelineTest.create_ranking_structures()
        ClusterAndSortArtifactsStep().run(args, state)
        for parent, traces in state.sorted_parent2children.items():
            self.assertSize(3, traces)
            parent_number = parent[-1]
            self.assertEqual(f"s{parent_number}", traces[0][TraceKeys.SOURCE])
