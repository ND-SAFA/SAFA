from typing import List, Optional

from gen_common.data.managers.trainer_dataset_manager import TrainerDatasetManager
from gen_common.data.tdatasets.dataset_role import DatasetRole
from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs
from gen_common.traceability.metrics.supported_trace_metric import SupportedTraceMetric
from gen_common.traceability.output.trace_train_output import TraceTrainOutput
from gen_common.traceability.vsm.vsm_trainer import VSMTrainer


class VSMJob(AbstractJob):
    """
    Handles VSM training + prediction
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, job_args: JobArgs = None, metrics: List[str] = None, **kwargs):
        """
        Handles VSM training + prediction
        :param job_args: the arguments for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param metrics: List of metric names to use for evaluation
        """
        super().__init__(job_args)
        if metrics is None:
            metrics = SupportedTraceMetric.get_keys()
        self.trainer_dataset_manager = trainer_dataset_manager
        self.metrics = metrics
        self._trainer: Optional[VSMTrainer] = None
        self.trainer_kwargs = kwargs

    def _run(self) -> TraceTrainOutput:
        """
        Performs predictions and (optionally) evaluation of model
        :return: results of the prediction including prediction values and associated ids
        """
        trainer: VSMTrainer = self.get_trainer()
        train_dataset_role = DatasetRole.TRAIN if DatasetRole.TRAIN in self.trainer_dataset_manager else DatasetRole.EVAL
        training_output = trainer.perform_training(train_dataset_role)
        prediction_output = trainer.perform_prediction()
        train_output = TraceTrainOutput(prediction_output=prediction_output, training_time=training_output.training_time)
        return train_output

    def get_trainer(self) -> VSMTrainer:
        """
        Gets the VSM trainer for the job
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = VSMTrainer(trainer_dataset_manager=self.trainer_dataset_manager, metrics=self.metrics,
                                       **self.trainer_kwargs)
        return self._trainer
