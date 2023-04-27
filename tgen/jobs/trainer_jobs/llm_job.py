from typing import Union

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.train.args.supported_llm_args import SupportedLLMArgs
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trainers.llm_trainer import LLMTrainer
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.override import overrides


class LLMJob(AbstractTrainerJob):
    """
    Job to handle open ai tasks
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, trainer_args: SupportedLLMArgs = None,
                 task: TrainerTask = TrainerTask.PREDICT, job_args: JobArgs = None):
        """
        Initializes job with necessary args
        :param trainer_args: The arguments for training and prediction calls
        :param trainer_dataset_manager: The dataset manager for training and prediction
        """
        if trainer_args is None:
            trainer_args = OpenAIArgs()
        super().__init__(model_manager=None, trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=trainer_args, task=task, job_args=job_args)
        self.trainer_args = trainer_args

    @overrides(AbstractTrainerJob)
    def get_trainer(self, **kwargs) -> LLMTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = LLMTrainer(trainer_args=self.trainer_args,
                                       trainer_dataset_manager=self.trainer_dataset_manager)
        return self._trainer

    @overrides(AbstractTrainerJob)
    def _run_trainer_specific_task(self) -> Union[AbstractTraceOutput, dict]:
        """
        Runs a task that is specific to the trainer (may be implemented by child classes)
        :return: The output of the task run
        """
        raise RuntimeError("Task cannot be performed by this Trainer %s" % self.task)
