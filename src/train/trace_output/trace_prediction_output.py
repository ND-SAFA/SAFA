from typing import Dict, List, Optional, Tuple, Union

import numpy as np
from transformers.trainer_utils import PredictionOutput

from train.trace_output.abstract_trace_output import AbstractTraceOutput
from train.trace_output.stage_eval import TracePredictions


class TracePredictionOutput(AbstractTraceOutput):
    """
    The output of predicting on the trace trainer.
    """

    def __init__(self, prediction_output: PredictionOutput = None, **kwargs):
        self.predictions: TracePredictions = None
        self.label_ids: Optional[Union[np.ndarray, Tuple[np.ndarray]]] = None
        self.metrics: Optional[Dict[str, float]] = None
        self.source_target_pairs: List[Tuple[str, str]] = None
        super().__init__(prediction_output, **kwargs)
