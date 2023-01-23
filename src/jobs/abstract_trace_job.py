from abc import ABC
from typing import Any, Optional, Type

from config.override import overrides
from data.datasets.managers.deterministic_trainer_dataset_manager import DeterministicTrainerDatasetManager
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.create_datasets_job import CreateDatasetsJob
from models.model_manager import ModelManager
from train.base_trainer import BaseTrainer
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs
from util.base_object import BaseObject
from util.reflection_util import ReflectionUtil
from variables.definition_variable import DefinitionVariable


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, job_args: JobArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, trainer_args: TrainerArgs):
        """
        The base job class for tracing jobs
        :param job_args: the arguments for the job
        :param model_manager: the manages the model necessary for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param trainer_args: other arguments needed for the trainer
        """
        if not model_manager.model_output_path:
            model_manager.model_output_path = trainer_args.output_dir
        super().__init__(job_args=job_args, model_manager=model_manager)
        self.trainer_dataset_manager = trainer_dataset_manager
        self.trainer_args = trainer_args
        self._trainer: Optional[TraceTrainer] = None

    @overrides(AbstractJob)
    def run(self) -> None:
        """
        Runs the job and saves the output
        """
        if self.job_args.save_dataset_splits:
            CreateDatasetsJob(self.job_args, self.trainer_dataset_manager).run()
        super().run()

    def get_trainer(self, **kwargs) -> BaseTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = TraceTrainer(trainer_args=self.trainer_args,
                                         trainer_dataset_manager=self.trainer_dataset_manager,
                                         model_manager=self.model_manager, **kwargs)
        return self._trainer

    def cleanup(self) -> None:
        """
        Removes trainer from memory.
        :return: None
        """
        super().cleanup()
        if hasattr(self._trainer, "accelerator") and self._trainer.accelerator:  # covers custom and non-custom
            self._trainer.accelerator.free_memory()
        self._trainer = None
        self.trainer_dataset_manager.cleanup()

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
            return DeterministicTrainerDatasetManager.initialize_from_definition(definition)
        return cls._make_child_object_helper(definition, expected_class)
