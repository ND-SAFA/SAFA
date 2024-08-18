from gen_common.constants.ranking_constants import RANKING_MAX_SCORE, RANKING_MIN_SCORE
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.traceability.ranking.common.ranking_args import RankingArgs
from gen_common.traceability.ranking.llm_ranking_pipeline import LLMRankingPipeline
from gen_common.traceability.ranking.trace_selectors.selection_methods import SupportedSelectionMethod

from gen_common.util.math_util import MathUtil
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.traceability.ranking.explanation_prompts import EXPLANATION_TASK_QUESTIONNAIRE
from gen_common_test.traceability.ranking.steps.ranking_pipeline_test import CHILD_ID, PARENT_ID, RankingPipelineTest


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
        ai_manager.set_responses([RankingPipelineTest.get_response()] +
                                 [RankingPipelineTest.get_response(task_prompt=EXPLANATION_TASK_QUESTIONNAIRE)])
        args = self.create_args()
        pipeline = LLMRankingPipeline(args)
        pipeline.run()
        prediction_entries = pipeline.state.selected_entries
        self.assertEqual(1, len(prediction_entries))
        entry = prediction_entries[0]
        self.assertEqual(CHILD_ID, entry[TraceKeys.SOURCE.value])
        self.assertEqual(PARENT_ID, entry[TraceKeys.TARGET.value])
        for tag in RankingPipelineTest.get_explanation_tags(task_prompt=EXPLANATION_TASK_QUESTIONNAIRE):
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
                           children_ids=children_ids, weight_of_embedding_scores=0, weight_of_explanation_scores=0,
                           generate_explanations=True,
                           types_to_trace=("target", "source"), selection_method=SupportedSelectionMethod.SELECT_BY_THRESHOLD)
        return args


if __name__ == "__main__":
    TestLLMRankingPipeline.test_prediction_construction(None)
