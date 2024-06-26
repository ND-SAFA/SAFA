from test.jobs.health_check_jobs.health_check_constants import EXPECTED_CONTEXT_IDS, QUERY
from test.jobs.health_check_jobs.health_check_utils import get_chat_history, get_dataset_for_context
from tgen.chat.chat_args import ChatArgs
from tgen.chat.chat_node_ids import ChatNodeIDs
from tgen.chat.chat_state import ChatState
from tgen.chat.chat_tree_definition import ChatTreeDefinition
from tgen.chat.message_meta import MessageMeta
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.decision_tree.nodes.action_node import ActionNode
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.path import Path
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestChatTreeDefinition(BaseTest):

    def test_include_context_node(self):
        builder = ChatTreeDefinition().builder
        include_context_node: LLMNode = builder.get_node(ChatNodeIDs.INCLUDE_CONTEXT)
        args, state = self.get_args_and_state()
        prompt_builder = include_context_node.create_prompt_builder(args, state)
        prompt = prompt_builder.build(args.llm_manager.prompt_args)[PromptKeys.PROMPT]
        self.assertIn(QUERY[ArtifactKeys.CONTENT], prompt)

        self.assert_correct_choice(" Yes", ChatNodeIDs.CONTEXT_TYPE, include_context_node, prompt_builder)

        self.assert_correct_choice("no", ChatNodeIDs.USER_CHAT, include_context_node, prompt_builder)

        self.assert_correct_choice("Bad Response", ChatNodeIDs.USER_CHAT, include_context_node, prompt_builder)

    def assert_correct_choice(self, llm_response: str, expected_next_node_id: str, node: LLMNode, prompt_builder: PromptBuilder):
        response = prompt_builder.parse_responses(PromptUtil.create_xml(node.response_tag, llm_response))
        choice = node.get_choice_from_response(response)
        next_selected_node = node.select_branch(choice)
        self.assertEqual(next_selected_node.node_id, expected_next_node_id)

    def test_context_type_node(self):
        builder = ChatTreeDefinition().builder
        context_type_node: LLMNode = builder.get_node(ChatNodeIDs.CONTEXT_TYPE)
        args, state = self.get_args_and_state()
        prompt_builder = context_type_node.create_prompt_builder(args, state)
        prompt = prompt_builder.build(args.llm_manager.prompt_args)[PromptKeys.PROMPT]
        self.assertIn(QUERY["content"], prompt)
        for a_type in args.dataset.artifact_df.get_artifact_types():
            self.assertIn(a_type, prompt)

        response = prompt_builder.parse_responses(PromptUtil.create_xml(context_type_node.response_tag, "layer1, layer2"))
        choice = context_type_node.get_choice_from_response(response)
        Path(context_type_node, args, state).add_decision(choice)
        self.assertEqual(len(choice), 2)
        self.assertEqual(state.context_artifact_types, choice)

        next_selected_node = context_type_node.select_branch(choice)
        self.assertEqual(next_selected_node.node_id, ChatNodeIDs.REWRITE_QUERY)

    def test_re_write_query_node(self):
        builder = ChatTreeDefinition().builder
        rewrite_query_node: LLMNode = builder.get_node(ChatNodeIDs.REWRITE_QUERY)
        args, state = self.get_args_and_state()
        prompt_builder = rewrite_query_node.create_prompt_builder(args, state)
        prompt = prompt_builder.build(args.llm_manager.prompt_args)[PromptKeys.PROMPT]
        self.assertIn(QUERY["content"], prompt)

        rewritten_query = "rewritten query"
        response = prompt_builder.parse_responses(PromptUtil.create_xml(rewrite_query_node.response_tag, rewritten_query))
        choice = rewrite_query_node.get_choice_from_response(response)
        Path(rewrite_query_node, args, state).add_decision(choice)
        self.assertEqual(rewritten_query, choice)
        self.assertEqual(state.rewritten_query, choice)

        next_selected_node = rewrite_query_node.select_branch(choice)
        self.assertEqual(next_selected_node.node_id, ChatNodeIDs.RAG)

    def test_rag_node(self):
        builder = ChatTreeDefinition().builder
        rag_node: ActionNode = builder.get_node(ChatNodeIDs.RAG)
        args, state = self.get_args_and_state()
        state.context_artifact_types = ["all"]

        choice = rag_node.make_choice(args, state)
        for a_id in EXPECTED_CONTEXT_IDS:
            self.assertIn(a_id, choice)
        self.assertEqual(state.related_artifact_ids, choice)
        self.assertSetEqual(state.context_artifact_types, set(args.dataset.artifact_df.get_artifact_types()))

        next_selected_node = rag_node.select_branch(choice)
        self.assertEqual(next_selected_node.node_id, ChatNodeIDs.USER_CHAT)

    @mock_anthropic
    def test_user_chat(self, test_manager: TestAIManager):
        builder = ChatTreeDefinition().builder
        chat_node: ActionNode = builder.get_node(ChatNodeIDs.USER_CHAT)
        args, state = self.get_args_and_state()
        state.update_related_artifact_ids(EXPECTED_CONTEXT_IDS, args.dataset.artifact_df, args.llm_manager)

        response = "You should get a cat"
        test_manager.set_responses([lambda prompt: self.response(prompt, response, args.dataset.artifact_df)])
        choice = chat_node.make_choice(args, state)
        self.assertEqual(choice, response)

        Path(chat_node, args, state).add_decision(choice)
        self.assertEqual(MessageMeta.get_most_recent_message(state.user_chat_history)["content"], response)

    def response(self, prompt, response, artifact_df):
        user_prompt, system_prompt = prompt

        for a_id in EXPECTED_CONTEXT_IDS:
            content = artifact_df.get_artifact(a_id)[ArtifactKeys.CONTENT]
            self.assertIn(content, system_prompt)
        return response

    def get_args_and_state(self):
        args = ChatArgs(dataset=get_dataset_for_context(),
                        chat_history=get_chat_history())
        state = ChatState(user_chat_history=args.chat_history)
        return args, state
