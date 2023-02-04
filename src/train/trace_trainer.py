import os
from typing import Any, Dict, Optional, Union

import torch
from datasets import Dataset
from transformers.trainer import Trainer

from data.datasets.data_key import DataKey
from data.datasets.dataset_role import DatasetRole
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from data.samplers.balanced_batch_sampler import BalancedBatchSampler
from models.model_manager import ModelManager
from train.metrics.metrics_manager import MetricsManager
from train.save_strategy.abstract_save_strategy import AbstractSaveStrategy
from train.save_strategy.comparison_criteria import ComparisonCriterion
from train.save_strategy.metric_save_strategy import MetricSaveStrategy
from train.trace_output.trace_prediction_output import TracePredictionOutput
from train.trace_output.trace_train_output import TraceTrainOutput
from train.trainer_args import TrainerArgs
from train.trainer_tools.trace_accelerator import TraceAccelerator
from util.base_object import BaseObject
from util.logging.logger_manager import logger
from util.override import overrides

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
torch.use_deterministic_algorithms(True)

TRIAL = Union["optuna.Trial", Dict[str, Any]]


class TraceTrainer(Trainer, BaseObject):
    """
    Trains model on data for generic task.
    """

    def __init__(self, trainer_args: TrainerArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, save_strategy: AbstractSaveStrategy = None, **kwargs):
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
        if save_strategy is None:
            self.save_strategy = MetricSaveStrategy(ComparisonCriterion(["map", "f2"]))
        super().__init__(model_init=model_init, args=trainer_args, tokenizer=tokenizer,
                         callbacks=trainer_args.callbacks,
                         **kwargs)

    def perform_training(self, checkpoint: str = None) -> TraceTrainOutput:
        """
        Performs the model training.
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        self.model = self.model_manager.get_model()
        self.train_dataset = self.trainer_dataset_manager[DatasetRole.TRAIN].to_trainer_dataset(self.model_manager)
        self.eval_dataset = self._get_dataset(DatasetRole.VAL)
        train_output = self.train(resume_from_checkpoint=checkpoint)
        self.eval_dataset = self._get_dataset(DatasetRole.EVAL)
        return TraceTrainOutput(train_output=train_output)

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :return: A dictionary containing the results.
        """
        dataset = self.trainer_dataset_manager[dataset_role]
        self.eval_dataset = dataset.to_trainer_dataset(self.model_manager)
        output = self.predict(self.eval_dataset)
        n_predictions, n_expected = len(output.predictions), len(dataset)
        assert n_predictions == n_expected, f"Expected {n_expected} samples but received {n_predictions} predictions."
        metrics_manager = MetricsManager(dataset.get_ordered_links(), output.predictions)
        eval_metrics = metrics_manager.eval(self.trainer_args.metrics) if self.trainer_args.metrics else {}
        logger.log_with_title(f"{dataset_role.name} Metrics", repr(eval_metrics))
        output.metrics.update(eval_metrics)
        return TracePredictionOutput(predictions=metrics_manager.get_scores(), label_ids=output.label_ids, metrics=output.metrics,
                                     source_target_pairs=dataset.get_source_target_pairs())

    def cleanup(self) -> None:
        """
        Free memory associated with trainer.
        :return: None
        """
        TraceAccelerator.clear()
        if self.model:
            del self.model

    @overrides(Trainer)
    def _get_train_sampler(self) -> Optional[torch.utils.data.Sampler]:
        """
        Gets the data sampler used for training
        :return: the train sampler
        """
        if self.trainer_args.use_balanced_batches and self.train_dataset is not None and DataKey.LABEL_KEY in self.train_dataset:
            return BalancedBatchSampler(data_source=self.train_dataset, batch_size=self._train_batch_size)
        return super()._get_train_sampler()

    def _get_dataset(self, dataset_role: DatasetRole) -> Optional[Dataset]:
        """
        Returns dataset set in role if it exists, otherwise none is returned.
        :param dataset_role: The role of the dataset to return.
        :return: Dataset at dataset role if it exists.
        """
        return self.trainer_dataset_manager[dataset_role].to_trainer_dataset(
            self.model_manager) if dataset_role in self.trainer_dataset_manager else None
