from abc import abstractmethod
from typing import Union, List, Dict
from datasets import load_metric
from transformers.trainer_utils import PredictionOutput, TrainOutput
import numpy as np
from metrics.supported_metrics import get_metric_path


# TODO
class BaseResult:

    def __init__(self, output: Union[PredictionOutput, TrainOutput]):
        self.output = output

    def evaluate(self, metric_names: List) -> Dict:
        metric_paths = [get_metric_path(name) for name in metric_names]
        metric = load_metric(*metric_paths)
        preds = np.argmax(self.output.predictions, axis=-1)
        return metric.compute(predictions=preds, references=self.output.predictions.label_ids)
