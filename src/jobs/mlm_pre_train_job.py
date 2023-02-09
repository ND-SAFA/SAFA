import os

from transformers import DataCollatorForLanguageModeling

from constants import MLM_PROBABILITY_DEFAULT
from data.datasets.dataset_role import DatasetRole
from data.datasets.pre_train_dataset import PreTrainDataset
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from jobs.train_job import TrainJob
from models.model_manager import ModelManager
from models.model_properties import ModelTask
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs


class MLMPreTrainJob(TrainJob):

    def __init__(self, job_args: JobArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, trainer_args: TrainerArgs,
                 mlm_probability: float = MLM_PROBABILITY_DEFAULT):
        """
        The base job class for tracing jobs
        :param job_args: the arguments for the job
        :param model_manager: the manages the model necessary for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param trainer_args: other arguments needed for the trainer
        :param mlm_probability: the probability for the masking a word in the learning model
        """
        model_manager.model_task = ModelTask.MASKED_LEARNING
        super().__init__(job_args, model_manager, trainer_dataset_manager, trainer_args)
        self.mlm_probability = mlm_probability

    def _run(self) -> JobResult:
        """
        Runs the pre training using a masked learning model
        :return: the result from the pre training
        """
        tokenizer = self.model_manager.get_tokenizer()
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, mlm=True, mlm_probability=self.mlm_probability
        )
        tokenizer.save_pretrained(self.job_args.output_dir)

        job_result = super()._run(data_collator=data_collator)
        self.trainer_args.output_dir = os.path.join(self.trainer_args.output_dir, "best")

        train_dataset: PreTrainDataset = self.trainer_dataset_manager[DatasetRole.TRAIN]
        os.remove(train_dataset.training_file_path)
        return job_result

    def get_trainer(self, **kwargs) -> TraceTrainer:
        if self._trainer is None:
            self._trainer = TraceTrainer(trainer_args=self.trainer_args,
                                         trainer_dataset_manager=self.trainer_dataset_manager,
                                         model_manager=self.model_manager, **kwargs)
        return self._trainer
