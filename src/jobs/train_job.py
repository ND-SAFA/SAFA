import os

from transformers.integrations import WandbCallback

from constants import BEST_MODEL_NAME
from data.datasets.dataset_role import DatasetRole
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult


class TrainJob(AbstractTraceJob):

    def _run(self, **kwargs) -> JobResult:
        """
        Runs the training and obtains results.
        :return: Results of the training including as loss and time
        """
        trainer = self.get_trainer(**kwargs)
        trainer.remove_callback(WandbCallback)
        training_output = trainer.perform_training(
            self.trainer_args.checkpoint_path)  # will also switch dataset in val to eval if present.
        if DatasetRole.EVAL in self.trainer_dataset_manager:
            training_output.prediction_output = trainer.perform_prediction(DatasetRole.EVAL)
        best_model_path = self._trainer.state.best_model_checkpoint
        if best_model_path:
            os.rename(best_model_path, os.path.join(self.trainer_args.output_dir, BEST_MODEL_NAME))
        return JobResult.from_trace_output(training_output)
