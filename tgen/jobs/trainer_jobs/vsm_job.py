from typing import List, Optional

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.models.model_manager import ModelManager
from tgen.train.args.hugging_face_args import HuggingFaceArgs
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trace_output.trace_train_output import TraceTrainOutput
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.train.trainers.vsm_trainer import VSMTrainer
from tgen.util.override import overrides


class VSMJob(AbstractTrainerJob):
    """
    Handles VSM training + prediction
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, job_args: JobArgs = None, metrics: List[str] = None):
        """
        Handles VSM training + prediction
        :param job_args: the arguments for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param metrics: List of metric names to use for evaluation
        """
        if metrics is None:
            metrics = SupportedTraceMetric.get_keys()
        super().__init__(model_manager=ModelManager("VSM"), trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=HuggingFaceArgs(output_dir=job_args.output_dir), job_args=job_args, task=TrainerTask.TRAIN)
        self.metrics = metrics
        self._trainer: Optional[VSMTrainer] = None

    @overrides(AbstractTrainerJob)
    def _run(self) -> JobResult:
        """
        Performs predictions and (optionally) evaluation of model
        :return: results of the prediction including prediction values and associated ids
        """
        trainer = self.get_trainer()
        training_output = trainer.perform_training()
        prediction_output = trainer.perform_prediction()
        train_output = TraceTrainOutput(prediction_output=prediction_output, training_time=training_output.training_time)
        return JobResult.from_trace_output(train_output)

    def get_trainer(self) -> AbstractTrainer:
        """
        Gets the VSM trainer for the job
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = VSMTrainer(trainer_dataset_manager=self.trainer_dataset_manager, metrics=self.metrics)
        return self._trainer
