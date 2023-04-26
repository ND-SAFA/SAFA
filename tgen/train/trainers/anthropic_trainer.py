from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.train.trace_output.trace_train_output import TraceTrainOutput
from tgen.train.trainers.abstract_trainer import AbstractTrainer


class AnthropicTrainer(AbstractTrainer):
    """
    Provides interface for accessing anthropic's Claude LLM.
    """

    def perform_training(self) -> TraceTrainOutput:
        raise NotImplementedError()

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL, dataset: iDataset = None) -> TracePredictionOutput:
        raise NotImplementedError()

    def cleanup(self) -> None:
        raise NotImplementedError()
