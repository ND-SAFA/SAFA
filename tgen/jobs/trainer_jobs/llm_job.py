from typing import Union

from tgen.constants.open_ai_constants import CLASSIFICATION_MODEL_DEFAULT
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.models.model_manager import ModelManager
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trainers.llm_trainer import LLMTrainer
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.override import overrides


class LLMJob(AbstractTrainerJob):
    """
    Job to handle open ai tasks
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, trainer_args: OpenAiArgs = OpenAiArgs(),
                 base_model: str = CLASSIFICATION_MODEL_DEFAULT, task: TrainerTask = TrainerTask.PREDICT, job_args: JobArgs = None,
                 prompt_creator: AbstractPromptCreator = None):
        """
        Initializes job with necessary args
        :param base_model: The name of the model
        :param trainer_args: The arguments for training and prediction calls
        :param trainer_dataset_manager: The dataset manager for training and prediction
        """
        if prompt_creator is None:
            prompt_creator = ClassificationPromptCreator(prompt_args=trainer_args.prompt_args)
        super().__init__(model_manager=ModelManager(model_path=base_model), trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=trainer_args, task=task, job_args=job_args)
        self.base_model = base_model
        self.trainer_args = trainer_args
        self.prompt_creator = prompt_creator

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
                                       base_model=self.base_model, prompt_creator=self.prompt_creator)
        return self._trainer

    @overrides(AbstractTrainerJob)
    def _run_trainer_specific_task(self) -> Union[AbstractTraceOutput, dict]:
        """
        Runs a task that is specific to the trainer (may be implemented by child classes)
        :return: The output of the task run
        """
        raise RuntimeError("Task cannot be performed by this Trainer %s" % self.task)
