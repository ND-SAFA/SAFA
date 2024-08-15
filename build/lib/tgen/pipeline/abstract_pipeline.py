import os
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Set, Tuple, Type

from common_resources.tools.cli.confirm import confirm
from common_resources.tools.cli.inquirer_selector import inquirer_selection, inquirer_value
from common_resources.tools.constants.symbol_constants import EMPTY_STRING, NEW_LINE
from common_resources.tools.state_management.state import State
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.enum_util import EnumUtil
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.reflection_util import ReflectionUtil

from tgen.common.constants import tgen_constants
from tgen.common.constants.pipeline_constants import DEFAULT_INTERACTIVE_STATE
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep, ArgType, StateType, title_format_for_logs
from tgen.pipeline.interactive_mode_options import InteractiveModeOptions
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summary import Summary


class AbstractPipeline(ABC, Generic[ArgType, StateType]):
    INTERACTIVE_MODE_OPTIONS = [InteractiveModeOptions.NEXT_STEP, InteractiveModeOptions.RE_RUN,
                                InteractiveModeOptions.LOAD_NEW_STATE, InteractiveModeOptions.DELETE_MODEL_OUTPUT,
                                InteractiveModeOptions.TURN_OFF_INTERACTIVE]

    def __init__(self, args: ArgType, steps: List[Type[AbstractPipelineStep]], summarizer_args: SummarizerArgs = None,
                 skip_summarization: bool = False, log_state_exception: bool = True, **summarizer_args_kwargs):
        """
        Constructs pipeline of steps.
        :param args: The arguments to the pipeline.
        :param steps: Steps to perform in sequential order.
        :param summarizer_args: The args used to create project summary
        :param summarizer_args_kwargs: Keyword arguments to summarizer to customize default settings.
        :param skip_summarization: Whether to skip summarization of artifacts.
        :param log_state_exception: If True, logs any exceptions thrown while init state, else fails silently
        """
        self.args = args
        self.steps = [s() for s in steps]
        self.summarizer_args = SummarizerArgs(
            summarize_code_only=True,
            do_resummarize_artifacts=False,
            **summarizer_args_kwargs) if not summarizer_args else summarizer_args
        self.resume_interactive_mode_step = None
        if skip_summarization:
            self.summarizer_args = None
        self.log_state_exception = log_state_exception
        self.state: StateType = self.init_state()
        self.artifact_summaries_costs = 0
        self.project_summary_costs = 0
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
            return self.state_class().load_latest(self.args.load_dir, self.get_step_names(), self.log_state_exception)
        return self.state_class()()

    def run(self, run_setup: bool = True, log_start: bool = True) -> None:
        """
        Runs steps with store.
        :param run_setup: If True, runs the necessary setup before running the pipeline
        :param log_start: If True, logs that the pipeline is starting
        :return: None
        """
        if log_start:
            logger.log_with_title(f"{self.get_pipeline_name().upper()}", formatting=NEW_LINE + title_format_for_logs)
        if run_setup:
            self.run_setup_for_pipeline()
        for step in self.steps:
            re_run_pipeline = self.run_step(step)
            if re_run_pipeline:
                self.run(run_setup=False)
                return
        self._log_costs()

    def run_setup_for_pipeline(self) -> None:
        """
        Runs anything that is needed before the pipeline begins
        :return: None
        """
        self.args.update_llm_managers_with_state(self.state)
        if self.summarizer_args:
            self.summarizer_args: SummarizerArgs
            self.run_summarizations()
        if tgen_constants.IS_INTERACTIVE:
            self._run_interactive_mode()

    def run_summarizations(self) -> Summary:
        """
        Runs the summarizer to create pipeline project summary and summarize artifacts
        :return: The project summary
        """
        from tgen.summarizer.summarizer import Summarizer
        self.summarizer_args.update_export_dir(self.state.export_dir)
        dataset = Summarizer(self.summarizer_args, dataset=self.args.dataset).summarize()
        if not self.args.dataset.project_summary:
            self.args.dataset = dataset
        else:
            self.args.dataset.update_artifact_df(dataset.artifact_df)  # keep original project summary
        self.state.project_summary = dataset.project_summary if dataset.project_summary else None
        return self.state.project_summary

    def run_step(self, step: AbstractPipelineStep, re_run: bool = False) -> bool:
        """
        Runs a pipeline step
        :param step: The step to run
        :param re_run: If True, runs step even if it complete
        :return: Returns if the pipeline needs to be rerun because a prior state was reloaded
        """
        step_ran = step.run(self.args, self.state, re_run=re_run)
        if step.get_step_name() == self.resume_interactive_mode_step:
            tgen_constants.IS_INTERACTIVE = DEFAULT_INTERACTIVE_STATE
        if step_ran and tgen_constants.IS_INTERACTIVE:
            return self._run_interactive_mode()
        return False

    def get_remaining_steps(self, curr_step: AbstractPipelineStep) -> List[str]:
        """
        Gets a list of the steps that are remaining in the pipeline
        :param curr_step: The step the pipeline is currently at
        :return: The steps that are remaining in the pipeline
        """
        next_index = self.steps.index(curr_step) + 1 if curr_step else 0
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

    def _run_interactive_mode(self, exclude_options: set[str] = None) -> bool:
        """
        Allows the user to interact with the state to rerun a step or continue the pipeline
        :param exclude_options: Set of names of options to exclude from the menu
        :return: Returns if the pipeline needs to be rerun because a prior state was reloaded
        """
        exclude_options = exclude_options if exclude_options else set()
        curr_step, next_step = self._get_current_and_next_step(exclude_options)
        options = [option for option in self.INTERACTIVE_MODE_OPTIONS if option.name not in exclude_options]
        selected_option = self._display_interactive_menu(options, allow_back=False)
        if selected_option == InteractiveModeOptions.LOAD_NEW_STATE:
            success = self._option_new_state(curr_step)
            if success:
                exclude_options.add(InteractiveModeOptions.LOAD_NEW_STATE.name)
            selected_option = None
        elif selected_option == InteractiveModeOptions.DELETE_MODEL_OUTPUT:
            success = self._option_delete_model_output()
            if success:
                exclude_options.add(InteractiveModeOptions.DELETE_MODEL_OUTPUT.name)
            selected_option = None
        elif selected_option == InteractiveModeOptions.RE_RUN:
            logger.log_with_title("Re-running step")
            self.state.mark_step_as_incomplete(curr_step.get_step_name())
        elif selected_option == InteractiveModeOptions.TURN_OFF_INTERACTIVE:
            resume_interactive_mode_step = self._option_turn_off_interactive(curr_step)
            if not resume_interactive_mode_step:
                selected_option = None
            else:
                self.resume_interactive_mode_step = resume_interactive_mode_step
                self.args.interactive_mode = False
                tgen_constants.IS_INTERACTIVE = False

        if selected_option is None:
            self._run_interactive_mode(exclude_options=exclude_options)
        if curr_step:
            return not self.state.step_is_complete(curr_step.get_step_name())  # check if an earlier state was loaded
        return False

    def get_next_step(self, curr_step: AbstractPipelineStep) -> AbstractPipelineStep:
        """
        Marks the next step as complete
        :param curr_step: The current step
        :return: The next step if the current step is not the last
        """
        next_index = self.steps.index(curr_step) + 1
        if next_index < len(self.steps):
            return self.steps[next_index]

    def get_current_step(self) -> AbstractPipelineStep:
        """
        Gets the current step the pipeline is on
        :return: The  current step the pipeline is on
        """
        completed_steps = [step for step in self.steps if self.state.step_is_complete(step.get_step_name())]
        curr_step = None if len(completed_steps) == 0 else completed_steps[-1]
        return curr_step

    def get_pipeline_name(self) -> str:
        """
        Gets the name of the pipeline
        :return: The name of the pipeline
        """
        name = ReflectionUtil.get_class_name(self)
        return name

    def _get_current_and_next_step(self, exclude_options: Set[str]) -> Tuple[AbstractPipelineStep, AbstractPipelineStep]:
        """
        Determines what is the current step the pipeline is on and what is the next step
         :param exclude_options: Set of names of options to exclude from the menu
        :return: The current and next step
        """
        curr_step = self.get_current_step()
        if curr_step is None:
            next_step = self.steps[0]
            exclude_options.add(InteractiveModeOptions.RE_RUN.name)
            msg = EMPTY_STRING
        else:
            next_step = self.get_next_step(curr_step)
            msg = f"Current step: {curr_step.get_step_name()}, "
        if next_step:
            msg += f"Next step: {next_step.get_step_name()}"
        logger.info(f"{msg}")
        return curr_step, next_step

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

    def _option_new_state(self, curr_step: AbstractPipelineStep) -> bool:
        """
        Runs the new state loading when the option is selected
        :param curr_step: The current step the user is one
        :return: True if the state was successfully reloaded
        """
        load_external_option = InteractiveModeOptions.LOAD_EXTERNAL_STATE.value
        steps = self.get_step_names() + [load_external_option]
        step_to_load_from = inquirer_selection(selections=steps,
                                               message="What step state do you want to load from?",
                                               allow_back=True) if self.args.load_dir else load_external_option
        if step_to_load_from is None:
            return False
        load_path = self._get_state_load_path(step_to_load_from)
        if load_path is None:
            return self._option_new_state(curr_step) if self.args.load_dir else None
        if not os.path.exists(load_path):
            logger.warning(f"File not found: {load_path}")
            return self._option_new_state(curr_step)
        new_state = self.state.load_state_from_path(load_path)
        if isinstance(new_state, Exception):
            logger.warning(f"Loading state failed: {new_state}")
            return self._option_new_state(curr_step)
        if new_state is None:
            return False
        self.state = new_state
        self._optional_delete_old_state_files(step_to_load_from)
        logger.info("New state is reloaded - What would you like to do next?\n")
        return True

    def _option_delete_model_output(self) -> bool:
        """
        Deletes any model output found in the load dir
        :return: True if the model output was deleted/never existed, else False if the model output remains
        """
        model_output_files = self._get_model_output_files()
        if not model_output_files:
            msg = f"Could not find any model files to delete "
            msg += f"in {self.args.load_dir}" if self.args.load_dir else "- No load dir provided"
            logger.info(msg)
            return True
        should_delete = confirm(f"Delete the following files? {NEW_LINE}{NEW_LINE.join(model_output_files)}")
        if should_delete:
            for file in model_output_files:
                FileUtil.delete_file_safely(os.path.join(self.args.load_dir, file))
            logger.info("Model output has been deleted. What would you like to do next? \n")
        return should_delete

    def _get_model_output_files(self) -> List[str]:
        """
        Returns a list of the model's output files
        :return: The list of the model's output files
        """
        model_output_files = []
        if self.args.load_dir:
            try:
                model_output_files = FileUtil.ls_files(self.args.load_dir, with_ext=FileUtil.YAML_EXT)
            except Exception:
                pass
        return model_output_files

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
                                                                step_num=load_step_num + 1)
        return load_path

    def _optional_delete_old_state_files(self, step_to_load_from: str) -> bool:
        """
        Allows the user to delete all the state files that are now outdated
        :param step_to_load_from: The step that the state was just loaded from
        :return: Whether they were deleted or not
        """
        load_step_num = self.get_step_names().index(step_to_load_from) if step_to_load_from in self.get_step_names() else -1
        if not self.args.load_dir or step_to_load_from == InteractiveModeOptions.LOAD_EXTERNAL_STATE.value \
                or load_step_num + 1 >= len(self.steps):
            should_delete = False
        else:
            should_delete = confirm("Delete old state files?: ")
        if should_delete:
            step_names = self.get_step_names()
            self.state.delete_state_files(self.args.load_dir, step_names=step_names,
                                          step_to_delete_from=step_names[load_step_num + 1])
        return should_delete

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
        :param message: The message to display at the top of the menu
        :param allow_back: If True, allows user to go to previous menu
        :return: The selected option
        """
        message = "Menu Options: " if not message else message
        choice = inquirer_selection(selections=[mo.value for mo in menu_options], message=message, allow_back=allow_back)
        return EnumUtil.get_enum_from_value(InteractiveModeOptions, choice) if choice else choice

    def _log_costs(self, save: bool = False) -> None:
        """
        Logs the costs accumulated during the run
        :param save: If True, saves the data to a csv
        :return: None
        """
        total_cost = self.state.total_input_cost + self.state.total_output_cost
        if total_cost > 0:
            total_costs = {"Total Input Cost": self.state.total_input_cost,
                           "Total Output Cost": self.state.total_output_cost,
                           "Total Cost": total_cost}
            cost_msg = "{} Token Cost: ${}"
            cost_msgs = [cost_msg.format(name, "%.2f" % cost) for name, cost in total_costs.items()]
            logger.log_with_title("COSTS FOR RUN: ", NEW_LINE.join(cost_msgs))
