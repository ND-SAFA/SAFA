from typing import Dict, List, Optional, Tuple, TypedDict, Union

import numpy as np
from transformers.trainer_utils import TrainOutput

from train.save_strategy.save_strategy_stage import SaveStrategyStage
from util.reflection_util import ReflectionUtil

Metrics = Dict[str, float]
TracePredictions = Union[np.ndarray, Tuple[np.ndarray]]


class StageEval(TypedDict):
    """
    Represents the evaluation of a stage.
    """
    stage: SaveStrategyStage
    iteration: int
    metrics: Metrics


class TraceTrainOutput:
    """
    The output of training with the trace trainer.
    """

    def __init__(self, train_output: Union[TrainOutput, "TraceTrainOutput"]):
        """
        Provides wrapper method to convert output from default and custom training loop.
        :param train_output: The output of the training function.
        """
        self.global_step: Optional[int] = None
        self.training_loss: Optional[float] = None
        self.metrics: List[StageEval] = []
        self.eval_metrics: List[StageEval] = []
        ReflectionUtil.copy_attributes(train_output, self)


class TracePredictionOutput(TypedDict):
    """
    The output of predicting on the trace trainer.
    """
    predictions: TracePredictions
    label_ids: Optional[Union[np.ndarray, Tuple[np.ndarray]]]
    metrics: Optional[Dict[str, float]]
    source_target_pairs: List[Tuple[str, str]]


class TraceEvalOutput(TypedDict):
    """
    The output of evaluating a set of predictions on the trace trainer.
    """
