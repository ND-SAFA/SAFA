import os

from test.ranking.steps.ranking_pipeline_util import RankingPipelineTest
from tgen.common.util.file_util import FileUtil
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.ranking.steps.step_create_project_summary import CreateProjectSummary
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.testprojects.mocking.mock_anthropic import mock_anthropic
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


class TestCreateProjectSummary(BaseTest):
    """
    Requirements: https://www.notion.so/nd-safa/step_create_project_summary-e67877b280d144ec8007a2062a2d3936?pvs=4
    """
    PROJECT_SUMMARY = "project summary"

    @mock_anthropic
    def test_generate_project_summary(self, ai_manager: TestAIManager):
        """
        Tests the generation of a project summary.
        """
        ai_manager.set_responses([self.PROJECT_SUMMARY])
        args, state = RankingPipelineTest.create_ranking_structures()
        step = CreateProjectSummary()
        self.assert_result(args, state, step)

    def test_accept_project_summary(self):
        """
        Tests ability to receive a specified project summary.
        """
        args, state = RankingPipelineTest.create_ranking_structures(project_summary=self.PROJECT_SUMMARY)
        step = CreateProjectSummary()
        self.assert_result(args, state, step)

    def test_read_project_summary(self):
        project_summary_path = os.path.join(TEST_OUTPUT_DIR, "project_summary.txt")
        FileUtil.write(self.PROJECT_SUMMARY, project_summary_path)

        args, state = RankingPipelineTest.create_ranking_structures(project_summary_path=project_summary_path)
        step = CreateProjectSummary()
        self.assert_result(args, state, step)

    def test_skip_project_summary(self):
        """
        Tests that project summary can be skipped.
        """
        args, state = RankingPipelineTest.create_ranking_structures(generate_summary=False)
        step = CreateProjectSummary()
        self.assert_result(args, state, step, expected_value=None)

    def assert_result(self, args: RankingArgs, state: RankingState, step: CreateProjectSummary,
                      expected_value: str = PROJECT_SUMMARY):
        self.assertEqual(state.project_summary, None)
        step.run(args, state)
        self.assertEqual(state.project_summary, expected_value)
