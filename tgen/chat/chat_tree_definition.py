from typing import Dict, Set

from tgen.chat.chat_args import ChatArgs
from tgen.chat.chat_node_ids import ChatNodeIDs
from tgen.chat.chat_state import ChatState
from tgen.common.constants.deliminator_constants import COMMA
from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.common_choices import CommonChoices
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.decision_tree.nodes.action_node import ActionNode
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.tree import Tree
from tgen.decision_tree.tree_builder import TreeBuilder
from tgen.models.llm.abstract_llm_manager import PromptRoles
from tgen.prompts.supported_prompts.chat_prompts import INCLUDE_MORE_CONTEXT_PROMPT, ARTIFACT_TYPE_FOR_CONTEXT_PROMPT, TYPES_FORMAT_VAR
from tgen.tracing.context_finder import ContextFinder


class ChatTreeDefinition:
    QUERY_ARTIFACT_ID = "query"

    def __init__(self, root_node_id: str = ChatNodeIDs.INCLUDE_CONTEXT):
        """
        Defines the nodes and tree structure for chat state.
        :param root_node_id: The id of the root or starting node.
        """
        node_constructor_map = {ChatNodeIDs.INCLUDE_CONTEXT: self.build_include_context_node,
                                ChatNodeIDs.CONTEXT_TYPE: self.build_context_type_node,
                                ChatNodeIDs.USER_CHAT: self.build_user_chat_node,
                                ChatNodeIDs.RAG: self.build_rag_node}
        self.builder = TreeBuilder(root_node_id=root_node_id, node_constructor_map=node_constructor_map)

    @staticmethod
    def get_tree(root_node_id: str = ChatNodeIDs.INCLUDE_CONTEXT) -> Tree:
        """
        Gets the decision tree for chat.
        :param root_node_id: The id of the root or starting node.
        :return: The decision tree for chat.
        """
        return ChatTreeDefinition(root_node_id).builder.build_tree()

    def build_include_context_node(self) -> LLMNode:
        """
        Builds the node to determine whether the chat needs additional context.
        :return: The node to determine whether the chat needs additional context.
        """
        context_type_node = self.builder.get_node(node_id=ChatNodeIDs.CONTEXT_TYPE)
        user_chat_node = self.builder.get_node(node_id=ChatNodeIDs.USER_CHAT)
        include_context_node = LLMNode(description=INCLUDE_MORE_CONTEXT_PROMPT.value,
                                       node_id=ChatNodeIDs.INCLUDE_CONTEXT,
                                       default_response=CommonChoices.NO,
                                       branches={CommonChoices.YES: context_type_node,
                                                 CommonChoices.NO: user_chat_node})
        return include_context_node

    def build_context_type_node(self) -> LLMNode:
        """
        Builds the node to determine the types of artifacts to use for the context.
        :return: The node to determine the types of artifacts to use for the context.
        """
        rag_node = self.builder.get_node(node_id=ChatNodeIDs.RAG)
        context_type_node = LLMNode(description=ARTIFACT_TYPE_FOR_CONTEXT_PROMPT.value,
                                    node_id=ChatNodeIDs.CONTEXT_TYPE,
                                    input_variable_converter=ChatTreeDefinition.get_context_type_format_vars,
                                    response_manager_params={
                                        "value_formatter": lambda tag, value: {v.strip() for v in value.split(COMMA)}},
                                    state_setter="context_artifact_types",
                                    branches=rag_node)
        return context_type_node

    def build_rag_node(self) -> ActionNode:
        """
        Builds the node to perform rag for creating chat context.
        :return: The node to perform rag for creating chat contex.
        """
        chat_node = self.builder.get_node(node_id=ChatNodeIDs.USER_CHAT)
        rag_node = ActionNode(description="Run Rag for Chat Context", action_method=ChatTreeDefinition.run_rag,
                              branches=chat_node, node_id=ChatNodeIDs.RAG)
        return rag_node

    def build_user_chat_node(self) -> ActionNode:
        """
        Builds the node to get the response for user chat.
        :return: The node to get the response for user chat.
        """
        user_chat_node = ActionNode(description="Get Response for User Chat",
                                    node_id=ChatNodeIDs.USER_CHAT,
                                    action_method=lambda args, state: LLMTrainer.perform_chat(
                                        llm_manager=args.llm_manager, chat_history=state.user_chat_history,
                                        save_and_load_path=self.create_save_and_load_path_for_node(args, ChatNodeIDs.USER_CHAT),
                                        system_prompts=state.system_prompt).predictions[0],
                                    state_setter=lambda choice, state: state.add_user_chat_message(
                                        message_content=choice, role=PromptRoles.ASSISTANT))
        return user_chat_node

    @staticmethod
    def get_context_type_format_vars(args: ChatArgs, state: ChatState) -> Dict:
        """
        Creates the format vars for the context type node.
        :param args: The args to the chat
        :param state: The state of the chat.
        :return: The format vars for the context type node.
        """
        types = args.dataset.artifact_df.get_artifact_types()
        return {TYPES_FORMAT_VAR: PromptUtil.format_options(types, conjunction="and/or")}

    @staticmethod
    def run_rag(args: ChatArgs, state: ChatState) -> Set[str]:
        """
        Runs rag to find context for the chat.
        :param args: The arguments for chat.
        :param state: The current state of the chat.
        :return: The format vars for the context type node.
        """
        related_artifact_ids = ChatTreeDefinition.get_related_context(args, state)
        state.update_related_artifact_ids(related_artifact_ids, args.dataset.artifact_df, args.llm_manager)
        state.user_chat_history[-1].artifact_ids = related_artifact_ids
        return related_artifact_ids

    @staticmethod
    def get_related_context(args: ChatArgs, state: ChatState) -> Set[str]:
        """
        Extracts the artifacts related to the query.
        :param args: The arguments for chat.
        :param state: The current state of the chat.
        :return: The related artifact_ids to the user query.
        """
        query_artifact = Artifact(id=ChatTreeDefinition.QUERY_ARTIFACT_ID, content=state.user_query, layer_id="query")
        args.dataset.artifact_df.add_row(query_artifact)
        layer_ids = ChatTreeDefinition.validate_artifact_types_to_use(args, state, {query_artifact[ArtifactKeys.LAYER_ID]})
        id2context, _ = ContextFinder.find_related_artifacts(query_artifact[ArtifactKeys.ID],
                                                             args.dataset,
                                                             layer_ids=layer_ids,
                                                             base_export_dir=args.export_dir,
                                                             max_context=args.max_context)
        args.dataset.artifact_df.remove_row(query_artifact[ArtifactKeys.ID])
        return {artifact[ArtifactKeys.ID] for artifact in id2context[query_artifact[ArtifactKeys.ID]]}

    @staticmethod
    def validate_artifact_types_to_use(args: ChatArgs, state: ChatState, artifact_types_to_ignore: Set[str]):
        """
        Ensures all artifact types for context exist.
        :param args: The arguments for chat.
        :param state: The current state of the chat.
        :param artifact_types_to_ignore: Any artifact types that should not be included.
        :return: The validated artifact types.
        """
        all_artifact_types = {layer for layer in args.dataset.artifact_df[ArtifactKeys.LAYER_ID]
                              if layer not in artifact_types_to_ignore}
        layer_ids = {layer for layer in state.context_artifact_types if layer in all_artifact_types}
        state.context_artifact_types = layer_ids if layer_ids else all_artifact_types
        return state.context_artifact_types

    @staticmethod
    def create_save_and_load_path_for_node(args: ChatArgs, node_id: str) -> str:
        """
        Creates a path to save results at a given node.
        :param args: The arguments for chat.
        :param node_id: The id of the current node.
        :return: The path to save results at.
        """
        return FileUtil.safely_join_paths(args.export_dir, args.chat_id, node_id, ext=FileUtil.YAML_EXT)
