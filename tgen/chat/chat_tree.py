from typing import Dict, Set

from tgen.chat.chat_args import ChatArgs
from tgen.chat.chat_state import ChatState
from tgen.common.constants.deliminator_constants import COMMA
from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.common_choices import CommonChoices
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.decision_tree.nodes.action_node import ActionNode
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.models.llm.abstract_llm_manager import PromptRoles
from tgen.prompts.supported_prompts.chat_prompts import INCLUDE_MORE_CONTEXT_PROMPT, ARTIFACT_TYPE_FOR_CONTEXT_PROMPT
from tgen.tracing.context_finder import ContextFinder


class ChatTree:
    QUERY_ARTIFACT_ID = "query"

    @staticmethod
    def construct_tree() -> AbstractNode:
        """
        Constructs the decision tree used for chat.
        :return: The root node.
        """
        CHAT_NODE = ActionNode(description="Perform Chat", action_method=lambda args, state: LLMTrainer.perform_chat(
            llm_manager=args.llm_manager, chat_history=state.user_chat_history, system_prompts=state.system_prompt,
            save_and_load_path=ChatTree.create_save_and_load_path_for_node(args, "chat_node")
        ).predictions[0], state_setter=lambda choice, state: state.add_user_chat_message(message_content=choice,
                                                                                         role=PromptRoles.ASSISTANT),
                               node_id="chat_node")
        RAG_NODE = ActionNode(description="Run Rag", action_method=ChatTree.run_rag, branches=CHAT_NODE, node_id="rag_node")
        CONTEXT_TYPE_NODE = LLMNode(description=ARTIFACT_TYPE_FOR_CONTEXT_PROMPT.value,
                                    input_variable_converter=ChatTree.get_context_type_format_vars,
                                    response_manager_params={
                                        "value_formatter": lambda tag, value: [v.strip() for v in value.split(COMMA)]},
                                    state_setter="context_artifact_types",
                                    branches=RAG_NODE, node_id="context_type_node")
        STARTING_NODE = LLMNode(description=INCLUDE_MORE_CONTEXT_PROMPT.value, branches={CommonChoices.YES: CONTEXT_TYPE_NODE,
                                                                                         CommonChoices.NO: CHAT_NODE},
                                node_id="include_context_node")
        return STARTING_NODE

    @staticmethod
    def get_context_type_format_vars(args: ChatArgs, state: ChatState) -> Dict:
        """
        Creates the format vars for the context type node.
        :param args: The args to the chat
        :param state: The state of the chat.
        :return: The format vars for the context type node.
        """
        types = args.dataset.artifact_df.get_artifact_types()
        return {"types": PromptUtil.format_options(types, conjunction="and/or")}

    @staticmethod
    def run_rag(args: ChatArgs, state: ChatState) -> Set[str]:
        """
        Runs rag to find context for the chat.
        :param args: The arguments for chat.
        :param state: The current state of the chat.
        :return: The format vars for the context type node.
        """
        related_artifact_ids = ChatTree.get_related_context(args, state)
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
        query_artifact = Artifact(id=ChatTree.QUERY_ARTIFACT_ID, content=state.user_query, layer_id="query")
        args.dataset.artifact_df.add_row(query_artifact)
        id2context, _ = ContextFinder.find_related_artifacts(query_artifact[ArtifactKeys.ID],
                                                             args.dataset,
                                                             layer_ids={layer for layer in state.context_artifact_types
                                                                        if layer in
                                                                        set(args.dataset.artifact_df[ArtifactKeys.LAYER_ID])},
                                                             base_export_dir=args.export_dir,
                                                             max_context=args.max_context)
        args.dataset.artifact_df.remove_row(query_artifact[ArtifactKeys.ID])
        return {artifact[ArtifactKeys.ID] for artifact in id2context[query_artifact[ArtifactKeys.ID]]}

    @staticmethod
    def create_save_and_load_path_for_node(args: ChatArgs, node_id: str) -> str:
        """
        Creates a path to save results at a given node.
        :param args: The arguments for chat.
        :param node_id: The id of the current node.
        :return: The path to save results at.
        """
        return FileUtil.safely_join_paths(args.export_dir, args.chat_id, node_id, ext=FileUtil.YAML_EXT)
