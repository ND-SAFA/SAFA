from typing import Any, Type

from jobs.predict_job import PredictJob
from models.llama.llama_model_manager import LLaMAModelManager
from models.model_manager import ModelManager
from util.reflection_util import ReflectionUtil
from variables.definition_variable import DefinitionVariable


class LLaMAPredictJob(PredictJob):

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
