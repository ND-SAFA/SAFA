import os
from copy import deepcopy
from typing import Dict, List, NamedTuple, Union, Tuple

import numpy as np
import torch
from datasets import load_metric
from transformers.trainer import Trainer

from scipy.special import softmax
from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from data.datasets.trace_matrix import TraceMatrixManager
from models.model_manager import ModelManager
from train.metrics.map_at_k_metric import MapAtKMetric
from train.metrics.map_metric import MapMetric
from train.metrics.precision_at_threshold_metric import PrecisionAtKMetric
from train.metrics.recall_at_threshold_metric import RecallAtThresholdMetric
from train.metrics.supported_trace_metric import get_metric_name, get_metric_path
from train.trainer_args import TrainerArgs
from util.base_object import BaseObject

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
torch.use_deterministic_algorithms(True)


class TraceTrainer(Trainer, BaseObject):
    """
    Responsible for using given model for training and prediction using given data.
    """

    def __init__(self, trainer_args: TrainerArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, **kwargs):
        """
        Handles the training and evaluation of learning models
        :param args: the learning model arguments
        """
        self.trainer_args = trainer_args
        self.trainer_dataset_manager = trainer_dataset_manager
        self.model_manager = model_manager
        self.model_manager.set_max_seq_length(self.trainer_args.max_seq_length)
        model_init = lambda: self.model_manager.get_model()
        tokenizer = self.model_manager.get_tokenizer()
        super().__init__(model_init=model_init, args=trainer_args, tokenizer=tokenizer,
                         callbacks=trainer_args.callbacks,
                         **kwargs)

    def perform_training(self, checkpoint: str = None) -> Dict:
        """
        Performs the model training.
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        self.model = self.model_manager.get_model()
        self._move_model_to_device(self.model, self.args.device)
        self.train_dataset = self.trainer_dataset_manager[DatasetRole.TRAIN].to_trainer_dataset(self.model_manager)
        output = self.train(resume_from_checkpoint=checkpoint)
        output_dict = TraceTrainer.output_to_dict(output)
        return output_dict

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL) -> Dict:
        """
        Performs the prediction and (optionally) evaluation for the model
        :return: A dictionary containing the results.
        """
        dataset = self.trainer_dataset_manager[dataset_role]
        self.eval_dataset = dataset.to_trainer_dataset(self.model_manager)
        output = self.predict(self.eval_dataset)
        scores = self.get_similarity_scores(output.predictions)
        trace_matrix = TraceMatrixManager(dataset.get_ordered_links(), scores)
        results = self._eval(trace_matrix, scores, output.label_ids, output.metrics,
                             self.trainer_args.metrics) if self.trainer_args.metrics else None
        output_dict = TraceTrainer.output_to_dict(output, metrics=results, predictions=scores,
                                                  source_target_pairs=dataset.get_source_target_pairs())
        return output_dict

    @staticmethod
    def output_to_dict(output: NamedTuple, **kwargs) -> Dict:
        """
        Converts train/prediction output to a dictionary
        :param output: output from training or prediction
        :return: the output represented as a dictionary
        """
        base_output = {field: kwargs[field] if (field in kwargs and kwargs[field]) else getattr(output, field) for field
                       in output._fields}
        additional_attrs = {field: kwargs[field] for field in kwargs.keys() if field not in base_output}
        return {**base_output, **additional_attrs}

    @staticmethod
    def _eval(trace_matrix: TraceMatrixManager, predicted_scores: List[float], label_ids: np.ndarray,
              output_metrics: Dict, metric_names: List) -> Dict:
        """
        Performs the evaluation of the model (use this instead of Trainer.evaluation to utilize predefined metrics from models)
        :param trace_matrix: the matrix of trace links and their scores
        :param predicted_scores: a list of the predicted similarity scores
        :param label_ids: the list of ground truth labels
        :param output_metrics: the dictionary of metrics to include in the results
        :param metric_names: name of metrics desired for evaluation
        :return: a dictionary of metric_name to result
        """
        metric_paths = [get_metric_path(name) for name in metric_names]
        results = deepcopy(output_metrics)
        trace_matrix_metrics = [MapMetric.name, MapAtKMetric.name, PrecisionAtKMetric.name,
                                RecallAtThresholdMetric.name]
        for metric_path in metric_paths:
            metric = load_metric(metric_path, keep_in_memory=True)
            args = {"trace_matrix": trace_matrix} if metric.name in trace_matrix_metrics else {}
            metric_result = metric.compute(predictions=predicted_scores, references=label_ids, **args)
            metric_name = get_metric_name(metric)
            if isinstance(metric_result, dict):
                results.update(metric_result)
            else:
                results[metric_name] = metric_result
        return results

    @staticmethod
    def get_similarity_scores(predictions: Union[np.ndarray, Tuple[np.ndarray]]) -> List[float]:
        """
        Transforms predictions into similarity scores.
        :param predictions: The model predictions.
        :return: List of similarity scores associated with predictions.
        """
        similarity_scores = []
        for pred_i in range(predictions.shape[0]):
            prediction = predictions[pred_i]
            similarity_scores.append(softmax(prediction)[1])
        return similarity_scores
