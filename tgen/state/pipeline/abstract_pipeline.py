from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from tgen.state.pipeline.pipeline_args import PipelineArgs
from tgen.state.state import State
from tgen.common.util.logging.logger_manager import logger

StateType = TypeVar("StateType", bound=State)
ArgType = TypeVar("ArgType", bound=PipelineArgs)


class AbstractPipelineStep(ABC, Generic[ArgType, StateType]):

    def run(self, args: ArgType, state: State, force_run: bool = False) -> None:
        """
        Runs the step operations, modifying state in some way.
        :param args: The pipeline arguments and configuration.
        :param state: The current state of the pipeline results.
        :param force_run: If True, will run even if the step is already completed
        :return: None
        """
        result = None
        if force_run or not state.step_is_complete(self.get_step_name()):
            result = self._run(args, state)
        if not force_run:
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

    @classmethod
    def get_step_name(cls) -> str:
        """
        Returns the name of the step class
        :return: The name of the step class
        """
        return cls.__name__


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
            logger.info(f"Starting step: {step.get_step_name()}")
            step.run(self.args, self.state)
            logger.info(f"Finished step: {step.get_step_name()}")

    def init_state(self):
        """
        Creates a new state corresponding to sub-class.
        :return: The new state.
        """
        if self.args.load_dir:
            return self.state_class().load_latest(self.args.load_dir, [step.get_step_name() for step in self.steps])
        return self.state_class()()

    @abstractmethod
    def state_class(self) -> Type[State]:
        """
        Gets the class used for the pipeline state.
        :return: the state class
        """
