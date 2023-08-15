from typing import List

from test.ranking.steps.ranking_pipeline_util import RankingPipelineTest
from tgen.ranking.steps.step_create_ranking_prompts import CreateRankingPrompts
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_data_manager import TestDataManager


class TestCreateRankingPrompts(BaseTest):
    """
    TODO: Add notion requirements
    """
    DEFAULT_PARENT_IDS = ["s4"]
    DEFAULT_CHILDREN_IDS = ["t1", "t6"]

    def test_no_project_summary_included(self):
        prompt = self.run_step()
        self.assertNotIn("# Project Specification", prompt)

    def test_project_summary_included(self):
        project_summary = "# Project Specification\nthis is a project summary"
        prompt = self.run_step(project_summary=project_summary)
        self.assertIn(project_summary, prompt)

    def test_all_artifacts_included(self):
        prompt = self.run_step()
        artifact_ids = self.DEFAULT_PARENT_IDS + self.DEFAULT_CHILDREN_IDS
        for artifact_id in artifact_ids:
            artifact_body = self.get_artifact_body(artifact_id)
            self.assertIn(artifact_body, prompt)

    def run_step(self, parent_ids: List[str] = None, children_ids: List[str] = None, **state_kwargs) -> str:
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

        parent2children = {p: children_ids for p in parent_ids}
        args, state = RankingPipelineTest.create_ranking_structures(parent_ids=parent_ids,
                                                                    children_ids=children_ids,
                                                                    state_kwargs=state_kwargs)
        state.sorted_parent2children = parent2children
        step = CreateRankingPrompts()
        step.run(args, state)
        self.assertEqual(len(self.DEFAULT_PARENT_IDS), len(state.ranking_prompts))
        self.assertIsNotNone(state.prompt_builder)
        prompt = state.ranking_prompts[0]
        return prompt

    @staticmethod
    def get_artifact_body(artifact_name: str) -> str:
        return TestDataManager.get_artifact_body(artifact_name)
