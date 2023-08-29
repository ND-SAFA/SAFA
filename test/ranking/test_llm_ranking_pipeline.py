from tgen.common.constants.tracing.ranking_constants import RANKING_ARTIFACT_TAG, RANKING_EXPLANATION_TAG, RANKING_ID_TAG, \
    RANKING_PARENT_SUMMARY_TAG, \
    RANKING_SCORE_TAG
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_responses import MockResponses
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.tracing.ranking.llm_ranking_pipeline import LLMRankingPipeline
from tgen.tracing.ranking.ranking_args import RankingArgs

PARENT_ID = "parent_1"
CHILD_ID = "child_1"
EXPLANATION = "EXPLANATION"
SCORE = 4
TEST_RESPONSE = (
    f"<{RANKING_PARENT_SUMMARY_TAG}>Parent Summary.</{RANKING_PARENT_SUMMARY_TAG}>\n"
    f"<{RANKING_ARTIFACT_TAG}>"
    f"<{RANKING_ID_TAG}>0</{RANKING_ID_TAG}>"
    f"<{RANKING_EXPLANATION_TAG}>{EXPLANATION}</{RANKING_EXPLANATION_TAG}>"
    f"<{RANKING_SCORE_TAG}>{SCORE}</{RANKING_SCORE_TAG}>"
    f"</{RANKING_ARTIFACT_TAG}>"
)


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
                                 [TEST_RESPONSE])
        args = self.create_args()
        pipeline = LLMRankingPipeline(args)
        prediction_entries = pipeline.run()
        self.assertEqual(1, len(prediction_entries))
        entry = prediction_entries[0]
        self.assertEqual(CHILD_ID, entry[TraceKeys.SOURCE.value])
        self.assertEqual(PARENT_ID, entry[TraceKeys.TARGET.value])
        self.assertEqual(EXPLANATION, entry[TraceKeys.EXPLANATION.value])
        self.assertEqual(.4, entry[TraceKeys.SCORE.value])

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
        args = RankingArgs(run_name=f"{child_type}2{parent_type}", artifact_df=artifact_df, parent_ids=parent_ids,
                           children_ids=children_ids)
        return args
