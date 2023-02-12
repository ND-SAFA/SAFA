from typing import List, Optional, Union

from transformers.trainer_utils import TrainOutput

from train.trace_output.abstract_trace_output import AbstractTraceOutput
from train.trace_output.stage_eval import StageEval
from train.trace_output.trace_prediction_output import TracePredictionOutput


class TraceTrainOutput(AbstractTraceOutput):
    """
    The output of training with the trace trainer.
    """

    def __init__(self, global_step: Optional[int] = None, training_loss: Optional[float] = None,
                 train_output: Union[TrainOutput, "TraceTrainOutput"] = None, metrics: Optional[List[StageEval]] = None,
                 val_metrics: Optional[List[StageEval]] = None,
                 prediction_output: TracePredictionOutput = None):
        """
        Provides wrapper method to convert output from default and custom training loop.
        :param train_output: The output of the training function.
        """
        self.global_step: Optional[int] = global_step
        self.training_loss: Optional[float] = training_loss
        self.metrics: List[StageEval] = metrics
        self.val_metrics: List[StageEval] = val_metrics
        self.prediction_output = prediction_output
        super().__init__(hf_output=train_output)
