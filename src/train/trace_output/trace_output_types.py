from typing import Dict, List, NamedTuple, Tuple

from transformers.trainer_utils import PredictionOutput, TrainOutput

from train.save_strategy.abstract_save_strategy import SaveStrategyStage

Metrics = Dict[str, float]


class StageEval(NamedTuple):
    """
    Represents the evaluation of a stage.
    """
    stage: SaveStrategyStage
    iteration: int
    metrics: Metrics


class TraceTrainOutput(TrainOutput):
    """
    The trace_output of training with the trace trainer.
    """
    eval_metrics: List[StageEval]


class TracePredictionOutput(PredictionOutput):
    """
    The trace_output of predicting on the trace trainer.
    """
    source_target_pairs: List[Tuple[str, str]]


class TraceEvalOutput(NamedTuple):
    """
    The trace_output of evaluating a set of predictions on the trace trainer.
    """
