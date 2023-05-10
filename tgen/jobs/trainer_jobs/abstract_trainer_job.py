import os
from abc import ABC
from dataclasses import dataclass
from typing import Any, Optional, Type, Union

from tgen.constants.experiment_constants import BEST_MODEL_NAME
from tgen.data.managers.deterministic_trainer_dataset_manager import DeterministicTrainerDatasetManager
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.data_jobs.create_datasets_job import CreateDatasetsJob
from tgen.models.model_manager import ModelManager
from tgen.train.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.base_object import BaseObject
from tgen.util.override import overrides
from tgen.util.reflection_util import ReflectionUtil
from tgen.variables.definition_variable import DefinitionVariable


class AbstractTrainerJob(AbstractJob, ABC):

    def __init__(self, model_manager: ModelManager, trainer_dataset_manager: TrainerDatasetManager, trainer_args: dataclass,
                 task: TrainerTask, job_args: JobArgs = None, **kwargs):
        """
        The base job class for tracing jobs
        :param job_args: the arguments for the job
        :param model_manager: the manages the model necessary for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param trainer_args: other arguments needed for the trainer
        """
        super().__init__(job_args=job_args, model_manager=model_manager)
        self.task = task
        self.trainer_dataset_manager = trainer_dataset_manager
        self.trainer_args = trainer_args
        self.kwargs = kwargs
        self._trainer: Optional[HuggingFaceTrainer] = None

    @overrides(AbstractJob)
    def run(self) -> None:
        """
        Runs the job and saves the output
        """
        if self.job_args.save_dataset_splits:
            CreateDatasetsJob(self.trainer_dataset_manager, self.job_args).run()
        return super().run()

    def _run(self, **kwargs) -> JobResult:
        """
        Runs the trainer job
        :return: The result of the job
        """
        if self.task == TrainerTask.TRAIN:
            output = self.get_trainer(**kwargs).perform_training()
        elif self.task == TrainerTask.PREDICT:
            output = self.get_trainer(**kwargs).perform_prediction()
        else:
            output = self._run_trainer_specific_task(**kwargs)
        return JobResult.from_trace_output(output) if isinstance(output, AbstractTraceOutput) else JobResult(body=output)

    def get_trainer(self, **kwargs) -> HuggingFaceTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = HuggingFaceTrainer(trainer_args=self.trainer_args,
                                               trainer_dataset_manager=self.trainer_dataset_manager,
                                               model_manager=self.model_manager, **kwargs)
        return self._trainer

    def cleanup(self) -> None:
        """
        Removes trainer from memory.
        :return: None
        """
        super().cleanup()
        if self._trainer:
            self._trainer.cleanup()
        self._trainer = None
        if self.trainer_dataset_manager:  # push model job has not dataset
            self.trainer_dataset_manager.cleanup()

    def load_best_model(self):
        """
        Loads the best model found during job.
        :return: The best model
        """
        self.model_manager.model_path = os.path.join(self.trainer_args.output_dir, BEST_MODEL_NAME)
        return self.model_manager.get_model()

    @classmethod
    @overrides(BaseObject)
    def _make_child_object(cls, definition: DefinitionVariable, expected_class: Type) -> Any:
        """
        Handles making children objects
        :param expected_class: the expected_class for the child obj
        :param definition: contains attributes necessary to construct the child
        :return: the child obj
        """
        expected_class = ReflectionUtil.get_target_class_from_type(expected_class)
        if ReflectionUtil.is_instance_or_subclass(expected_class, TrainerDatasetManager) \
                and DeterministicTrainerDatasetManager.DETERMINISTIC_KEY in definition:
            definition.pop(DeterministicTrainerDatasetManager.DETERMINISTIC_KEY)
            return DeterministicTrainerDatasetManager.initialize_from_definition(definition)
        return cls._make_child_object_helper(definition, expected_class)

    def _run_trainer_specific_task(self, **kwargs) -> Union[AbstractTraceOutput, dict]:
        """
        Runs a task that is specific to the trainer (may be implemented by child classes)
        :return: The output of the task run
        """
        raise RuntimeError("Task cannot be performed by this Trainer %s" % self.task)
