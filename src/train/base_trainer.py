import os
from typing import Any, Dict, Optional, Union

import torch
from accelerate import Accelerator
from transformers.trainer import Trainer

from data.datasets.dataset_role import DatasetRole
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from models.model_manager import ModelManager
from train.metrics.metrics_manager import MetricsManager
from train.save_strategy.abstract_save_strategy import AbstractSaveStrategy
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
    accelerator: Optional[Accelerator] = None

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
            self.save_strategy = MetricSaveStrategy(ComparisonCriterion("map"))
        super().__init__(model_init=model_init, args=trainer_args, tokenizer=tokenizer,
                         callbacks=trainer_args.callbacks,
                         **kwargs)

    def perform_training(self, checkpoint: str = None) -> TraceTrainOutput:
        """
        Performs the model training.
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        print("*" * 20, "Starting new training job", "-" * 20)
        with self.get_accelerator().main_process_first():
            self.model = self.model_manager.get_model()
            self.train_dataset = self.trainer_dataset_manager[DatasetRole.TRAIN].to_trainer_dataset(self.model_manager)
        print("*" * 20, "finished dataset construction", "-" * 20)
        train_output = self.train(resume_from_checkpoint=checkpoint)
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
        print(eval_metrics)
        output.metrics.update(eval_metrics)
        return TracePredictionOutput(predictions=metrics_manager.get_scores(), label_ids=output.label_ids, metrics=output.metrics,
                                     source_target_pairs=dataset.get_source_target_pairs())

    def get_accelerator(self) -> Accelerator:
        """
        Creates accelerator from the training arguments.
        :return: Constructed accelerator.
        """
        if self.accelerator is None:
            self.accelerator = Accelerator(gradient_accumulation_steps=self.trainer_args.gradient_accumulation_steps,
                                           split_batches=True, step_scheduler_with_optimizer=False)
        return self.accelerator

    def cleanup(self) -> None:
        """
        Free memory associated with trainer.
        :return: None
        """
        if self.accelerator:  # covers custom and non-custom
            self.accelerator.free_memory()
        if self.model:
            del self.model
