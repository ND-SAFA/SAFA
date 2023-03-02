import os
from typing import Callable, List

import numpy as np
from sklearn.preprocessing import minmax_scale, scale

from constants import OUTPUT_FILENAME
from data.datasets.dataset_role import DatasetRole
from experiments.experiment import Experiment
from experiments.experiment_step import ExperimentStep
from jobs.components.job_result import JobResult
from jobs.train_job import TrainJob
from train.metrics.metrics_manager import MetricsManager
from train.trace_output.trace_prediction_output import TracePredictionEntry
from util.dict_util import ListUtil
from util.file_util import FileUtil
from util.json_util import JsonUtil


def average(arr):
    return sum(arr) / len(arr)


def first(arr):
    return arr[0]


EnsembleFunctions = {
    # "sum": sum,
    # "max": max,
    "average": average,
    "first": first
}


class EnsembleExperiment(Experiment):
    """
    Aggregates a series of train jobs that produce predictions on the same dataset.
    """

    def run(self):
        """
        Runs training jobs and uses their output to create an ensemble model using defined agg function.
        Ensemble output is
        :return:
        """
        self.set_cross_step_vars(self.steps)
        jobs: List[TrainJob] = super().run()
        job_prediction_entries = self.collect_job_predictions(jobs)
        job_labels = [[entry["label"] for entry in job_entries] for job_entries in job_prediction_entries]
        job_predictions = [[entry["score"] for entry in job_entries] for job_entries in job_prediction_entries]

        job_predictions = EnsembleExperiment.scale_predictions(job_predictions)

        ListUtil.assert_equal(job_labels)
        ensemble_labels = job_labels[0]
        ensemble_metrics = jobs[0].trainer_args.metrics
        eval_dataset = jobs[0].trainer_dataset_manager[DatasetRole.EVAL]
        for func_name, agg_func in EnsembleFunctions.items():
            ensemble_similarities = self.ensemble_predictions(job_predictions, agg_func)
            metrics_manager = MetricsManager(eval_dataset.get_ordered_links(), predicted_similarities=ensemble_similarities)
            agg_metrics = metrics_manager.eval(ensemble_metrics)
            self.save_as_job_output(ensemble_similarities, ensemble_labels, agg_metrics, model_name=f"ensemble-{func_name}")

    @staticmethod
    def collect_job_predictions(jobs) -> List[List[TracePredictionEntry]]:
        """
        Gathers and aligns predictions for each job.
        :param jobs: The jobs whose predictions are read.
        :return: Aggregated labels, links, and predictions.
        """
        job_entries = []
        for job in jobs:
            job_output_path = os.path.join(job.job_args.output_dir, OUTPUT_FILENAME)
            job_output = JsonUtil.read_json_file(job_output_path)
            prediction_entries = job_output["prediction_output"]["prediction_entries"]
            job_entries.append(prediction_entries)
        return job_entries

    @staticmethod
    def ensemble_predictions(global_predictions: List[List[float]], agg_func: Callable[[np.array], float], technique_axis: int = 0):
        """
        Applies aggregation function across prediction to create ensemble prediction.
        :param global_predictions: The prediction across several techniques.
        :param agg_func: The aggregation function to use to combine scores.
        :param technique_axis: The axis along which each technique is stacked.
        :return: Aggregated predictions.
        """
        global_predictions = np.array(global_predictions)
        ensemble_predictions = np.apply_along_axis(func1d=agg_func, arr=global_predictions, axis=technique_axis)
        return ensemble_predictions

    @staticmethod
    def scale_predictions(predictions: List[List[float]]) -> List[List[float]]:
        """
        Scales predictions so that technique has been standardized and squished to fit between 0 and 1
        :param predictions: List of technique predictions.
        :return: List of technique predictions
        """
        scaled_predictions = []
        for p in predictions:
            scaled_predictions.append(minmax_scale(scale(p)))
        return scaled_predictions

    @staticmethod
    def set_cross_step_vars(steps: List[ExperimentStep]) -> None:
        """
        Sets the experimental variables to model path if empty, like due to the fact of using different jobs.
        :return: None
        """
        for step in steps:
            for job in step.jobs:
                job_experimental_vars = job.result[JobResult.EXPERIMENTAL_VARS]
                if len(job_experimental_vars) == 0:
                    job.result[JobResult.EXPERIMENTAL_VARS] = {"model_path": job.model_manager.model_path.lower()}

    def save_as_job_output(self, ensemble_predictions, ensemble_labels, agg_metrics, model_name: str) -> None:
        """
        Saves predictions, labels, and metrics as a job output so it can be read with the other results.
        :param ensemble_predictions: The ensemble predictions.
        :param ensemble_labels: The ensemble labels.
        :param agg_metrics: The metrics calculated for eval dataset.
        :param model_name: The name of the model.
        :return: None
        """
        job_result = JobResult()
        job_result[JobResult.PREDICTION_OUTPUT] = {
            JobResult.PREDICTIONS: ensemble_predictions,
            JobResult.LABEL_IDS: ensemble_labels,
            JobResult.METRICS: agg_metrics,
        }
        job_result[JobResult.EXPERIMENTAL_VARS] = {
            "model_path": model_name
        }
        step_output_dir = self.get_step_output_dir(self.experiment_index, 0)
        job_output_dir = os.path.join(step_output_dir, f"mp={model_name}")
        FileUtil.create_dir_safely(job_output_dir)
        job_output_path = os.path.join(job_output_dir, OUTPUT_FILENAME)
        json_output = JsonUtil.dict_to_json(job_result.as_dict())
        FileUtil.write(json_output, job_output_path)
