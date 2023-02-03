from data.datasets.dataset_role import DatasetRole
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult
from train.base_trainer import BaseTrainer


class TrainJob(AbstractTraceJob):

    def _run(self, **kwargs) -> JobResult:
        """
        Runs the training and obtains results
        :return: results of the training including as loss and time
        """
        trainer = self.get_trainer(**kwargs)
        training_output = trainer.perform_training(
            self.trainer_args.checkpoint_path)  # will also switch dataset in val to eval if present.
        if DatasetRole.EVAL in self.trainer_dataset_manager:
            eval_predictions = trainer.perform_prediction(DatasetRole.EVAL)
            training_output.eval_metrics = eval_predictions.metrics
        return JobResult.from_trace_output(training_output)

    def get_trainer(self, **kwargs) -> BaseTrainer:
        if self._trainer is None:
            self._trainer = BaseTrainer(trainer_args=self.trainer_args,
                                        trainer_dataset_manager=self.trainer_dataset_manager,
                                        model_manager=self.model_manager, **kwargs)
        return self._trainer
