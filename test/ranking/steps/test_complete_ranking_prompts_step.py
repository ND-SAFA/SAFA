from typing import List
from unittest import TestCase, mock

from test.ranking.steps.ranking_pipeline_test import RankingPipelineTest
from tgen.common.constants.tracing.ranking_constants import PROJECT_SUMMARY_HEADER
from tgen.testres.test_data_manager import TestDataManager
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.steps.complete_ranking_prompts_step import CompleteRankingPromptsStep


class TesCompleteRankingResponsesStep(TestCase):
    DEFAULT_PARENT_IDS = ["s4"]
    DEFAULT_CHILDREN_IDS = ["t1", "t6"]

    def test_no_project_summary_included(self):
        prompt = self.run_step()
        self.assertNotIn(f"# {PROJECT_SUMMARY_HEADER}\n", prompt)

    def test_project_summary_included(self):
        project_summary = f"# {PROJECT_SUMMARY_HEADER}\nthis is a project summary"
        prompt = self.run_step(project_summary=project_summary)
        self.assertIn(project_summary, prompt)

    def test_all_artifacts_included(self):
        prompt = self.run_step()
        artifact_ids = self.DEFAULT_PARENT_IDS + self.DEFAULT_CHILDREN_IDS
        for artifact_id in artifact_ids:
            artifact_body = self.get_artifact_body(artifact_id)
            self.assertIn(artifact_body, prompt)

    @mock.patch.object(CompleteRankingPromptsStep, "complete_ranking_prompts")
    def run_step(self, complete_ranking_prompts_mock: mock.MagicMock,
                 parent_ids: List[str] = None, children_ids: List[str] = None, **state_kwargs) -> str:
        """
        Runs the prompt creation step with given configuration variables.
        :param parent_ids: The ids of the parent artifacts.
        :param children_ids: The ids of the children artifacts.
        :param state_kwargs: Additional keyword arguments to state.
        :return: The prompt created by builder.
        """
        if parent_ids is None:
            parent_ids = self.DEFAULT_PARENT_IDS
        if children_ids is None:
            children_ids = self.DEFAULT_CHILDREN_IDS

        parent2children = {p: [RankingUtil.create_entry(p, c) for c in children_ids] for p in parent_ids}
        args, state = RankingPipelineTest.create_ranking_structures(parent_ids=parent_ids,
                                                                    children_ids=children_ids,
                                                                    state_kwargs=state_kwargs)
        state.sorted_parent2children = parent2children
        step = CompleteRankingPromptsStep()
        step.run(args, state)
        ranking_prompts = step.create_ranking_prompts(args, state)
        self.assertEqual(len(self.DEFAULT_PARENT_IDS), len(ranking_prompts))
        prompt = ranking_prompts[0]
        return prompt

    @staticmethod
    def get_artifact_body(artifact_name: str) -> str:
        return TestDataManager.get_artifact_body(artifact_name)
