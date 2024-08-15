from typing import Union

from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.llm.args.abstract_llm_args import AbstractLLMArgs
from common_resources.llm.llm_task import LLMCompletionType
from common_resources.llm.prompts.prompt_builder import PromptBuilder
from common_resources.tools.constants.default_model_managers import get_efficient_default_llm_manager
from common_resources.tools.util.override import overrides

from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob


class LLMJob(AbstractTrainerJob):
    """
    Job to handle open ai tasks
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, prompt_builder: PromptBuilder,
                 trainer_args: AbstractLLMArgs = None, task: TrainerTask = TrainerTask.PREDICT,
                 job_args: JobArgs = None, llm_manager: AbstractLLMManager = None,
                 completion_type: LLMCompletionType = LLMCompletionType.GENERATION):
        """
        Initializes job with necessary args
        :param trainer_args: The arguments for training and prediction calls
        :param trainer_dataset_manager: The dataset manager for training and prediction
        :param prompt_builder: Responsible for building the prompt used by the LLM
        :param task: The type of task to perform (i.e. train, predict. etc)
        :param job_args: Any args necessary for the job
        :param llm_manager: Manages the LLM used in job
        :param completion_type: The type of completion (prediction or generation)
        """
        if llm_manager is None:
            llm_manager = get_efficient_default_llm_manager()
        if trainer_args is None:
            trainer_args = llm_manager.llm_args
        super().__init__(model_manager=None, trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=trainer_args, task=task, job_args=job_args)
        self.trainer_args = trainer_args
        self.prompt_builder = prompt_builder
        self.llm_manager = llm_manager
        self.completion_type = completion_type

    @overrides(AbstractTrainerJob)
    def get_trainer(self, **kwargs) -> LLMTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = LLMTrainer(LLMTrainerState(
                trainer_dataset_manager=self.trainer_dataset_manager,
                prompt_builders=self.prompt_builder,
                llm_manager=self.llm_manager,
                completion_type=self.completion_type,
                **kwargs))
        return self._trainer

    @overrides(AbstractTrainerJob)
    def _run_trainer_specific_task(self) -> Union[AbstractTraceOutput, dict]:
        """
        Runs a task that is specific to the trainer (may be implemented by child classes)
        :return: The output of the task run
        """
        raise RuntimeError("Task cannot be performed by this Trainer %s" % self.task)
