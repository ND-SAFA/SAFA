from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.tracing.ranking_constants import RANKING_ARTIFACT_TAG, RANKING_ID_TAG, \
    RANKING_PARENT_SUMMARY_TAG, \
    RANKING_SCORE_TAG
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_responses import MockResponses
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.tracing.ranking.llm_ranking_pipeline import LLMRankingPipeline
from tgen.tracing.ranking.common.ranking_args import RankingArgs

PARENT_ID = "parent_1"
CHILD_ID = "child_1"
SCORE = 4
TASK_PROMPT: QuestionnairePrompt = SupportedPrompts.RANKING_QUESTION2.value
EXPLANATION_TAG = [tag for tag in TASK_PROMPT.response_manager.get_all_tag_ids() if tag not in {RANKING_PARENT_SUMMARY_TAG,
                                                                                                RANKING_ARTIFACT_TAG,
                                                                                                RANKING_ID_TAG,
                                                                                                RANKING_SCORE_TAG}]
EXPLANTION_RESPONSE = NEW_LINE.join([PromptUtil.create_xml(tag, tag.upper()) for tag in EXPLANATION_TAG])
TEST_RESPONSE = (
        f"<{RANKING_PARENT_SUMMARY_TAG}>Parent Summary.</{RANKING_PARENT_SUMMARY_TAG}>\n"
        f"<{RANKING_ARTIFACT_TAG}>"
        f"<{RANKING_ID_TAG}>0</{RANKING_ID_TAG}>"
        f"{EXPLANTION_RESPONSE}"
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
        pipeline.run()
        prediction_entries = pipeline.state.children_entries
        self.assertEqual(1, len(prediction_entries))
        entry = prediction_entries[0]
        self.assertEqual(CHILD_ID, entry[TraceKeys.SOURCE.value])
        self.assertEqual(PARENT_ID, entry[TraceKeys.TARGET.value])
        for tag in EXPLANATION_TAG:
            self.assertIn(tag, entry[TraceKeys.EXPLANATION.value].lower())
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
        args = RankingArgs(run_name=f"{child_type}2{parent_type}", dataset=PromptDataset(artifact_df=artifact_df),
                           parent_ids=parent_ids,
                           children_ids=children_ids)
        return args
