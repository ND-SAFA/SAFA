from copy import deepcopy
from typing import Dict, List

from common_resources.graph.graph_builder import GraphBuilder
from common_resources.graph.graph_definition import GraphDefinition
from common_resources.graph.io.graph_args import GraphArgs
from common_resources.graph.io.graph_state import GraphState
from common_resources.graph.llm_tools.tool_models import RequestAssistance
from common_resources.graph.nodes.generate_node import AnswerUser
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.json_util import JsonUtil


class GraphRunner:
    CONFIG = {"configurable": {"thread_id": "1"}}

    def __init__(self, graph_definition: GraphDefinition, state_type: GraphState = GraphState, **config):
        """
        Handles running the graph and storing states.
        :param graph_definition: Defines the nodes and edges of the graph.
        :param builder: Responsible for building the graph.
        :param state_type: The type of state class to use.
        :param config: Arguments for the config.
        """
        self.graph_definition = graph_definition
        self.state_type = state_type
        self.config = deepcopy(self.CONFIG)
        self.config["configurable"].update(config)

        self.states_for_runs: Dict[int, List[GraphState]] = {}
        self.nodes_visited_on_runs: Dict[int, List[str]] = {}
        self.run_num = 0

    def run(self, args: GraphArgs, verbose: bool = False) -> AnswerUser | RequestAssistance:
        """
        Runs the graph based on the input.
        :param args: Args to the graph.
        :param verbose: If True, prints the state at each time step.
        :return: The final generation.
        """
        graph_input = args.to_graph_input(self.state_type)
        builder = GraphBuilder(self.graph_definition, args)
        app = builder.build()
        nodes_visited = []
        run_states = []

        value: GraphState = {}
        for output in app.stream(graph_input, self.config):
            for key, value in output.items():
                if verbose:
                    logger.info(f'Current state:\n{JsonUtil.dict_to_json(value)}')
                nodes_visited.append(key)
                run_states.append(value)

        self.nodes_visited_on_runs[self.run_num] = nodes_visited
        self.states_for_runs[self.run_num] = run_states
        self.run_num += 1
        if value.get("generation"):
            return AnswerUser(answer=value.get("generation"), reference_ids=value.get("reference_ids"))
        elif value.get("relevant_information_learned"):
            return RequestAssistance(relevant_information_learned=value.get("relevant_information_learned"),
                                     related_doc_ids=value.get("related_doc_ids"))
        logger.error("LLM was unable to answer question.")

    def get_nodes_visited_on_last_run(self) -> List[str]:
        """
        Gets a list of the names of the nodes visited on the last run.
        :return: A list of the names of the nodes visited on the last run.
        """
        return self._extract_data_from_last_run(self.nodes_visited_on_runs)

    def get_states_from_last_run(self) -> List[str]:
        """
        Gets a list of the states from the last run.
        :return: A list of the states from the last run.
        """
        return self._extract_data_from_last_run(self.states_for_runs)

    def clear_run_history(self) -> None:
        """
        Clears prior run history.
        :return: None.
        """
        self.nodes_visited_on_runs.clear()
        self.states_for_runs.clear()
        self.run_num = 0

    def _extract_data_from_last_run(self, run_data: Dict[int, List]) -> List:
        """
        Extracts the data from the dictionary containing information from the last run.
        :param run_data: A dictionary mapping run num to the corresponding data.
        :return: The data from the last run.
        """
        if (self.run_num - 1) in run_data:
            return run_data[self.run_num - 1]
