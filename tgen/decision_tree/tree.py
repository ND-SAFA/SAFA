import abc
from typing import Tuple

from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.decision_tree.nodes.leaf_node import LeafNode
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.path import Path
from tgen.pipeline.pipeline_args import PipelineArgs
from tgen.pipeline.state import State
from tgen.prompts.prompt_builder import PromptBuilder


class Tree(abc.ABC):

    def __init__(self, starting_node: AbstractNode):
        """
        Represents the decision tree.
        :param starting_node: The root node of the tree from which all other choices branch off.
        """
        self.starting_node = starting_node

    def traverse(self, args: PipelineArgs, current_state: State) -> Path:
        """
        Travels through the decision tree until a leaf node is reached.
        :param args: The arguments to the node.
        :param current_state: Stores the current state of the tree.
        :return: The path taken to the final leaf node.
        """
        path_taken = Path(self.starting_node, args=args, state=current_state)
        node = self.starting_node
        while not node.is_leaf():
            node = self._take_step(args, current_state, node, path_taken)
        return path_taken

    def next_step(self, args: PipelineArgs, current_state: State, current_path_taken: Path = None) -> Tuple[PromptBuilder, Path]:
        """
        Take the next step from the last node in the current path.
        :param args: The arguments to the node.
        :param current_state: Stores the current state of the tree.
        :param current_path_taken: The path up until the current point.
        :return: Prompt builder if LLM Node is reached and the updated path.
        """
        current_path_taken = Path(self.starting_node, args, current_state) if not current_path_taken else current_path_taken
        current_node = current_path_taken.get_node(-1)
        prompt_builder, path = None, current_path_taken
        if isinstance(current_node, LLMNode):
            prompt_builder = current_node.create_prompt_builder(args, current_state)
        elif not isinstance(current_node, LeafNode):
            self._take_step(args, current_state, current_node, current_path_taken)
            if not current_node.is_leaf():
                prompt_builder, path = self.next_step(args, current_state, current_path_taken)
        return prompt_builder, path

    @staticmethod
    def _take_step(args: PipelineArgs, current_state: State, current_node: AbstractNode, path_taken: Path) -> AbstractNode:
        """
        Takes the next step through the tree.
        :param args: The arguments to the node.
        :param current_state: Stores the current state of the tree.
        :param current_node: The current node.
        :param path_taken: The path up to the current node.
        :return: The next node to take.
        """
        choice = current_node.make_choice(args, current_state)
        if choice:
            current_node = path_taken.add_decision(choice)
        return current_node
