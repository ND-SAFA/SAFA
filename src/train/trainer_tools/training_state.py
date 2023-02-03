import time
from typing import Any, Dict

import torch

from data.datasets.dataset_role import DatasetRole
from train.save_strategy.metric_save_strategy import MetricSaveStrategy
from train.save_strategy.save_strategy_stage import SaveStrategyStage
from train.trace_output.stage_eval import Metrics
from train.trace_output.trace_prediction_output import TracePredictionOutput
from train.trainer_tools.trace_accelerator import TraceAccelerator
from util.logging.logger_manager import logger


class TrainingMetrics:
    """
    Represents the metrics to use to evaluate training
    """

    def __init__(self):
        """
        Defaults all starting values
        """
        self.val_results: Dict[int, Metrics] = {}
        self.eval_results: Dict[int, Metrics] = {}
        self.epoch_losses: Dict[int, float] = {}
        self.curr_stage: SaveStrategyStage = SaveStrategyStage.STEP
        self.elapsed_time: float = -1

    def as_dict(self) -> Dict[str, Any]:
        """
        Returns the training metrics as a dictionary
        :return:
        """
        dict_ = vars(self)
        return dict_


class TrainingState:
    """
    Represents the current training state
    """

    def __init__(self, save_strategy: MetricSaveStrategy):
        """
        Defaults all starting values
        :param save_strategy: The save strategy to apply to eval and save model
        """
        self.save_strategy = save_strategy
        self.global_step = 0
        self.training_loss = 0
        self.curr_epoch_loss = 0
        self.curr_epoch_iteration = 0
        self.start_time = -1
        self.finish_time = -1
        self.training_metrics = TrainingMetrics()
        self.curr_stage = SaveStrategyStage.STEP

    def on_start(self) -> None:
        """
        Callback function called after training starts
        :return: None
        """
        self.start_time = time.perf_counter()
        logger.info(f"Number of workers: {TraceAccelerator.num_processes}. GPUs devices: {torch.cuda.device_count()}")

    def on_finish(self) -> None:
        """
        Callback function called after training finishes
        :return: None
        """
        self.finish_time = time.perf_counter()
        self.training_metrics.elapsed_time = self.finish_time - self.start_time

    def on_step(self, loss) -> bool:
        """
        Callback function called on each step
        :param loss: The step loss
        :return: True if the model should be evaluated after this step else False
        """
        self.curr_stage = SaveStrategyStage.STEP
        should_evaluate = self.save_strategy.should_evaluate(self.curr_stage, self.global_step)
        self.training_loss += loss.item()
        self.curr_epoch_loss += loss.item()
        self.global_step += 1
        return should_evaluate

    def on_epoch(self) -> bool:
        """
        Callback function called on each epoch
        :return: True if the model should be evaluated after this epoch else False
        """
        self.curr_stage = SaveStrategyStage.EPOCH
        logger.info(f"Epoch Loss: {self.curr_epoch_loss}")
        should_evaluate = self.save_strategy.should_evaluate(SaveStrategyStage.EPOCH, self.curr_epoch_iteration)
        self.training_metrics.epoch_losses[self.curr_epoch_iteration] = self.curr_epoch_iteration
        self.curr_epoch_iteration += 1
        self.curr_epoch_loss = 0
        return should_evaluate

    def on_eval(self, dataset_role: DatasetRole, prediction_output: TracePredictionOutput) -> bool:
        """
        Callback function called on each evaluation
        :param dataset_role: The dataset role used for the evaluation
        :param prediction_output: The results of the evaluation
        :return: True if the model should be saved after this evaluation else False
        """
        stage_iteration = (self.global_step if self.curr_stage == SaveStrategyStage.STEP else self.curr_epoch_iteration) - 1
        if dataset_role == DatasetRole.VAL:
            self.training_metrics.val_results[stage_iteration] = prediction_output.metrics
            previous_best = self.save_strategy.best_scores
            should_save = self.save_strategy.should_save(prediction_output.metrics, stage_iteration)
            if should_save:
                current_score = self.save_strategy.get_metric_scores(prediction_output.metrics)
                logger.log_with_title("Saving Best Model", f"New Best: {current_score}\tPrevious: {previous_best}")
            else:
                logger.info(f"Previous best is still {previous_best}.")
        else:
            self.training_metrics.eval_results[stage_iteration] = prediction_output.metrics
            should_save = False
        return should_save
