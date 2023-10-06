from unittest import TestCase

from test.ranking.steps.ranking_pipeline_test import DEFAULT_PARENT_IDS, DEFAULT_CHILDREN_IDS, RankingPipelineTest
from tgen.common.util.enum_util import EnumDict
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.steps.create_explanations_step import CreateExplanationsStep


class TestCreateExplanationsStep(TestCase):
    SELECTED_ENTRIES = [EnumDict({'id': 1, 'source': 't6', 'target': 's4', 'score': 0.4}),
                        EnumDict({'id': 2, 'source': 't1', 'target': 's4', 'score': 0.7}),
                        EnumDict({'id': 3, 'source': 't6', 'target': 's5', 'score': 0.5}),
                        EnumDict({'id': 4, 'source': 't1', 'target': 's5', 'score': 0.7})
                        ]

    @mock_anthropic
    def test_run(self, anthropic_mock: TestAIManager):
        anthropic_mock.set_responses([RankingPipelineTest.get_response(child_id=entry['source'], include_child_id_in_explanation=True)
                                      for entry in self.SELECTED_ENTRIES])
        parent_ids = DEFAULT_PARENT_IDS
        children_ids = DEFAULT_CHILDREN_IDS
        args, state = self.get_args_and_state(children_ids, parent_ids)
        CreateExplanationsStep().run(args, state)
        for i, entry in enumerate(state.selected_entries):
            self.assertIn('explanation', entry)
            self.assertIn(self.SELECTED_ENTRIES[i]['source'], entry['explanation'])

    @staticmethod
    def get_args_and_state(children_ids, parent_ids):
        args, state = RankingPipelineTest.create_ranking_structures(
            children_ids=[entry['source'] for entry in TestCreateExplanationsStep.SELECTED_ENTRIES],
            parent_ids=[entry['target'] for entry in TestCreateExplanationsStep.SELECTED_ENTRIES])
        state.sorted_parent2children = {p_id: [RankingUtil.create_entry(p_id, c_id) for c_id in children_ids]
                                        for p_id in parent_ids},
        state.selected_entries = TestCreateExplanationsStep.SELECTED_ENTRIES
        return args, state
