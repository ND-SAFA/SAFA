from test.ranking.steps.ranking_pipeline_test import PARENT_ID, CHILD_ID, RankingPipelineTest
from tgen.common.constants.ranking_constants import RANKING_MAX_SCORE, RANKING_MIN_SCORE
from tgen.common.util.math_util import MathUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_responses import MockResponses
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.llm_ranking_pipeline import LLMRankingPipeline


class TestLLMRankingPipeline(BaseTest):
    """
    Tests the requirements: https://www.notion.so/nd-safa/llm_ranking_pipeline-b9c4607d47f44c739fc2ebf623fa8dcc?pvs=4
    """

    @mock_anthropic
    def test_prediction_construction(self, ai_manager: TestAIManager):
        """
        Tests that pipeline correctly constructs the ranked predictions.
        """
        ai_manager.mock_summarization()
        ai_manager.set_responses(MockResponses.project_summary_responses +
                                 [RankingPipelineTest.get_response()])
        args = self.create_args()
        pipeline = LLMRankingPipeline(args)
        pipeline.run()
        prediction_entries = pipeline.state.selected_entries
        self.assertEqual(1, len(prediction_entries))
        entry = prediction_entries[0]
        self.assertEqual(CHILD_ID, entry[TraceKeys.SOURCE.value])
        self.assertEqual(PARENT_ID, entry[TraceKeys.TARGET.value])
        for tag in RankingPipelineTest.get_explanation_tags():
            self.assertIn(tag, entry[TraceKeys.EXPLANATION.value].lower())
        expected_score = MathUtil.normalize_val(4.0, max_val=RANKING_MAX_SCORE, min_val=RANKING_MIN_SCORE)
        self.assertEqual(expected_score, entry[TraceKeys.SCORE.value])

    @staticmethod
    def create_args() -> RankingArgs:
        """
        Creates ranking arguments for pipeline.
        """
        parent_type = "parent_type"
        child_type = "child_type"
        parent_artifact = {"id": PARENT_ID, "content": "content_1", "layer_id": parent_type}
        child_artifact = {"id": CHILD_ID, "content": "content_2", "layer_id": child_type}
        parent_ids = [PARENT_ID]
        children_ids = [CHILD_ID]
        artifact_df = ArtifactDataFrame([parent_artifact, child_artifact])
        args = RankingArgs(run_name=f"{child_type}2{parent_type}", dataset=PromptDataset(artifact_df=artifact_df),
                           parent_ids=parent_ids,
                           children_ids=children_ids)
        return args
