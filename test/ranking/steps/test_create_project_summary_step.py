from typing import Any, List, Union

from test.ranking.steps.ranking_pipeline_test import RankingPipelineTest
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_responses import MOCK_PS_RES_MAP, MockResponses
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.steps.create_project_summary_step import CreateProjectSummaryStep


class TestCreateProjectSummary(BaseTest):
    """
    Requirements: https://www.notion.so/nd-safa/step_create_project_summary-e67877b280d144ec8007a2062a2d3936?pvs=4
    """
    PROJECT_SUMMARY = list(MOCK_PS_RES_MAP.values())

    @mock_anthropic
    def test_generate_project_summary(self, ai_manager: TestAIManager):
        """
        Tests the generation of a project summary.
        """
        ai_manager.mock_summarization()
        ai_manager.set_responses(MockResponses.project_summary_responses)
        args, state = RankingPipelineTest.create_ranking_structures()
        step = CreateProjectSummaryStep()
        self.assert_result(args, state, step)

    def test_accept_project_summary(self):
        """
        Tests ability to receive a specified project summary.
        """
        args, state = RankingPipelineTest.create_ranking_structures(project_summary=self.PROJECT_SUMMARY)
        step = CreateProjectSummaryStep()
        self.assert_result(args, state, step)

    def test_skip_project_summary(self):
        """
        Tests that project summary can be skipped.
        """
        args, state = RankingPipelineTest.create_ranking_structures(generate_summary=False)
        step = CreateProjectSummaryStep()
        self.assert_result(args, state, step, expected_value=None)

    def assert_result(self, args: RankingArgs, state: RankingState, step: CreateProjectSummaryStep,
                      expected_value: Union[Any, List[str]] = PROJECT_SUMMARY):
        self.assertEqual(state.project_summary, None)
        step.run(args, state)
        if isinstance(expected_value, list):
            for ev in expected_value:
                self.assertIn(ev, state.project_summary)
        else:
            self.assertEqual(state.project_summary, expected_value)
