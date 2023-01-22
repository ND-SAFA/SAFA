from typing import List, Optional, Union

from transformers.trainer_utils import TrainOutput

from train.trace_output.abstract_trace_output import AbstractTraceOutput
from train.trace_output.stage_eval import StageEval


class TraceTrainOutput(AbstractTraceOutput):
    """
    The output of training with the trace trainer.
    """

    def __init__(self, train_output: Union[TrainOutput, "TraceTrainOutput"] = None, **kwargs):
        """
        Provides wrapper method to convert output from default and custom training loop.
        :param train_output: The output of the training function.
        """
        self.global_step: Optional[int] = None
        self.training_loss: Optional[float] = None
        self.metrics: List[StageEval] = []
        self.eval_metrics: List[StageEval] = []
        super().__init__(train_output, **kwargs)
