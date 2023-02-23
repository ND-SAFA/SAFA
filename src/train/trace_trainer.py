import os
from typing import Any, Dict, Optional, Tuple, Union

import torch
from datasets import Dataset
from transformers.trainer import Trainer
from transformers.trainer_utils import PredictionOutput

from data.datasets.data_key import DataKey
from data.datasets.dataset_role import DatasetRole
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from data.samplers.balanced_batch_sampler import BalancedBatchSampler
from models.model_manager import ModelManager
from train.itrainer import iTrainer
from train.metrics.metrics_manager import MetricsManager
from train.save_strategy.abstract_save_strategy import AbstractSaveStrategy
from train.save_strategy.comparison_criteria import ComparisonCriterion
from train.save_strategy.metric_save_strategy import MetricSaveStrategy
from train.trace_output.trace_prediction_output import TracePredictionOutput
from train.trace_output.trace_train_output import TraceTrainOutput
from train.trainer_args import TrainerArgs
from train.trainer_tools.trace_accelerator import TraceAccelerator
from train.wandb.trace_callback import TraceCallback
from util.base_object import BaseObject
from util.logging.logger_manager import logger
from util.override import overrides

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
TRIAL = Union["optuna.Trial", Dict[str, Any]]


class TraceTrainer(Trainer, iTrainer, BaseObject):
    """
    Trains model on data for generic task.
    """

    def __init__(self, trainer_args: TrainerArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, save_strategy: AbstractSaveStrategy = None, **kwargs):
        """
        Handles the training and evaluation of learning models
        :param trainer_args: The learning model arguments
        :param model_manager: The manager for the model used for training and/or predicting
        :param trainer_dataset_manager: The manager for the datasets used for training and/or predicting
        :param save_strategy: The strategy used to save the best model
        :param kwargs: Any additional arguments given to the HF Trainer
        """
        self.trainer_args = trainer_args
        self.trainer_dataset_manager = trainer_dataset_manager
        self.model_manager = model_manager
        self.model_manager.set_max_seq_length(self.trainer_args.max_seq_length)
        self.trainer_args.remove_unused_columns = False
        callbacks = [TraceCallback()]
        model_init = lambda: self.model_manager.get_model()
        tokenizer = self.model_manager.get_tokenizer()
        if save_strategy is None:
            self.save_strategy = MetricSaveStrategy(ComparisonCriterion(["map", "f2"]))
        super().__init__(model_init=model_init, args=trainer_args, tokenizer=tokenizer, callbacks=callbacks, **kwargs)

    def perform_training(self, checkpoint: str = None) -> TraceTrainOutput:
        """
        Performs the model training.
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        self.compute_metrics = self._compute_validation_metrics  # Will compute trace metrics alongside default eval metrics
        self.model = self.model_manager.get_model()
        self.train_dataset = self.trainer_dataset_manager[DatasetRole.TRAIN].to_hf_dataset(self.model_manager)
        self.eval_dataset = self._get_dataset(DatasetRole.VAL)
        train_output = self.train(resume_from_checkpoint=checkpoint)
        self.eval_dataset = self._get_dataset(DatasetRole.EVAL)
        self.compute_metrics = None  # Turn off since prediction uses custom logic surrounding computing metrics.
        return TraceTrainOutput(train_output=train_output)

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :return: THe prediction output
        """
        dataset = self.trainer_dataset_manager[dataset_role]
        self.eval_dataset = dataset.to_hf_dataset(self.model_manager)
        output = self.predict(self.eval_dataset)
        eval_metrics, metrics_manager = self._compute_trace_metrics(output, dataset_role)
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
        if self.trainer_args.use_balanced_batches and self.train_dataset is not None and DataKey.LABEL_KEY in self.train_dataset[0]:
            return BalancedBatchSampler(data_source=self.train_dataset, batch_size=self._train_batch_size)
        return super()._get_train_sampler()

    def _compute_validation_metrics(self, output: PredictionOutput, dataset_role: DatasetRole = DatasetRole.VAL) -> Dict:
        """
        Callback that allows Trainer to compute trace metrics on validation set.
        :param output:The prediction output on a trace dataset.
        :return: Trace metrics associated with prediction.
        """
        trace_metrics, _ = self._compute_trace_metrics(output, dataset_role=dataset_role)
        return trace_metrics

    def _compute_trace_metrics(self, output: PredictionOutput, dataset_role: DatasetRole) -> Tuple[Dict, MetricsManager]:
        """
        Computes the traces metric on given trace output using trace information from dataset role.
        :param output: The output of a prediction on a trace dataset.
        :param dataset_role: The role of the trace dataset being predicted (used for source-target labels).
        :return: Trace metrics and metrics manager used to calculate them.
        """
        dataset = self.trainer_dataset_manager[dataset_role]
        n_predictions, n_expected = len(output.predictions), len(self.eval_dataset)
        assert n_predictions == n_expected, f"Expected {n_expected} samples but received {n_predictions} predictions."
        assert len(dataset) == n_expected, f"Found dataset ({len(dataset)}) does not required links ({n_expected})."
        metrics_manager = MetricsManager(dataset.get_ordered_links(), output.predictions)
        trace_metrics = metrics_manager.eval(self.trainer_args.metrics) if self.trainer_args.metrics else {}
        return trace_metrics, metrics_manager

    def _get_dataset(self, dataset_role: DatasetRole) -> Optional[Dataset]:
        """
        Returns dataset set in role if it exists, otherwise none is returned.
        :param dataset_role: The role of the dataset to return.
        :return: Dataset at dataset role if it exists.
        """
        return self.trainer_dataset_manager[dataset_role].to_hf_dataset(
            self.model_manager) if dataset_role in self.trainer_dataset_manager else None
