import os
from typing import Dict

from data.datasets.dataset_role import DatasetRole
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult
from train.trace_trainer import TraceTrainer
from util.file_util import FileUtil


class TrainJob(AbstractTraceJob):

    def _run(self, **kwargs) -> JobResult:
        """
        Runs the training and obtains results
        :return: results of the training including as loss and time
        """
        trainer = self.get_trainer(**kwargs)
        training_output = trainer.perform_training(
            self.trainer_args.checkpoint_path)  # will also switch dataset in val to eval if present.
        trainer.save_model(self.model_manager.model_output_path)
        if DatasetRole.VAL in self.trainer_dataset_manager:
            val_metrics = trainer.perform_prediction(DatasetRole.VAL)
            training_output[JobResult.METRICS].update(val_metrics[JobResult.METRICS])
            self.save_if_best(trainer, val_metrics)
        return JobResult.from_dict(training_output)

    def save_if_best(self, trainer: TraceTrainer, metrics: Dict):
        if self.trainer_args.save_best and self.trainer_args.comparison_metric:
            metric_value = metrics[JobResult.METRICS][self.trainer_args.comparison_metric]
            metric_path = os.path.join(self.model_manager.model_output_path, "metrics.json")
            best_model_path = os.path.join(self.model_manager.model_output_path, "best_model")
            should_save = False
            if os.path.exists(metric_path):
                metric_file = FileUtil.read_json_file(metric_path)
                best_score = metric_file["best"]
                if self.trainer_args.should_maximize_metric:
                    if metric_value > best_score:
                        should_save = True
                else:
                    if metric_value < best_score:
                        should_save = True
            else:
                should_save = True
                metric_file = {}

            if should_save:
                metric_file["best"] = metric_value
                metric_file["args"] = self.trainer_args
                trainer.save_model(best_model_path)
                FileUtil.save_to_file(metric_file, metric_path)
