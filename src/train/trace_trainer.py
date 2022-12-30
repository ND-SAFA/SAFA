import os
from copy import deepcopy
from typing import Dict, List, NamedTuple, Tuple, Union

import numpy as np
import torch
from datasets import load_metric
from scipy.special import softmax
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler
from transformers.trainer import Trainer
from transformers.trainer_pt_utils import get_tpu_sampler, is_torch_tpu_available

from config.override import overrides
from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from models.model_manager import ModelManager
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
                 trainer_dataset_manager: TrainerDatasetManager,
                 **kwargs):
        """
        Handles the training and evaluation of learning models
        :param args: the learning model arguments
        """
        self.trainer_args = trainer_args
        self.trainer_dataset_manager = trainer_dataset_manager
        self.model_manager = model_manager
        self.model_manager.set_max_seq_length(self.trainer_args.max_seq_length)
        model = self.model_manager.get_model()
        tokenizer = self.model_manager.get_tokenizer()
        super().__init__(model=model, args=trainer_args, tokenizer=tokenizer, callbacks=trainer_args.callbacks,
                         **kwargs)

    def perform_training(self, checkpoint: str = None) -> Dict:
        """
        Performs the model training.
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        self.train_dataset = self.trainer_dataset_manager[DatasetRole.TRAIN].to_trainer_dataset(self.model_manager)
        if DatasetRole.VAL in self.trainer_dataset_manager:
            self.eval_dataset = self.trainer_dataset_manager[DatasetRole.VAL].to_trainer_dataset(self.model_manager)
        output = self.train(resume_from_checkpoint=checkpoint)
        return TraceTrainer.output_to_dict(output)

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL) -> Dict:
        """
        Performs the prediction and (optionally) evaluation for the model
        :return: A dictionary containing the results.
        """
        self.eval_dataset = self.trainer_dataset_manager[dataset_role].to_trainer_dataset(self.model_manager)
        output = self.predict(self.eval_dataset)
        predictions = TraceTrainer.get_similarity_scores(output.predictions)
        results = self._eval(predictions, output.label_ids, output.metrics,
                             self.trainer_args.metrics) if self.trainer_args.metrics else None
        output_dict = TraceTrainer.output_to_dict(output, metrics=results, predictions=predictions,
                                                  source_target_pairs=self.trainer_dataset_manager[
                                                      dataset_role].get_source_target_pairs())
        return output_dict

    @staticmethod
    def output_to_dict(output: NamedTuple, **kwargs) -> Dict:
        """
        Converts train/prediction output to a dictionary
        :param output: output from training or prediction
        :return: the output represented as a dictionary
        """
        base_output = {field: kwargs[field] if (field in kwargs and kwargs[field]) else getattr(output, field) for field
                       in
                       output._fields}
        additional_attrs = {field: kwargs[field] for field in kwargs.keys() if field not in base_output}
        return {**base_output, **additional_attrs}

    @staticmethod
    def _eval(preds: Union[np.ndarray, Tuple[np.ndarray]], label_ids: np.ndarray, output_metrics: Dict,
              metric_names: List) -> Dict:
        """
        Performs the evaluation of the model (use this instead of Trainer.evaluation to utilize predefined metrics from models)
        :param output: the output from predictions
        :param metric_names: name of metrics desired for evaluation
        :return: a dictionary of metric_name to result
        """
        metric_paths = [get_metric_path(name) for name in metric_names]
        results = deepcopy(output_metrics)
        for metric_path in metric_paths:
            metric = load_metric(metric_path, keep_in_memory=True)
            metric_result = metric.compute(predictions=preds, references=label_ids)
            metric_name = get_metric_name(metric)
            if isinstance(metric_result, dict) and metric_name in metric_result:
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

    @overrides(Trainer)
    def get_train_dataloader(self) -> DataLoader:
        """
        Gets the dataloader for training
        :return: the DataLoader
        """
        if is_torch_tpu_available():
            train_sampler = get_tpu_sampler(self.train_dataset, self.trainer_args.train_batch_size)
        else:
            train_sampler = (
                RandomSampler(self.train_dataset)
                if self.trainer_args.local_rank == -1
                else DistributedSampler(self.train_dataset)
            )

        data_loader = DataLoader(
            self.train_dataset,
            batch_size=self.trainer_args.train_batch_size,
            sampler=train_sampler,
            collate_fn=self.data_collator,
            drop_last=self.trainer_args.dataloader_drop_last,
        )
        return data_loader
