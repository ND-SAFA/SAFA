from typing import Dict, Any

from data.datasets.dataset_role import DatasetRole
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult


class TrainJob(AbstractTraceJob):

    def _run(self, **kwargs) -> JobResult:
        """
        Runs the training and obtains results
        :return: results of the training including as loss and time
        """
        trainer = self.get_trainer(**kwargs)
        training_output = trainer.perform_training()
        trainer.save_model(self.output_dir)
        if DatasetRole.EVAL in self.trainer_dataset_manager:
            val_metrics = trainer.perform_prediction()
            training_output[JobResult.METRICS].update(val_metrics[JobResult.METRICS])
        return JobResult.from_dict(training_output)
