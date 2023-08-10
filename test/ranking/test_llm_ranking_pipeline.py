from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.ranking.llm_ranking_pipeline import LLMRankingPipeline
from tgen.ranking.ranking_args import RankingArgs
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.testprojects.mocking.mock_ai_decorator import mock_anthropic
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager

PARENT_ID = "parent_1"
CHILD_ID = "child_1"
EXPLANATION = "EXPLANATION"
SCORE = 4
TEST_RESPONSE = "<query-summary>Query Summary.</query-summary>\n" \
                f"<explanation>0 | SUMMARY | {EXPLANATION} | {SCORE}</explanation>"


class TestLLMRankingPipeline(BaseTest):
    """
    Tests the requirements: https://www.notion.so/nd-safa/llm_ranking_pipeline-b9c4607d47f44c739fc2ebf623fa8dcc?pvs=4
    """

    @mock_anthropic
    def test_prediction_construction(self, test_response_manager: TestAIManager):
        """
        Tests that pipeline correctly constructs the ranked predictions.
        """
        test_response_manager.responses = [
            "<summary>project_summary</summary>",
            TEST_RESPONSE
        ]
        args = self.create_args()
        pipeline = LLMRankingPipeline(args)
        prediction_entries = pipeline.run()
        self.assertEqual(1, len(prediction_entries))
        entry = prediction_entries[0]
        self.assertEqual(CHILD_ID, entry["source"])
        self.assertEqual(PARENT_ID, entry["target"])
        self.assertEqual(EXPLANATION, entry["explanation"])
        self.assertEqual(1, entry["score"])  # top score because only ranking

    @staticmethod
    def create_args() -> RankingArgs:
        """
        Creates ranking arguments for pipeline.
        """
        parent_artifact = {"id": PARENT_ID, "content": "content_1", "layer_id": "parent"}
        child_artifact = {"id": CHILD_ID, "content": "content_2", "layer_id": "child"}
        parent_ids = [PARENT_ID]
        children_ids = [CHILD_ID]
        artifact_df = ArtifactDataFrame([parent_artifact, child_artifact])
        args = RankingArgs(artifact_df=artifact_df, parent_ids=parent_ids, children_ids=children_ids)
        return args
