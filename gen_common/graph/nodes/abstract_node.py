import abc
from abc import abstractmethod
from typing import Any, Dict, Optional

from gen_common.graph.agents.base_agent import BaseAgent
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.io.graph_state_vars import GraphStateVars
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.str_util import StrUtil


class AbstractNode(abc.ABC):
    BASE_NAME = "Node"

    def __init__(self, graph_args: GraphArgs):
        """
        Represents a node in the graph.
        :param graph_args: Starting arguments to the graph.
        """
        self.graph_args = graph_args
        self.__agent = None

    def __call__(self, state: GraphState) -> Any:
        """
        Used to start the action of the node.
        :param state: The state of the graph.
        :return: The result of the node (generally the state).
        """
        logger.log_title(self.get_name().upper())
        run_async = GraphStateVars.RUN_ASYNC.get_value(state)
        return self.perform_action(state, run_async=run_async if run_async else False)

    @abstractmethod
    def perform_action(self, state: Dict, run_async: bool = False) -> Any:
        """
        Runs when the node is invoked.
        :param state: The current state of the graph.
        :param run_async: If True, runs in async mode else synchronously.
        :return: The result of the node (generally the state).
        """

    @classmethod
    def get_name(cls) -> str:
        """
        Gets the name of the node.
        :return: The name of the node.
        """
        name = StrUtil.remove_substring(cls.__name__, cls.BASE_NAME)
        name = StrUtil.separate_joined_words(name)
        return name

    def get_agent(self) -> Optional[BaseAgent]:
        """
        Get Agent if Node relies on an agent.
        :return: The agent
        """
        if not self.__agent:
            self.__agent = self.create_agent()
        return self.__agent

    def create_agent(self) -> Optional[BaseAgent]:
        """
        Can be overridden by children to create a special agent for that Node.
        :return: The created agent.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement a way to get agent.")
