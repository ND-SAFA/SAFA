import os
from typing import Any, Dict, Union

import torch
from transformers.trainer import Trainer
from transformers.trainer_utils import PredictionOutput

from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from models.model_manager import ModelManager
from train.metrics.metrics_manager import MetricsManager
from train.save_strategy.save_strategy_stage import SaveStrategyStage
from train.trace_output.trace_prediction_output import TracePredictionOutput
from train.trace_output.trace_train_output import TraceTrainOutput
from train.trainer_args import TrainerArgs
from util.base_object import BaseObject

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
torch.use_deterministic_algorithms(True)

TRIAL = Union["optuna.Trial", Dict[str, Any]]


class TraceTrainer(Trainer, BaseObject):
    """
    Responsible for using given model for training and prediction using given data.
    """
    BEST_MODEL_NAME = "best"
    CURRENT_MODEL_NAME = "current"

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

    def perform_training(self, checkpoint: str = None) -> TraceTrainOutput:
        """
        Performs the model training.
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        self.model = self.model_manager.get_model()
        self.train_dataset = self.trainer_dataset_manager[DatasetRole.TRAIN].to_trainer_dataset(self.model_manager,
                                                                                                self.trainer_args.train_batch_size)
        train_output = self.train(resume_from_checkpoint=checkpoint)
        self.save_model()
        return TraceTrainOutput(train_output)

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

    def on_step(self, step_iteration: int) -> None:
        """
        Callback function called after every training step.
        :param step_iteration: The global step count of the training loop.
        :return: None
        """
        self.conditional_evaluate(SaveStrategyStage.STEP, step_iteration)

    def on_epoch(self, epoch_iteration: int) -> None:
        """
        Callback function called after every training epoch.
        :param epoch_iteration: The index of epoch performed.
        :return: None
        """
        self.conditional_evaluate(SaveStrategyStage.EPOCH, epoch_iteration)
        self.save_model(self.get_output_path(self.CURRENT_MODEL_NAME))

    def conditional_evaluate(self, stage: SaveStrategyStage, stage_iteration: int) -> None:
        """
        Conditionally evaluates model depending on save strategy and saves it if it is the current best.
        :param stage: The stage in training.
        :param stage_iteration: The number of times this stage has been reached.
        :return: None
        """
        save_strategy = self.trainer_args.custom_save_strategy
        should_evaluate = save_strategy.should_evaluate(stage, stage_iteration)

        if should_evaluate:
            eval_result = self.perform_prediction(DatasetRole.VAL)
            should_save = save_strategy.should_save(eval_result)
            if should_save:
                self.save_model(self.get_output_path(self.BEST_MODEL_NAME))

    def get_output_path(self, dir_name: str = None):
        """
        Returns the output path of trainer, with argument accessing directories within it.
        :param dir_name: The directory within the output path to retrieve.
        :return: The path to the trainer output or directory within it.
        """
        base_output_path = self.trainer_args.output_dir
        if dir_name:
            return os.path.join(base_output_path, dir_name)
        return base_output_path
