from collections.abc import Set

from tgen.chat.chat_args import ChatArgs
from tgen.chat.chat_state import ChatState
from tgen.chat.chat_tree_definition import ChatTreeDefinition
from tgen.core.trainers.llm_trainer import LLMTrainer
from common_resources.data.keys.prompt_keys import PromptKeys
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.path import Path


class ChatStateMachine:

    def __init__(self, args: ChatArgs, nodes2skip: Set[str] = None):
        """
        Runs through each state in the chat.
        :param args: Arguments required for chat.
        :param nodes2skip: Set of node ids that should be skipped.
        """
        self.tree = ChatTreeDefinition(root_node_id=args.root_node_id, nodes2skip=nodes2skip).get_tree()
        self.args = args
        self.state = ChatState(user_chat_history=self.args.chat_history)
        self.state.update_related_artifact_ids(additional_artifact_ids={a for meta in self.args.chat_history
                                                                        for a in meta.artifact_ids},
                                               artifact_df=self.args.dataset.artifact_df, llm_manager=self.args.llm_manager)

    def run(self) -> Path:
        """
        Travels through the decision tree until a leaf node is reached.
        :return: The path taken to the final leaf node.
        """
        prompt_builder, path = self.tree.next_step(self.args, current_state=self.state)
        while not path.get_node().is_leaf():
            node = path.get_node()
            if isinstance(node, LLMNode):
                next_prompt = prompt_builder.build(node.llm_manager.prompt_args)[PromptKeys.PROMPT]
                chat_history = self.state.add_internal_chat_message(next_prompt, replace_last=True)
                res = LLMTrainer.perform_chat(node.llm_manager, chat_history,
                                              self.state.system_prompt, prompt_builder,
                                              save_and_load_path=ChatTreeDefinition.create_save_and_load_path_for_node(self.args,
                                                                                                                       node.node_id))
                choice = node.get_choice_from_response(res.predictions[0])
                path.add_decision(choice)
            prompt_builder, path = self.tree.next_step(self.args, self.state, path)
        return path
