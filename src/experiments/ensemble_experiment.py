import os
from copy import deepcopy
from typing import Callable, List

import numpy as np
from sklearn.preprocessing import minmax_scale, scale

from constants import OUTPUT_FILENAME
from data.datasets.dataset_role import DatasetRole
from experiments.experiment import Experiment
from experiments.experiment_step import ExperimentStep
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult
from jobs.predict_job import PredictJob
from jobs.vsm_job import VSMJob
from models.single_layer.single_layer_model import train, SingleLayerModel, predict
from train.metrics.metrics_manager import MetricsManager
from util.file_util import FileUtil
from util.json_util import JsonUtil


def average(arr):
    return sum(arr) / len(arr)


def first(arr):
    return arr[0]


EnsembleFunctions = {
    "max": max,
    "average": average,
    "nn": None
    # "first": first
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
        train_step = self.steps[0]
        self.steps.append(self._create_predict_on_train_step(train_step.jobs))

        jobs: List[AbstractTraceJob] = super().run()
        train_jobs, predict_on_train_jobs = jobs[:len(train_step.jobs)], jobs[len(train_step.jobs):]

        train_dataset = train_jobs[0].trainer_dataset_manager[DatasetRole.TRAIN]
        train_labels = train_dataset.get_ordered_labels()

        eval_dataset = train_jobs[0].trainer_dataset_manager[DatasetRole.EVAL]
        eval_labels = eval_dataset.get_ordered_labels()

        train_job_predictions = self.collect_job_predictions(train_jobs)
        predict_on_train_job_predictions = self.collect_job_predictions(predict_on_train_jobs)
        model = self._train_ensemble_layer(predict_on_train_job_predictions, train_labels)

        ensemble_metrics = train_jobs[0].trainer_args.metrics
        for func_name, agg_func in EnsembleFunctions.items():
            if func_name == "nn":
                ensemble_similarities = predict(model, self.transform_predictions_for_nn(train_job_predictions))
            else:
                ensemble_similarities = self.ensemble_predictions(train_job_predictions, agg_func)
            metrics_manager = MetricsManager(trace_df=eval_dataset.trace_df,
                                             link_ids=eval_dataset.get_ordered_link_ids(),
                                             predicted_similarities=ensemble_similarities)
            agg_metrics = metrics_manager.eval(ensemble_metrics)
            self.save_as_job_output(ensemble_similarities, eval_labels, agg_metrics, model_name=f"ensemble-{func_name}")

    @staticmethod
    def collect_job_predictions(jobs) -> List[List[float]]:
        """
        Gathers and aligns predictions for each job.
        :param jobs: The jobs whose predictions are read.
        :return: Aggregated labels, links, and predictions.
        """
        job_entries = []
        for job in jobs:
            job_output_path = os.path.join(job.job_args.output_dir, OUTPUT_FILENAME)
            job_output = JsonUtil.read_json_file(job_output_path)
            prediction_output = job_output["prediction_output"] if "prediction_output" in job_output else job_output
            job_entries.append(prediction_output["prediction_entries"])
        job_predictions = [[entry["score"] for entry in job_entries] for job_entries in job_entries]
        return EnsembleExperiment.scale_predictions(job_predictions)

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

    @staticmethod
    def _create_predict_on_train_step(train_step_jobs: List[AbstractTraceJob]) -> ExperimentStep:
        """
        Creates an experiment step to perform a prediction on the training data
        :param train_step_jobs: The original train step jobs
        :return: The experiment step to perform a prediction on the training data
        """
        predict_on_train_jobs = []
        for train_job in train_step_jobs:
            tmp_job = deepcopy(train_job)
            predict_job = PredictJob(job_args=tmp_job.job_args, trainer_dataset_manager=tmp_job.trainer_dataset_manager,
                                     model_manager=tmp_job.model_manager, trainer_args=tmp_job.trainer_args) \
                if not isinstance(tmp_job, VSMJob) else deepcopy(tmp_job)
            train_dataset = predict_job.trainer_dataset_manager.get_datasets()[DatasetRole.TRAIN]
            predict_job.trainer_dataset_manager.replace_dataset(train_dataset, DatasetRole.EVAL)
            predict_on_train_jobs.append(predict_job)
        return ExperimentStep(predict_on_train_jobs)

    @staticmethod
    def transform_predictions_for_nn(original_predictions: List[List[float]]) -> List[List[float]]:
        """
        Transforms the predictions into the format expected by the NN
        :param original_predictions: The original predictions from the models
        :return: The predictions as input for the nn
        """
        transformed_predictions = [[] for i in range(len(original_predictions[0]))]
        for model_prediction in original_predictions:
            assert len(model_prediction) == len(transformed_predictions), "Number of model predictions are mismatched."
            for i, pred in enumerate(model_prediction):
                transformed_predictions[i].append(pred)
        return transformed_predictions

    @staticmethod
    def _train_ensemble_layer(ensemble_preds: List[List[float]], labels: List[float]) -> SingleLayerModel:
        """
        Trains a single layer neural network that accepts model predictions as input and combines for a single output
        :param ensemble_preds: The prediction from each models predictions
        :param labels: Ground-truth labels
        :return: The trained model
        """
        n_models = len(ensemble_preds)
        input_data = EnsembleExperiment.transform_predictions_for_nn(ensemble_preds)
        model = SingleLayerModel(n_models)
        train(model, input_data, labels)
        return model
