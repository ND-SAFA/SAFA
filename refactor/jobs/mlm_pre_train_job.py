import os
from transformers import DataCollatorForLanguageModeling

from constants.constants import MLM_PROBABILITY_DEFAULT
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.job_args import JobArgs


class MLMPreTrainJob(AbstractTraceJob):

    def __init__(self, job_args: JobArgs, mlm_probability: float = MLM_PROBABILITY_DEFAULT):
        """
        The base job class for tracing jobs
        :param mlm_probability: the probability for the masking a word in the learning model
        """
        super().__init__(job_args)
        self.mlm_probability = mlm_probability

    def _run(self):
        tokenizer = self.get_model_generator().get_tokenizer()
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, mlm=True, mlm_probability=self.mlm_probability
        )
        tokenizer.save_vocabulary(self.output_dir)
        trainer = self.get_trainer(data_collator=data_collator)
        result = trainer.perform_training()
        trainer.save_model(trainer.args.output_dir)

        os.remove(self.trace_args.trainer_dataset_container.train_dataset.training_file_path)
        return result
