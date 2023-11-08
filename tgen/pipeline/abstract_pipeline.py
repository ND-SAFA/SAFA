import os
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Generic, List, Optional, Type, TypeVar

from tgen.common.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.pipeline.interactive_mode_options import InteractiveModeOptions
from tgen.pipeline.pipeline_args import PipelineArgs
from tgen.pipeline.state import State
from tgen.scripts.toolset.selector import inquirer_selection, inquirer_value
from tgen.summarizer.summarizer import Summarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summary import Summary

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
        if step_ran:
            state.on_step_complete(step_name=self.get_step_name())
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
                                InteractiveModeOptions.LOAD_NEW_STATE,
                                InteractiveModeOptions.TURN_OFF_INTERACTIVE]

    def __init__(self, args: ArgType, steps: List[Type[AbstractPipelineStep]], summarizer_args: SummarizerArgs = None,
                 skip_summarization: bool = False, **summarizer_args_kwargs):
        """
        Constructs pipeline of steps.
        :param steps: Steps to perform in sequential order.
        :param summarizer_args: The args used to create project summary
        :param summarizer_args_kwargs: Keyword arguments to summarizer to customize default settings.
        """
        self.args = args
        self.steps = [s() for s in steps]
        self.summarizer_args = SummarizerArgs(do_resummarize_project=False,
                                              summarize_code_only=True,
                                              do_resummarize_artifacts=False,
                                              **summarizer_args_kwargs) if not summarizer_args else summarizer_args
        self.resume_interactive_mode_step = None
        if skip_summarization:
            self.summarizer_args = None
        self.state: StateType = self.init_state()
        if self.args.export_dir:
            os.makedirs(self.args.export_dir, exist_ok=True)
            self.state.export_dir = self.args.export_dir

    def init_state(self) -> StateType:
        """
        Creates a new state corresponding to sub-class.
        :return: The new state.
        """
        if not self.args.load_dir:
            self.args.load_dir = self.args.export_dir
        if self.args.load_dir:
            return self.state_class().load_latest(self.args.load_dir, self.get_step_names())
        return self.state_class()()

    def run(self) -> None:
        """
        Runs steps with store.
        :return: None
        """
        self.run_setup_for_pipeline()
        self._run_interactive_mode()
        for step in self.steps:
            self.run_step(step)
        self._log_costs()

    def run_setup_for_pipeline(self) -> None:
        """
        Runs anything that is needed before the pipeline begins
        :return: None
        """
        self.args.update_llm_managers_with_state(self.state)
        if self.summarizer_args:
            self.summarizer_args: SummarizerArgs
            self.summarizer_args.update_llm_managers_with_state(self.state)
            self.run_summarizations()

    def run_summarizations(self) -> Summary:
        """
        Runs the summarizer to create pipeline project summary and summarize artifacts
        :return: The project summary
        """
        self.summarizer_args.update_export_dir(self.state.export_dir)
        dataset = Summarizer(self.summarizer_args, dataset=self.args.dataset).summarize()
        if not self.args.dataset.project_summary:
            self.args.dataset = dataset
        else:
            self.args.dataset.update_artifact_df(dataset.artifact_df)  # keep original project summary
        self.state.project_summary = dataset.project_summary if dataset.project_summary else None
        return self.state.project_summary

    def run_step(self, step: AbstractPipelineStep, re_run: bool = False) -> None:
        """
        Runs a pipeline step
        :param step: The step to run
        :param re_run: If True, runs step even if it complete
        :return: None
        """
        step.run(self.args, self.state, re_run=re_run)
        if step.get_step_name() == self.resume_interactive_mode_step:
            self.args.interactive_mode = True
        if self.args.interactive_mode:
            self._run_interactive_mode(step)

    def get_remaining_steps(self, curr_step: AbstractPipelineStep) -> List[str]:
        """
        Gets a list of the steps that are remaining in the pipeline
        :param curr_step: The step the pipeline is currently at
        :return: The steps that are remaining in the pipeline
        """
        next_index = self.steps.index(curr_step) + 1
        return self.get_step_names(self.steps[next_index:])

    def get_step_names(self, steps: List[AbstractPipelineStep] = None) -> List[str]:
        """
        Gets the names of all steps in the list
        :param steps: The list of steps to get names for
        :return: The names of all steps in the list
        """
        steps = self.steps if not steps else steps
        return [step.get_step_name() for step in steps]

    @abstractmethod
    def state_class(self) -> Type[State]:
        """
        Gets the class used for the pipeline state.
        :return: the state class
        """

    def _run_interactive_mode(self, curr_step: AbstractPipelineStep = None) -> None:
        """
        Allows the user to interact with the state to rerun a step or continue the pipeline
        :param curr_step: The current step
        :return: None
        """
        options = deepcopy(self.INTERACTIVE_MODE_OPTIONS)
        if curr_step is None:
            next_step = self.get_next_step(self.steps[0])
            options.remove(InteractiveModeOptions.RE_RUN)
            msg = EMPTY_STRING
        else:
            next_step = self.get_next_step(curr_step)
            msg = f"Current step: {curr_step.get_step_name()}, "
        logger.info(f"{msg}Next step: {next_step.get_step_name()}")
        selected_option = self._display_interactive_menu(options)
        if selected_option == InteractiveModeOptions.LOAD_NEW_STATE:
            selected_option = self._option_new_state(curr_step)
        if selected_option == InteractiveModeOptions.RE_RUN:
            logger.log_with_title("Re-running step")
            self.run_step(curr_step, re_run=True)
        elif selected_option == InteractiveModeOptions.SKIP_STEP:
            logger.log_with_title("Skipping next step")
            if next_step:
                self.state.mark_step_as_complete(next_step.get_step_name())
        elif selected_option == InteractiveModeOptions.TURN_OFF_INTERACTIVE:
            resume_interactive_mode_step = self._option_turn_off_interactive(curr_step)
            if not resume_interactive_mode_step:
                selected_option = None
            elif resume_interactive_mode_step != InteractiveModeOptions.DO_NOT_RESUME.value:
                self.resume_interactive_mode_step = resume_interactive_mode_step
                self.args.interactive_mode = False
        if selected_option is None:
            self._run_interactive_mode(curr_step)

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

    def _option_new_state(self, curr_step: AbstractPipelineStep) -> INTERACTIVE_MODE_OPTIONS:
        """
        Runs the new state loading when the option is selected
        :param curr_step: The current step the user is one
        :return: The selected next step
        """
        load_external_option = InteractiveModeOptions.LOAD_EXTERNAL_STATE.value
        steps = self.get_remaining_steps(curr_step) + [load_external_option]
        step_to_load_from = inquirer_selection(selections=steps,
                                               message="What step state do you want to load from?",
                                               allow_back=True) if self.args.load_dir else load_external_option
        if step_to_load_from is None:
            return None
        load_path = self._get_state_load_path(step_to_load_from)
        if load_path is None:
            return self._option_new_state(curr_step) if self.args.load_dir else None
        if not os.path.exists(load_path):
            logger.warning(f"File not found: {load_path}")
            return AbstractPipeline._option_new_state(self.state)
        new_state = self.state.load_state_from_path(load_path)
        if isinstance(new_state, Exception):
            logger.warning(f"Loading state failed: {new_state}")
            return AbstractPipeline._option_new_state(self.state)
        if new_state is None:
            return None
        self.state = new_state
        self._mark_next_steps_as_incomplete(curr_step)
        self._optional_delete_old_state_files(step_to_load_from)
        return AbstractPipeline._display_interactive_menu([o for o in self.INTERACTIVE_MODE_OPTIONS
                                                           if o != InteractiveModeOptions.LOAD_NEW_STATE],
                                                          message="New state is reloaded - What would you like to do next?\n",
                                                          allow_back=True)

    def _get_state_load_path(self, step_to_load_from: str) -> str:
        """
        Determines the path of the state to load
        :param step_to_load_from: The state step to load the state for
        :return:
        """
        if step_to_load_from == InteractiveModeOptions.LOAD_EXTERNAL_STATE.value:
            load_path = inquirer_value("Enter the path to the new state: ", str, allow_back=True)
            load_path = FileUtil.expand_paths(load_path.strip()) if load_path else load_path
        else:
            load_step_num = self.get_step_names().index(step_to_load_from)
            load_path = self.state.get_path_to_state_checkpoint(self.args.load_dir, step_to_load_from,
                                                                step_num=load_step_num)
        return load_path

    def _optional_delete_old_state_files(self, step_to_load_from: str) -> None:
        """
        Allows the user to delete all the state files that are now outdated
        :param step_to_load_from: The step that the state was just loaded from
        :return: None
        """
        load_step_num = self.get_step_names().index(step_to_load_from)
        if not self.args.load_dir or step_to_load_from == InteractiveModeOptions.LOAD_EXTERNAL_STATE.value \
                or load_step_num + 1 >= len(self.steps):
            return
        should_delete = inquirer_value("Delete old state files? (Y/N): ", str)
        if should_delete:
            step_names = self.get_step_names()
            self.state.delete_state_files(self.args.load_dir, step_names=step_names,
                                          step_to_delete_from=step_names[load_step_num + 1])

    def _option_turn_off_interactive(self, curr_step: AbstractPipelineStep) -> Optional[str]:
        """
        Turns off interactive mode
        :param curr_step: The current step
        :return: The step at which to resume interactive mode
        """
        steps = self.get_remaining_steps(curr_step)
        if not steps:
            return InteractiveModeOptions.DO_NOT_RESUME.value
        selections = [InteractiveModeOptions.DO_NOT_RESUME.value] + steps
        choice = inquirer_selection(selections=selections, message="Would you like to resume after a later step? ", allow_back=True)
        if choice is None:
            return None
        return choice

    @staticmethod
    def _display_interactive_menu(menu_options: List[InteractiveModeOptions], message: str = None,
                                  allow_back: bool = True) -> InteractiveModeOptions:
        """
        Displays an interactive menu for users to select which action they would like
        :param menu_options: The different actions available to the user
        :param allow_back: If True, allows user to go to previous menu
        :return: The selected option
        """
        message = "Menu Options: " if not message else message
        choice = inquirer_selection(selections=[mo.value for mo in menu_options], message=message, allow_back=allow_back)
        return InteractiveModeOptions[choice.upper()] if choice else choice

    def _log_costs(self) -> None:
        """
        Logs the costs accumulated during the run
        :return: None
        """
        total_cost = self.state.total_input_cost + self.state.total_output_cost
        if total_cost > 0:
            costs = {"Input": self.state.total_input_cost,
                     "Output": self.state.total_output_cost,
                     "Total": total_cost}
            cost_msg = "{} Token Cost: ${}"
            cost_msgs = [cost_msg.format(name, "%.2f" % cost) for name, cost in costs.items()]
            logger.log_with_title("COSTS FOR RUN: ", NEW_LINE.join(cost_msgs))
