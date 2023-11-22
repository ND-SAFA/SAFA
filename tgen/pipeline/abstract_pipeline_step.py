from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from tgen.common.logging.logger_manager import logger
from tgen.pipeline.pipeline_args import PipelineArgs

from tgen.pipeline.state import State


StateType = TypeVar("StateType", bound=State)
ArgType = TypeVar("ArgType", bound=PipelineArgs)
title_format_for_logs = "---{}---"


class AbstractPipelineStep(ABC, Generic[ArgType, StateType]):

    def run(self, args: ArgType, state: State, re_run: bool = False, verbose: bool = True) -> bool:
        """
        Runs the step operations, modifying state in some way.
        :param args: The pipeline arguments and configuration.
        :param state: The current state of the pipeline results.
        :param re_run: If True, will run even if the step is already completed
        :param verbose: If True, prints logs
        :return: None
        """
        step_ran = False
        if re_run or not state.step_is_complete(self.get_step_name()):
            if verbose:
                logger.log_with_title(f"Starting step: {self.get_step_name()}", formatting=title_format_for_logs)
            self._run(args, state)
            step_ran = True
        if step_ran:
            state.on_step_complete(step_name=self.get_step_name())
            if verbose:
                logger.log_with_title(f"Finished step: {self.get_step_name()}", formatting=title_format_for_logs)
        return step_ran

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
