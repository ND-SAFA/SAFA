from typing import List
from unittest import TestCase

from tgen_test.ranking.steps.ranking_pipeline_test import RankingPipelineTest, DEFAULT_PARENT_IDS, DEFAULT_CHILDREN_IDS
from common_resources.tools.constants.symbol_constants import NEW_LINE
from tgen.common.constants.ranking_constants import PROJECT_SUMMARY_HEADER
from common_resources.tools.util.enum_util import EnumDict
from tgen.summarizer.summary import Summary
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager
from tgen.testres.test_data_manager import TestDataManager
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.steps.complete_ranking_prompts_step import CompleteRankingPromptsStep


class TesCompleteRankingResponsesStep(TestCase):

    def test_no_project_summary_included(self):
        self.run_step(summary_included=False)

    def test_project_summary_included(self):
        project_summary = Summary({"overview": EnumDict({"chunks": [f"# {PROJECT_SUMMARY_HEADER}\nthis is a project summary"],
                                                         "title": "overview"})})
        self.run_step(project_summary=project_summary, summary_included=True)

    @mock_anthropic
    def run_step(self, ai_manager: TestAIManager,
                 parent_ids: List[str] = None,
                 children_ids: List[str] = None,
                 summary_included: bool = True,
                 **state_kwargs) -> str:
        """
        Runs the prompt creation step with given configuration variables.
        :param parent_ids: The ids of the parent artifacts.
        :param children_ids: The ids of the children artifacts.
        :param state_kwargs: Additional keyword arguments to state.
        :return: The prompt created by builder.
        """
        ai_manager.n_used = 0
        if parent_ids is None:
            parent_ids = DEFAULT_PARENT_IDS
        if children_ids is None:
            children_ids = DEFAULT_CHILDREN_IDS

        ai_manager.set_responses([lambda prompt: self.assert_prompts(prompt, parent_ids, children_ids, summary_included)
                                  for p_id in parent_ids])

        parent2children = {p: [RankingUtil.create_entry(p, c) for c in children_ids] for p in parent_ids}
        args, state = RankingPipelineTest.create_ranking_structures(parent_ids=parent_ids,
                                                                    children_ids=children_ids,
                                                                    state_kwargs=state_kwargs)
        state.sorted_parent2children = parent2children
        step = CompleteRankingPromptsStep()
        step.run(args, state)
        self.assertEqual(len(parent_ids), ai_manager.n_used)
        for p_id, ranking_response in zip(parent_ids, state.ranking_responses):
            scores = self._get_scores_for_parent(children_ids, p_id)
            for score, child_entry in zip(scores, ranking_response):
                self.assertEqual(float(score), child_entry['score'][0])

    def assert_prompts(self, prompt, parent_ids, children_ids, summary_included):
        parent_id = None
        for p_id in parent_ids:
            artifact_body = TesCompleteRankingResponsesStep.get_artifact_body(p_id)
            if artifact_body in prompt:
                parent_id = p_id
        if summary_included:
            project_summary = f"# {PROJECT_SUMMARY_HEADER}\nthis is a project summary"
            self.assertIn(project_summary, prompt)
        else:
            self.assertNotIn(f"# {PROJECT_SUMMARY_HEADER}\n", prompt)
        for artifact_id in children_ids:
            artifact_body = TesCompleteRankingResponsesStep.get_artifact_body(artifact_id)
            self.assertIn(artifact_body, prompt)
        scores = self._get_scores_for_parent(children_ids, parent_id)
        responses = [RankingPipelineTest.get_response(score=info[1], child_id=info[0], include_parent_summary=i > 0
                                                      ) for i, info in enumerate(zip(children_ids, scores))]
        return NEW_LINE.join(responses)

    def _get_scores_for_parent(self, children_ids, parent_id):
        p_index = DEFAULT_PARENT_IDS.index(parent_id)
        scores = [abs(p_index - i) + 1 for i in range(len(children_ids))]
        return scores

    @staticmethod
    def get_artifact_body(artifact_name: str) -> str:
        return TestDataManager.get_artifact_body(artifact_name)
