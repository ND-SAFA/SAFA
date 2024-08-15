from typing import Dict, List, Tuple, Union

import numpy as np

from tgen.core.save_strategy.save_strategy_stage import SaveStrategyStage
from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput

Metrics = Dict[str, float]
TracePredictions = Union[np.ndarray, Tuple[np.ndarray], List]


class StageEval(AbstractTraceOutput):
    """
    Represents the evaluation of a stage.
    """

    def __init__(self, stage: SaveStrategyStage, iteration: int, metrics: Metrics):
        """
        Constructs evaluation of stage for given iteration and stores associated metrics.
        :param stage: The stage being evaluated.
        :param iteration: The iteration of that stage.
        :param metrics: The metrics of the evaluation
        """
        super().__init__(hf_output=None)
        self.stage: SaveStrategyStage = stage
        self.iteration: int = iteration
        self.metrics: Metrics = metrics
