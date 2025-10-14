import asyncio
import uuid
from typing import Any, Dict, List

from langgraph.constants import START

from gen_common.graph.graph_builder import GraphBuilder
from gen_common.graph.graph_definition import GraphDefinition
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.io.graph_state import GraphState
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.dict_util import DictUtil
from gen_common.util.json_util import JsonUtil


class GraphRunner:

    def __init__(self, graph_definition: GraphDefinition, state_type: GraphState = GraphState, **config_settings):
        """
        Handles running the graph and storing states.
        :param graph_definition: Defines the nodes and edges of the graph.
        :param builder: Responsible for building the graph.
        :param state_type: The type of state class to use.
        :param config_settings: Arguments for the config.
        """
        self.graph_definition = graph_definition
        self.state_type = state_type
        self.config_settings = config_settings
        self.states_for_runs: Dict[int, List[GraphState]] = {}
        self.nodes_visited_on_runs: Dict[int, List[str]] = {}
        self.run_num = 0

    def run_multi(self, args: GraphArgs, thread_ids: List[str] = None, **changing_params) -> List[Any | GraphState | None]:
        """
        Run graph with multiple different arguments.
        :param args: The unchanging params for the graph.
        :param thread_ids: If provided, uses as the ids of each thread.
        :param changing_params: Lists of params that are changing per run.
        :return: List of outputs from each run (in the same order as the given params).
        """
        builder = GraphBuilder(self.graph_definition, args)
        app = builder.build()

        thread_ids = self._assert_n_runs(thread_ids, **changing_params)

        initial_states = []
        for i in range(len(thread_ids)):
            params = {k: v[i] for k, v in changing_params.items()}
            initial_state = args.to_graph_input(self.state_type, run_async=True, thread_id=thread_ids[i],
                                                **params)
            initial_states.append(initial_state)
        configs = [self.create_new_config(thread_id=t_id) for t_id in thread_ids]
        outputs = [self.__get_async_result(app, state, config) for state, config in zip(initial_states, configs)]
        self._save_state_history(app, configs)
        return outputs

    def run(self, args: GraphArgs, verbose: bool = False) -> Any | GraphState | None:
        """
        Runs the graph based on the input.
        :param args: Args to the graph.
        :param verbose: If True, prints the state at each time step.
        :return: The final generation.
        """
        graph_input = args.to_graph_input(self.state_type)
        builder = GraphBuilder(self.graph_definition, args)
        app = builder.build()
        nodes_visited = [START]
        run_states = []

        state: GraphState = {}
        config = self.create_new_config()
        for output in app.stream(graph_input, config=config):
            for key, state in output.items():
                if verbose:
                    logger.info(f'Current state:\n{JsonUtil.dict_to_json(state)}')
                nodes_visited.append(key)
                run_states.append(state)

        self._update_state_history(nodes_visited, run_states)

        output = self._convert_graph_output(state)

        if output is None:
            logger.error("LLM was unable to answer question.")
        return output

    def create_new_config(self, thread_id: str = None) -> Dict[str, Dict]:
        """
        Creates a new config (with new thread id).
        :param thread_id: Optionally provide an id for the thread.
        :return: The configuration dictionary.
        """
        thread_id = uuid.uuid4() if not thread_id else thread_id
        config = {"configurable":
                      {"thread_id": thread_id,
                       **self.config_settings}
                  }
        return config

    @staticmethod
    def get_id_from_config(config: Dict[str, Dict]) -> str:
        """
        Gets the thread id from the config.
        :param config: The configuration dictionary.
        :return: The thread id.
        """
        return config["configurable"]["thread_id"]

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

    def _convert_graph_output(self, final_state: GraphState) -> Any | GraphState | None:
        """
        Converts the final graph output to expected format if a converter is provided. Otherwise, final state is returned unchanged.
        :param final_state: The final state of the graph.
        :return: The formatted output or the final graph state depending on if an output converter is provided.
        """
        output = final_state
        if (output_converter := self.graph_definition.output_converter) is not None:
            output = output_converter(final_state)
        return output

    def _update_state_history(self, nodes_visited: List[str], states: List[Dict]) -> None:
        """
        Updates the nodes visited and states for the current run.
        :param nodes_visited: List of nodes visited on run.
        :param states: List of states from the run.
        :return: none
        """
        self.nodes_visited_on_runs[self.run_num] = nodes_visited
        self.states_for_runs[self.run_num] = states
        self.run_num += 1

    def _save_state_history(self, app: "CompiledGraph", configs: List[Dict[str, Dict]]) -> bool:
        """
        Saves the states and nodes that were visited during each graph run.
        :param app: The compiled graph.
        :param configs: List of configs for each run.
        :return: True if save was successful else False.
        """
        try:
            run_snapshots = [list(app.get_state_history(config)) for config in configs]
            run_nodes_visited = [[ss.next[0] for ss in snapshots if len(ss.next) > 0] for snapshots in run_snapshots]
            run_states = [[ss.metadata["writes"] for ss in snapshots if ss.metadata["writes"]] for snapshots in run_snapshots]
            for nodes_visited, states in zip(run_nodes_visited, run_states):
                states = [state.get(node, state) for node, state in zip(nodes_visited, states)]
                self._update_state_history(nodes_visited, states)
            return True
        except Exception:
            logger.exception("Saving state history failed.")
            return False

    @staticmethod
    def _assert_n_runs(thread_ids: List[str] = None, **changing_params) -> List[str | None]:
        """
        Asserts same number of params and thread ids since they represent the number of runs.
        :param thread_ids: If provided, uses as the ids of each thread.
        :param changing_params: Lists of params that are changing per run.
        :return: The thread ids if provided else placeholder for each run.
        """
        n = len(DictUtil.get_value_by_index(changing_params))
        assert all([len(param) == n for param in changing_params.values()]), "Changing params must all be of the same length"
        thread_ids = [None for _ in range(n)] if not thread_ids else thread_ids
        assert len(thread_ids) == n, f"Number of thread ({len(thread_ids)}) ids must be the same as the number of params ({n})"
        return thread_ids

    def __get_async_result(self, app: "CompiledGraph", initial_state: GraphState,
                           config: Dict[str, Dict]) -> Any | GraphState | None:
        """
        Runs the graph async and returns the final state.
        :param app: The compiled graph to run.
        :param initial_state: Input to the graph.
        :param config: The configuration for the graph.
        :return: The final state of the graph.
        """
        try:
            final_state = asyncio.run(app.ainvoke(initial_state, config=config))
            return self._convert_graph_output(final_state)
        except Exception:
            logger.exception(f"Graph run {self.get_id_from_config(config)} has failed.")
            pass
