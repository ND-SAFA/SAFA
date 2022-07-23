from abc import abstractmethod
from typing import Union, List, Dict
from datasets import load_metric
from transformers.trainer_utils import PredictionOutput, TrainOutput
import numpy as np


# TODO
class BaseResults:

    def __init__(self, output: Union[PredictionOutput, TrainOutput]):
        self.output = output

    def evaluate(self, metric_names: List) -> Dict:
        metric = load_metric(*metric_names)
        preds = np.argmax(self.output.predictions, axis=-1)
        return metric.compute(predictions=preds, references=self.output.predictions.label_ids)
