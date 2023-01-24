import os
from typing import Any, Dict, Union

import torch
from transformers.trainer import Trainer
from transformers.trainer_utils import PredictionOutput

from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from models.model_manager import ModelManager
from train.metrics.metrics_manager import MetricsManager
from train.save_strategy.comparison_criteria import ComparisonCriterion
from train.save_strategy.epoch_save_strategy import MetricSaveStrategy
from train.trace_output.trace_prediction_output import TracePredictionOutput
from train.trace_output.trace_train_output import TraceTrainOutput
from train.trainer_args import TrainerArgs
from util.base_object import BaseObject

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
torch.use_deterministic_algorithms(True)

TRIAL = Union["optuna.Trial", Dict[str, Any]]


class BaseTrainer(Trainer, BaseObject):
    """
    Trains model on data for generic task.
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
        if trainer_args.custom_save_strategy is None:
            self.trainer_args.custom_save_strategy = MetricSaveStrategy(ComparisonCriterion("f2"))
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
        train_output = self.train(resume_from_checkpoint=checkpoint)
        return TraceTrainOutput(train_output=train_output)

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :return: A dictionary containing the results.
        """
        dataset = self.trainer_dataset_manager[dataset_role]
        self.eval_dataset = dataset.to_trainer_dataset(self.model_manager)
        output: PredictionOutput = self.predict(self.eval_dataset)
        metrics_manager = MetricsManager(dataset.get_ordered_links(), output.predictions)
        eval_metrics = metrics_manager.eval(self.trainer_args.metrics) if self.trainer_args.metrics else {}
        output.metrics.update(eval_metrics)
        return TracePredictionOutput(predictions=metrics_manager.get_scores(), label_ids=output.label_ids, metrics=output.metrics,
                                     source_target_pairs=dataset.get_source_target_pairs())

    def cleanup(self) -> None:
        """
        Free memory associated with trainer.
        :return: None
        """
