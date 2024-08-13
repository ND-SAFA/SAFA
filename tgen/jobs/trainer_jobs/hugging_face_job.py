import os
from typing import Union

from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.data.tdatasets.pre_train_dataset import PreTrainDataset
from common_resources.llm.args.hugging_face_args import HuggingFaceArgs
from common_resources.tools.constants.dataset_constants import MLM_PROBABILITY_DEFAULT
from common_resources.tools.util.override import overrides
from transformers.data.data_collator import DataCollatorForLanguageModeling

from tgen.common.constants.experiment_constants import BEST_MODEL_NAME
from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.trace_train_output import TraceTrainOutput
from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.core.trainers.supported_trainer import SupportedHuggingFaceTrainer
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.models.model_manager import ModelManager


class HuggingFaceJob(AbstractTrainerJob):

    def __init__(self, model_manager: ModelManager, trainer_dataset_manager: TrainerDatasetManager, trainer_args: HuggingFaceArgs,
                 task: TrainerTask, trainer: SupportedHuggingFaceTrainer = SupportedHuggingFaceTrainer.HF, job_args: JobArgs = None):
        """
        The base job class for tracing jobs
        :param job_args: the arguments for the job
        :param model_manager: the manages the model necessary for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param trainer_args: other arguments needed for the trainer
        :param task: Task performed by the trainer.
        """
        self.trainer = trainer
        super().__init__(job_args=job_args, model_manager=model_manager, trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=trainer_args, task=task)

    def get_trainer(self, **kwargs) -> HuggingFaceTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            trainer_class = self.trainer.value
            self._trainer = trainer_class(trainer_args=self.trainer_args,
                                          trainer_dataset_manager=self.trainer_dataset_manager,
                                          model_manager=self.model_manager, **kwargs)
        return self._trainer

    @overrides(AbstractTrainerJob)
    def _run_trainer_specific_task(self, **kwargs) -> Union[AbstractTraceOutput, dict]:
        """
        Runs a task that is specific to the trainer (may be implemented by child classes)
        :return: The output of the task run
        """
        output = None
        if self.task == TrainerTask.PUSH:
            output = self.get_trainer().push_to_hub()
        elif self.task == TrainerTask.PRE_TRAIN:
            output = self._perform_pretraining()
        else:
            super()._run_trainer_specific_task()
        return output

    def _perform_pretraining(self) -> TraceTrainOutput:
        """
        Performs masked learning pre-training
        :return: The output from the training
        """
        mlm_probability = self.kwargs.get("mlm_probability", MLM_PROBABILITY_DEFAULT)
        tokenizer = self.model_manager.get_tokenizer()
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, mlm=True, mlm_probability=mlm_probability
        )
        tokenizer.save_pretrained(self.job_args.output_dir)
        output = self.get_trainer(data_collator=data_collator).perform_training()
        self.trainer_args.output_dir = os.path.join(self.trainer_args.output_dir, BEST_MODEL_NAME)

        train_dataset: PreTrainDataset = self.trainer_dataset_manager[DatasetRole.TRAIN]
        os.remove(train_dataset.training_file_path)
        return output
