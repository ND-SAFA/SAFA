from abc import abstractmethod
from typing import Dict, List, Any

from gen_common.graph.branches.base_branch import BaseBranch
from gen_common.graph.branches.paths.path_choices import PathChoices
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.nodes.supported_nodes import SupportedNodes
from gen_common.util.supported_enum import SupportedEnum


class LLMBranch(BaseBranch):

    def __init__(self, graph_args: GraphArgs, response_tag: str = None, additional_paths: PathChoices = None):
        """
        Represents branches that should be taken based on the response from the LLM.
        :param graph_args: Arguments to the graph.
        :param response_tag: The expected tag to get the response from LLM.
        :param additional_paths: A list of additional paths that can be taken based on the state.
        """
        super().__init__(graph_args=graph_args)
        self.response_tag = response_tag if response_tag else self.get_agent().get_first_response_tag()
        self.additional_paths = additional_paths if additional_paths else PathChoices()

    def perform_action(self, state: Dict) -> Any:
        """
        Chooses what node to go to next based on the response from the LLM.
        :param state: The current state of the graph.
        :return: The name of the next node to visit.
        """
        response = self.get_agent().respond(state)
        chosen = self.get_agent().extract_answer(response)
        default = self.response_map.get(chosen, self.path_choices.default)
        if not self.path_choices.paths or state is None:
            return default.name if isinstance(default, SupportedEnum) else default
        return self.choose_path(state, default=default)

    def get_node_choices(self) -> List[SupportedNodes]:
        """
        Gets all possible next node choices.
        :return: All possible next node choices.
        """
        node_choices = super().get_node_choices()
        node_choices.extend(self.response_map.values())
        return node_choices

    @property
    @abstractmethod
    def response_map(self) -> Dict[str, SupportedNodes]:
        """
        Maps LLM response to node to visit if that response is given.
        :return: Dictionary mapping LLM response to node to visit if that response is given.
        """

    @property
    def path_choices(self) -> PathChoices:
        """
        Contains all other paths that can be taken based on the state if not relying solely on llm output.
        :return:  All other paths that can be taken based on the state if not relying solely on llm output.
        """
        return self.additional_paths
