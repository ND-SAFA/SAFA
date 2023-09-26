import os
from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar, Optional

from tgen.common.constants.deliminator_constants import NEW_LINE, F_SLASH
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.state.pipeline.interactive_mode_options import InteractiveModeOptions
from tgen.state.pipeline.pipeline_args import PipelineArgs
from tgen.state.state import State

StateType = TypeVar("StateType", bound=State)
ArgType = TypeVar("ArgType", bound=PipelineArgs)

title_format_for_logs = "---{}---"


class AbstractPipelineStep(ABC, Generic[ArgType, StateType]):

    def run(self, args: ArgType, state: State, re_run: bool = False) -> bool:
        """
        Runs the step operations, modifying state in some way.
        :param args: The pipeline arguments and configuration.
        :param state: The current state of the pipeline results.
        :param re_run: If True, will run even if the step is already completed
        :return: None
        """
        step_ran = False
        if re_run or not state.step_is_complete(self.get_step_name()):
            logger.log_with_title(f"Starting step: {self.get_step_name()}", formatting=title_format_for_logs)
            self._run(args, state)
            step_ran = True
        state.on_step_complete(step_name=self.get_step_name())
        if step_ran:
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


class AbstractPipeline(ABC, Generic[ArgType, StateType]):
    INTERACTIVE_MODE_OPTIONS = [InteractiveModeOptions.RE_RUN, InteractiveModeOptions.SKIP_STEP, InteractiveModeOptions.NEXT_STEP,
                                InteractiveModeOptions.LOAD_NEW_STATE, InteractiveModeOptions.QUIT]
    NEW_STATE_OPTIONS = [InteractiveModeOptions.RE_RUN, InteractiveModeOptions.SKIP_STEP, InteractiveModeOptions.NEXT_STEP]

    def __init__(self, args: ArgType, steps: List[Type[AbstractPipelineStep]]):
        """
        Constructs pipeline of steps.
        :param steps: Steps to perform in sequential order.
        """
        self.args = args
        self.state = self.init_state()
        self.steps = [s() for s in steps]

    def init_state(self):
        """
        Creates a new state corresponding to sub-class.
        :return: The new state.
        """
        if self.args.load_dir:
            return self.state_class().load_latest(self.args.load_dir, [step.get_step_name() for step in self.steps])
        return self.state_class()()

    def run(self) -> None:
        """
        Runs steps with store.
        :return: None
        """
        for step in self.steps:
            self.run_step(step)

    def run_step(self, step: AbstractPipelineStep, re_run: bool = False) -> None:
        """
        Runs a pipeline step
        :param step: The step to run
        :param re_run: If True, runs step even if it complete
        :return: None
        """
        step.run(self.args, self.state, re_run=re_run)
        if self.args.interactive_mode:
            self._run_interactive_mode(step)

    @abstractmethod
    def state_class(self) -> Type[State]:
        """
        Gets the class used for the pipeline state.
        :return: the state class
        """

    def _run_interactive_mode(self, curr_step: AbstractPipelineStep) -> None:
        """
        Allows the user to interact with the state to rerun a step or continue the pipeline
        :param curr_step: The current step
        :return: None
        """
        next_step = self.get_next_step(curr_step)
        print(f"Current step: {curr_step.get_step_name()}, Next step: {next_step.get_step_name()}")
        selected_option = self._display_interactive_menu(self.INTERACTIVE_MODE_OPTIONS)
        if selected_option == InteractiveModeOptions.QUIT:
            exit(0)
        elif selected_option == InteractiveModeOptions.LOAD_NEW_STATE:
            new_state = self._load_new_state_from_user(self.state)
            if new_state is None:
                return self._run_interactive_mode(curr_step)
            self.state = new_state
            self._mark_next_steps_as_incomplete(curr_step)
            print("New state is reloaded - What would you like to do next?\n")
            selected_option = AbstractPipeline._display_interactive_menu(self.NEW_STATE_OPTIONS)
        if selected_option == InteractiveModeOptions.RE_RUN:
            logger.log_with_title("Re-running step")
            self.run_step(curr_step, re_run=True)
        elif selected_option == InteractiveModeOptions.SKIP_STEP:
            logger.log_with_title("Skipping next step")
            if next_step:
                self.state.mark_step_as_complete(next_step.get_step_name())

    def _mark_next_steps_as_incomplete(self, curr_step: AbstractPipelineStep) -> None:
        """
        Marks each of the next steps as incomplete so they can still be run
        :param curr_step: The current step
        :return: None
        """
        curr_step_i = self.steps.index(curr_step)
        for i, step in enumerate(self.steps):
            if i > curr_step_i:
                self.state.mark_step_as_incomplete(step.get_step_name())

    def get_next_step(self, curr_step: AbstractPipelineStep) -> AbstractPipelineStep:
        """
        Marks the next step as complete
        :param curr_step: The current step
        :return: The next step if the current step is not the last
        """
        next_index = self.steps.index(curr_step) + 1
        if next_index < len(self.steps):
            return self.steps[next_index]

    @staticmethod
    def _load_new_state_from_user(state: State) -> Optional[State]:
        """
        Allows a user to select a path from which a new state will be loaded
        :return: The path selected by the user
        """
        load_path = input("Enter the path to the new state or press 'b' to go back to the menu: \n").strip()
        if load_path.lower() == "b":
            return None
        load_path = FileUtil.expand_paths(load_path)
        if not os.path.exists(load_path):
            print(f"File not found: {load_path}")
            return AbstractPipeline._load_new_state_from_user(state)
        new_state = state.load_state_from_path(load_path)
        if isinstance(new_state, Exception):
            print(f"Loading state failed: {new_state}")
            return AbstractPipeline._load_new_state_from_user(state)
        return new_state

    @staticmethod
    def _display_interactive_menu(menu_options: List[InteractiveModeOptions]) -> InteractiveModeOptions:
        """
        Displays an interactive menu for users to select which action they would like
        :param menu_options: The different actions available to the user
        :return: The selected option
        """
        possible_choices = [str(i + 1) for i in range(len(menu_options))]
        menu = NEW_LINE.join([f"{i}) {option.value}" for i, option in zip(possible_choices, menu_options)])
        print("Menu Options: ")
        print(menu)
        choice = input(f"Select an option ({F_SLASH.join(possible_choices)}): \n").strip()
        try:
            assert choice in possible_choices
            choice = int(choice)
            selected_options = menu_options[choice - 1]
        except (TypeError, AssertionError):
            print(f"Unknown input {choice}. Please try again\n")
            selected_options = AbstractPipeline._display_interactive_menu(menu_options)
        return selected_options
