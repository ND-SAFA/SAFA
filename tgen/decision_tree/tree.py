import abc
from typing import Any, Tuple

from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.path import Path
from tgen.prompts.prompt_builder import PromptBuilder


class Tree(abc.ABC):

    def __init__(self, starting_node: AbstractNode):
        """
        Represents the decision tree.
        :param starting_node: The root node of the tree from which all other choices branch off.
        """
        self.starting_node = starting_node

    def traverse(self, input_: Any) -> Path:
        """
        Travels through the decision tree until a leaf node is reached.
        :param input_: The input to make the decision on.
        :return: The path taken to the final leaf node.
        """
        path_taken = Path(self.starting_node, input_)
        node = self.starting_node
        while not node.is_leaf():
            node = self._take_step(input_, node, path_taken)
        return path_taken

    def next_step(self, input_: Any, current_path_taken: Path = None, **kwargs) -> Tuple[PromptBuilder, Path]:
        """
        Take the next step from the last node in the current path.
        :param input_: The input to the node.
        :param current_path_taken: The path up until the current point.
        :param kwargs: Any additional arguments needed to make decision.
        :return: Prompt builder if LLM Node is reached and the updated path.
        """
        current_path_taken = Path(self.starting_node, input_) if not current_path_taken else current_path_taken
        current_node = current_path_taken.get_node(-1)
        if current_node.is_leaf():
            prompt_builder = None
            path = current_path_taken
        elif isinstance(current_node, LLMNode):
            prompt_builder = current_node.create_prompt_builder(input_, **kwargs)
            path = current_path_taken
        else:
            self._take_step(input_, current_node, current_path_taken, **kwargs)
            prompt_builder, path = self.next_step(input_, current_path_taken)
        return prompt_builder, path

    @staticmethod
    def _take_step(input_: Any, current_node: AbstractNode, path_taken: Path, **kwargs) -> AbstractNode:
        """
        Takes the next step through the tree.
        :param input_: The input to make the decision on.
        :param current_node: The current node.
        :param path_taken: The path up to the current node.
        :param kwargs: Any additional arguments needed to make choice.
        :return: The next node to take.
        """
        choice = current_node.make_choice(input_, **kwargs)
        if choice:
            current_node = path_taken.add_decision(choice)
        return current_node
