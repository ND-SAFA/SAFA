from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from tgen.state.pipeline.pipeline_args import PipelineArgs
from tgen.state.state import State
from tgen.common.util.logging.logger_manager import logger

StateType = TypeVar("StateType", bound=State)
ArgType = TypeVar("ArgType", bound=PipelineArgs)


class AbstractPipelineStep(ABC, Generic[ArgType, StateType]):

    def run(self, args: ArgType, state: State) -> None:
        """
        Runs the step operations, modifying state in some way.
        :param args: The pipeline arguments and configuration.
        :param state: The current state of the pipeline results.
        :return: None
        """
        if state.step_is_complete(self.get_step_name()):
            return
        result = self._run(args, state)
        state.on_step_complete(step_name=self.get_step_name())
        return result

    @abstractmethod
    def _run(self, args: ArgType, state: State) -> None:
        """
        Runs the step operations, modifying state in some way.
        :param args: The pipeline arguments and configuration.
        :param state: The current state of the pipeline results.
        :return: None
        """
        if state.step_is_complete(self.get_step_name()):
            return

    def get_step_name(self) -> str:
        """
        Returns the name of the step class
        :return: The name of the step class
        """
        return self.__class__.__name__


class AbstractPipeline(ABC, Generic[ArgType, StateType]):

    def __init__(self, args: ArgType, steps: List[Type[AbstractPipelineStep]]):
        """
        Constructs pipeline of steps.
        :param steps: Steps to perform in sequential order.
        """
        self.args = args
        self.state = self.init_state()
        self.steps = [s() for s in steps]

    def run(self) -> None:
        """
        Runs steps with store.
        :return: None
        """
        for step in self.steps:
            step.run(self.args, self.state)
            logger.info(f"Finished step: {step.__class__.__name__}")

    @abstractmethod
    def init_state(self) -> StateType:
        """
        Creates a new state corresponding to sub-class.
        :return: The new state.
        """
