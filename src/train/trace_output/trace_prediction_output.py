from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, TypedDict, Union

import numpy as np
from transformers.trainer_utils import PredictionOutput

from train.trace_output.abstract_trace_output import AbstractTraceOutput
from train.trace_output.stage_eval import Metrics, TracePredictions
from util.reflection_util import ReflectionUtil


@dataclass
class TracePredictionEntry(TypedDict):
    """
    A trace prediction for a pair of artifacts.
    """
    source: str
    target: str
    score: float


class TracePredictionOutput(AbstractTraceOutput):
    """
    The output of predicting on the trace trainer.
    """

    def __init__(self, predictions: TracePredictions = None, label_ids: Optional[Union[np.ndarray, Tuple[np.ndarray]]] = None,
                 metrics: Optional[Metrics] = None, source_target_pairs: List[Tuple[str, str]] = None,
                 prediction_entries: List[TracePredictionEntry] = None,
                 prediction_output: PredictionOutput = None):
        self.predictions: TracePredictions = predictions
        self.label_ids = label_ids
        self.metrics = metrics
        self.source_target_pairs = source_target_pairs
        self.prediction_entries = prediction_entries
        super().__init__(hf_output=prediction_output)
        self.set_prediction_entries()

    def set_prediction_entries(self) -> None:
        """
        Generates the predictions for each target pair and stores them in prediction entries.
        :return: None
        """
        if self.predictions is None or self.source_target_pairs is None:
            return

        self.prediction_entries = [TracePredictionEntry(source=pred_ids[0], target=pred_ids[1], score=float(pred_scores))
                                   for pred_ids, pred_scores in zip(self.source_target_pairs, self.predictions)]

    def toJSON(self) -> Dict:
        return ReflectionUtil.get_fields(self)
