from typing import List, Optional, Union

from transformers.trainer_utils import TrainOutput

from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.stage_eval import StageEval
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput


class TraceTrainOutput(AbstractTraceOutput):
    """
    The output of training with the trace trainer.
    """

    def __init__(self, global_step: Optional[int] = None, training_loss: Optional[float] = None,
                 train_output: Union[TrainOutput, "TraceTrainOutput"] = None, metrics: Optional[List[StageEval]] = None,
                 prediction_output: TracePredictionOutput = None, training_time: float = None):
        """
        Provides wrapper method to convert output from default and custom training loop.
        :param global_step: The overall training step this output represents.
        :param training_loss: Overall loss during training.
        :param train_output: The training output.
        :param metrics: The metrics produced during evaluations during training.
        :param prediction_output: Output of the predictions on evaluation roles made during training.
        :param training_time: The total time occurring during training.
        """
        self.global_step: Optional[int] = global_step
        self.training_loss: Optional[float] = training_loss
        self.metrics: List[StageEval] = metrics
        self.training_time = training_time
        self.prediction_output = prediction_output
        super().__init__(hf_output=train_output)
