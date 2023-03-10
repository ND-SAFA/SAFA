import os

from transformers.integrations import WandbCallback
from typing import Type, Any

from constants import BEST_MODEL_NAME
from data.datasets.dataset_role import DatasetRole
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult
from jobs.train_job import TrainJob
from models.llama_model_manager import LLaMAModelManager
from models.model_manager import ModelManager
from util.reflection_util import ReflectionUtil
from variables.definition_variable import DefinitionVariable


class LLaMATrainJob(TrainJob):

    @classmethod
    def _make_child_object(cls, definition: DefinitionVariable, expected_class: Type) -> Any:
        """
        Handles making children objects
        :param expected_class: the expected_class for the child obj
        :param definition: contains attributes necessary to construct the child
        :return: the child obj
        """
        if ReflectionUtil.is_instance_or_subclass(expected_class, ModelManager):
            expected_class = LLaMAModelManager
        return super()._make_child_object(definition, expected_class)