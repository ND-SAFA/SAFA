from typing import List, Optional

from data.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from train.itrainer import iTrainer
from train.trace_output.trace_train_output import TraceTrainOutput
from train.vsm_trainer import VSMTrainer


class VSMJob(AbstractJob):
    """
    Handles VSM training + prediction
    """

    def __init__(self, job_args: JobArgs, trainer_dataset_manager: TrainerDatasetManager, metrics: List[str] = None):
        """
        Handles VSM training + prediction
        :param job_args: the arguments for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param metrics: List of metric names to use for evaluation
        """
        super().__init__(job_args=job_args, model_manager=None)
        self.trainer_dataset_manager = trainer_dataset_manager
        self.metrics = metrics
        self._trainer: Optional[VSMTrainer] = None

    def _run(self) -> JobResult:
        """
        Performs predictions and (optionally) evaluation of model
        :return: results of the prediction including prediction values and associated ids
        """
        self.get_trainer().perform_training()
        prediction_output = self.get_trainer().perform_prediction()
        train_output = TraceTrainOutput(prediction_output=prediction_output)
        return JobResult.from_trace_output(train_output)

    def get_trainer(self) -> iTrainer:
        """
        Gets the VSM trainer for the job
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = VSMTrainer(trainer_dataset_manager=self.trainer_dataset_manager, metrics=self.metrics)
        return self._trainer

    def load_best_model(self) -> None:
        """
        Under construction. Best model is current not used.
        :return:
        """
