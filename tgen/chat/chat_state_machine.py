from tgen.chat.chat_args import ChatArgs
from tgen.chat.chat_tree import ChatTree
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.path import Path
from tgen.decision_tree.tree import Tree
from tgen.models.llm.abstract_llm_manager import CONTENT_KEY


class ChatStateMachine:

    def __init__(self, chat_args: ChatArgs):
        """
        Runs through each state in the chat.
        :param chat_args: Arguments required for chat.
        """
        self.tree = Tree(ChatTree.CONTEXT_TYPE_NODE)
        self.args = chat_args

    def run(self) -> Path:
        """
        Travels through the decision tree until a leaf node is reached.
        :return: The path taken to the final leaf node.
        """
        chat_history = self.args.chat_history
        user_msg = chat_history[-1].message[CONTENT_KEY]
        prompt_builder, path = self.tree.next_step(user_msg, args=self.args)
        while not path.get_node().is_leaf():
            node = path.get_node()
            if isinstance(node, LLMNode):
                chat_history[-1].message[CONTENT_KEY] = prompt_builder.build(node.llm_manager.prompt_args)[PromptKeys.PROMPT]
                res = LLMTrainer.perform_chat(node.llm_manager, chat_history,
                                              self.args.system_prompt, prompt_builder)
                choice = node.get_choice_from_response(res.predictions[0])
                path.add_decision(choice)
            prompt_builder, path = self.tree.next_step(user_msg)
        return path
