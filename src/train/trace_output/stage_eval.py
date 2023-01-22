from typing import Dict, Tuple, Union

import numpy as np

from train.save_strategy.save_strategy_stage import SaveStrategyStage
from train.trace_output.abstract_trace_output import AbstractTraceOutput

Metrics = Dict[str, float]
TracePredictions = Union[np.ndarray, Tuple[np.ndarray]]


class StageEval(AbstractTraceOutput):
    """
    Represents the evaluation of a stage.
    """
    stage: SaveStrategyStage
    iteration: int
    metrics: Metrics
