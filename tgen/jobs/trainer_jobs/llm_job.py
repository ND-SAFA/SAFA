from typing import Union

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.supported_llm_manager import SupportedLLMManager
from tgen.train.args.abstract_llm_args import AbstractLLMArgs
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trainers.llm_trainer import LLMTrainer
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.override import overrides


class LLMJob(AbstractTrainerJob):
    """
    Job to handle open ai tasks
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, trainer_args: AbstractLLMArgs = None,
                 task: TrainerTask = TrainerTask.PREDICT, job_args: JobArgs = None, prompt_creator: AbstractPromptCreator = None,
                 llm_util: AbstractLLMManager = None):
        """
        Initializes job with necessary args
        :param trainer_args: The arguments for training and prediction calls
        :param trainer_dataset_manager: The dataset manager for training and prediction
        """
        if trainer_args is None:
            trainer_args = OpenAIArgs()
        if llm_util is None:
            llm_util = SupportedLLMManager.OPENAI.value
            assert isinstance(trainer_args, OpenAIArgs), "Using default OpenAI args and expected trainer args to match."
        if prompt_creator is None:
            prompt_creator = ClassificationPromptCreator(prompt_args=trainer_args.prompt_args)
        super().__init__(model_manager=None, trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=trainer_args, task=task, job_args=job_args)
        self.trainer_args = trainer_args
        self.prompt_creator = prompt_creator
        self.llm_util = llm_util

    @overrides(AbstractTrainerJob)
    def get_trainer(self, **kwargs) -> LLMTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = LLMTrainer(trainer_args=self.trainer_args,
                                       trainer_dataset_manager=self.trainer_dataset_manager,
                                       prompt_creator=self.prompt_creator,
                                       llm_manager=self.llm_util)
        return self._trainer

    @overrides(AbstractTrainerJob)
    def _run_trainer_specific_task(self) -> Union[AbstractTraceOutput, dict]:
        """
        Runs a task that is specific to the trainer (may be implemented by child classes)
        :return: The output of the task run
        """
        raise RuntimeError("Task cannot be performed by this Trainer %s" % self.task)
