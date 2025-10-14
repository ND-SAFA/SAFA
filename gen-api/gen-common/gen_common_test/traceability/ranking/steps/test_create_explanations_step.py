import re
from unittest import TestCase

from gen_common.traceability.ranking.steps.create_explanations_step import CreateExplanationsStep
from gen_common.util.enum_util import EnumDict
from gen_common.util.ranking_util import RankingUtil
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.traceability.ranking.explanation_prompts import EXPLANATION_TASK_QUESTIONNAIRE
from gen_common_test.traceability.ranking.steps.ranking_pipeline_test import DEFAULT_CHILDREN_IDS, DEFAULT_PARENT_IDS, \
    RankingPipelineTest


class TestCreateExplanationsStep(TestCase):
    SELECTED_ENTRIES = [EnumDict({'id': 1, 'source': 't6', 'target': 's4', 'score': 0.35}),
                        EnumDict({'id': 2, 'source': 't1', 'target': 's4', 'score': 0.7}),
                        EnumDict({'id': 3, 'source': 't6', 'target': 's5', 'score': 0.5}),
                        EnumDict({'id': 4, 'source': 't1', 'target': 's5', 'score': 0.7})
                        ]

    def assert_prompt(self, prompt):
        source_id = self.find_artifact_id_in_prompt(prompt, is_child=True)
        target_id = self.find_artifact_id_in_prompt(prompt, is_child=False)
        i, entry = [(i, entry) for i, entry in enumerate(self.SELECTED_ENTRIES)
                    if entry['source'] == source_id and entry['target'] == target_id][0]
        expected_score = CreateExplanationsStep._convert_normalized_score_to_ranking_range(entry['score'])
        self.assertIn(str(expected_score), prompt)
        response = RankingPipelineTest.get_response(child_id=entry['source'], include_child_id_in_explanation=True,
                                                    task_prompt=EXPLANATION_TASK_QUESTIONNAIRE)
        return response

    @staticmethod
    def find_artifact_id_in_prompt(prompt: str, is_child: bool):
        if is_child:
            relation = "Child"
            key = 'source'
        else:
            relation = "Parent"
            key = 'target'
        prefix = TestCreateExplanationsStep.SELECTED_ENTRIES[0][key][0]
        pattern = fr"# {prefix}[1-6] \({relation}\)"
        matches = re.findall(pattern, prompt)
        matches = re.findall(fr"{prefix}[1-6]", matches[0])
        return matches[0]

    @mock_anthropic
    def test_run(self, anthropic_mock: TestAIManager):
        first_filter_entries = [e for e in self.SELECTED_ENTRIES if e["score"] >= 0.4]
        anthropic_mock.set_responses([self.assert_prompt for _ in first_filter_entries])
        parent_ids = DEFAULT_PARENT_IDS
        children_ids = DEFAULT_CHILDREN_IDS
        args, state = self.get_args_and_state(children_ids, parent_ids)
        CreateExplanationsStep().run(args, state)
        for i, entry in enumerate(state.selected_entries):
            self.assertIn('explanation', entry)
            self.assertIn(first_filter_entries[i]['source'], entry['explanation'])

    @staticmethod
    def get_args_and_state(children_ids, parent_ids):
        args, state = RankingPipelineTest.create_ranking_structures(
            generate_explanations=True,
            children_ids=[entry['source'] for entry in TestCreateExplanationsStep.SELECTED_ENTRIES],
            parent_ids=[entry['target'] for entry in TestCreateExplanationsStep.SELECTED_ENTRIES])
        state.sorted_parent2children = {p_id: [RankingUtil.create_entry(p_id, c_id) for c_id in children_ids]
                                        for p_id in parent_ids},
        state.selected_entries = TestCreateExplanationsStep.SELECTED_ENTRIES
        return args, state
