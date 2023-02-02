import os

from data.datasets.dataset_role import DatasetRole
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult
from train.trainer_tools.trace_accelerator import TraceAccelerator


class TrainJob(AbstractTraceJob):

    def _run(self, **kwargs) -> JobResult:
        """
        Runs the training and obtains results
        :return: results of the training including as loss and time
        """
        test_log_dir = os.path.join(self.job_args.output_dir, "tensorboard")
        TraceAccelerator.update(logging_dir=test_log_dir)
        trainer = self.get_trainer(**kwargs)
        training_output = trainer.perform_training(
            self.trainer_args.checkpoint_path)  # will also switch dataset in val to eval if present.
        if DatasetRole.EVAL in self.trainer_dataset_manager:
            eval_predictions = trainer.perform_prediction(DatasetRole.EVAL)
            training_output.eval_metrics = eval_predictions.metrics
        return JobResult.from_trace_output(training_output)
