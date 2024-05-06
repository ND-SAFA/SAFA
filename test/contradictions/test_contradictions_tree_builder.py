from test.contradictions.data_test_requirements import R1, R3, R2, R4, R5
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.common_choices import CommonChoices
from tgen.contradictions.with_decision_tree.contradiction_decision_nodes import SupportedContradictionDecisionNodes
from tgen.contradictions.with_decision_tree.contradictions_tree_builder import ContradictionsTreeBuilder
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestContradictionsTreeBuilder(BaseTest):

    @mock_anthropic
    def test_traversal(self, test_manager: TestAIManager):
        builder = ContradictionsTreeBuilder()
        responses = [PromptUtil.create_xml("answer", r) for i in range(5) for r in [CommonChoices.NO, CommonChoices.YES]]
        test_manager.add_responses(responses)
        tree = builder.build_tree()

        # Q1
        q1a = tree.starting_node
        q1 = q1a.select_branch(q1a.make_choice((R1, R3)))  # should be no bc vars are different
        self.assertTrue(isinstance(q1, LLMNode))
        choice_no = q1.make_choice((R1, R2))  # mocked response from LLM
        self.assertEqual(q1.select_branch(choice_no), SupportedContradictionDecisionNodes.NONE.value)

        choice_no = q1a.make_choice((R1, R2))  # should be no bc vars are the same
        q2a = builder.get_question_node(2)
        choice_yes = q1.make_choice((R1, R2))  # mocked response from LLM
        self.assertEqual(q1a.select_branch(choice_no), q2a)
        self.assertEqual(q1.select_branch(choice_yes), q2a)

        # Q2
        q2 = q2a.select_branch(q2a.make_choice((R1, R2)))  # should be no bc actions are different
        self.assertTrue(isinstance(q2, LLMNode))
        choice_no = q2.make_choice((R1, R2))  # mocked response from LLM
        q3 = builder.get_question_node(3)
        self.assertEqual(q2.select_branch(choice_no), q3)

        choice_yes = q2a.make_choice((R1, R3))  # should be yes bc actions are same
        q4 = builder.get_question_node(4)
        self.assertEqual(q2a.select_branch(choice_yes), q4)
        choice_yes = q2.make_choice((R1, R2))  # mocked response from LLM
        self.assertEqual(q2.select_branch(choice_yes), q4)

        # Q3
        self.assertTrue(isinstance(q3, LLMNode))
        choice_no = q3.make_choice((R1, R2))  # mocked response from LLM
        self.assertEqual(q3.select_branch(choice_no), SupportedContradictionDecisionNodes.NONE.value)

        choice_yes = q3.make_choice((R1, R2))  # mocked response from LLM
        self.assertEqual(q3.select_branch(choice_yes), q4)

        # Q4
        choice_no = q4.make_choice((R1, R3))  # should be no bc one does not contain condition
        self.assertEqual(q4.select_branch(choice_no), SupportedContradictionDecisionNodes.SIMPLEX_CONTRADICTION.value)

        choice_yes = q4.make_choice((R1, R2))  # should be no bc one does not contain condition
        q5a = builder.get_question_node(5)
        self.assertEqual(q4.select_branch(choice_yes), q5a)

        # Q5
        q5 = q5a.select_branch(q5a.make_choice((R1, R4)))  # should be no bc conditions are different
        self.assertTrue(isinstance(q5, LLMNode))
        choice_no = q5.make_choice((R1, R2))  # mocked response from LLM
        q6 = builder.get_question_node(6)
        self.assertEqual(q5.select_branch(choice_no), q6)

        choice_yes = q5a.make_choice((R1, R2))  # should be yes bc conditions are the same
        self.assertEqual(q5a.select_branch(choice_yes), SupportedContradictionDecisionNodes.IDEM_CONTRADICTION.value)
        choice_yes = q5.make_choice((R1, R2))  # mocked response from LLM
        self.assertEqual(q5.select_branch(choice_yes), SupportedContradictionDecisionNodes.IDEM_CONTRADICTION.value)

        # Q6
        self.assertTrue(isinstance(q6, LLMNode))
        choice_no = q6.make_choice((R1, R4))  # mocked response from LLM
        self.assertEqual(q6.select_branch(choice_no), SupportedContradictionDecisionNodes.NONE.value)

        choice_yes = q6.make_choice((R1, R4))  # mocked response from LLM
        self.assertEqual(q6.select_branch(choice_yes), SupportedContradictionDecisionNodes.ALIUS_CONTRADICTION.value)

    def test_tree(self):
        builder = ContradictionsTreeBuilder()
        tree = builder.build_tree()
        first_prompt_builder, path = tree.next_step((R1, R5))
        q1: LLMNode = tree.starting_node.select_branch(CommonChoices.NO)
        self.assertIn(q1.get_formatted_question((R1, R5)), first_prompt_builder.build(OpenAIManager.prompt_args)[PromptKeys.PROMPT])
        path.add_decision(CommonChoices.NO)
        no_prompt_builder, path = tree.next_step((R1, R5), path)
        self.assertIsNone(no_prompt_builder)
        self.assertEqual(path.get_final_decision(), SupportedContradictionDecisionNodes.NONE.value.description)
