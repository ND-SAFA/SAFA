from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from tgen.pipeline.pipeline_state import PipelineArgs, State

StateType = TypeVar("StateType", bound=State)
ArgType = TypeVar("ArgType", bound=PipelineArgs)


class AbstractPipelineStep(ABC, Generic[ArgType, StateType]):
    @abstractmethod
    def run(self, args: ArgType, state: State) -> None:
        """
        Runs the step operations, modifying state in some way.
        :param args: The pipeline arguments and configuration.
        :param state: The current state of the pipeline results.
        :return: None
        """


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

    @abstractmethod
    def init_state(self) -> StateType:
        """
        Creates a new state corresponding to sub-class.
        :return: The new state.
        """
