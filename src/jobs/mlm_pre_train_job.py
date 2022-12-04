import os

from transformers import DataCollatorForLanguageModeling

from config.constants import MLM_PROBABILITY_DEFAULT
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from jobs.train_job import TrainJob
from data.datasets.dataset_role import DatasetRole
from data.datasets.pre_train_dataset import PreTrainDataset


class MLMPreTrainJob(TrainJob):

    def __init__(self, job_args: JobArgs, mlm_probability: float = MLM_PROBABILITY_DEFAULT):
        """
        The base job class for tracing jobs
        :param mlm_probability: the probability for the masking a word in the learning model
        """
        super().__init__(job_args)
        self.mlm_probability = mlm_probability

    def _run(self) -> JobResult:
        tokenizer = self.get_model_manager().get_tokenizer()
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, mlm=True, mlm_probability=self.mlm_probability
        )
        tokenizer.save_vocabulary(self.output_dir)

        job_result = super()._run(data_collator=data_collator)

        train_dataset: PreTrainDataset = self.trainer_args.trainer_dataset_container[DatasetRole.TRAIN]
        os.remove(train_dataset.training_file_path)
        return job_result
