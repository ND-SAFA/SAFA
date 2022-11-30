from typing import Dict

from jobs.job_factory import JobFactory
from server.serializers.serializer_utility import SerializerUtility
from tracer.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.datasets.dataset_role import DatasetRole
from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer
from tracer.pre_processing.pre_processing_steps import PreProcessingSteps
from tracer.pre_processing.steps.abstract_pre_processing_step import AbstractPreProcessingStep
from util.reflection_util import ParamScope, ReflectionUtil


class JobFactoryConverter:
    """
    Class responsible for converting JobFactory entities into their JSON representation.
    """

    @staticmethod
    def create_job_factory(serialized_data: Dict) -> JobFactory:
        # TODO: Should not need to call this whenever you want to create a job factory.
        """
        Creates job factory from serialized data.
        :param serialized_data: Validated and processed data from subclass of ModelIdentifierSerializer.
        :return: JobFactory
        :rtype:
        """
        params = serialized_data.pop("params")
        return JobFactory(**serialized_data, **params)

    @staticmethod
    def job_factory_representation(instance: JobFactory, ignore_vars=None) -> Dict:
        """
        Converts JobFactory into JSON representation
        :param instance: The job factory to convert.
        :return: The JSON representation.
        """
        data = {
            "params": instance.additional_job_params,
        }
        # 1. Get fields to serialize
        ignore_vars = ignore_vars if ignore_vars else ["additional_job_params"]
        fields = ReflectionUtil.get_fields(instance, ParamScope.LOCAL, ignore=ignore_vars)
        fields = {SerializerUtility.to_camel_case(k): v for k, v in fields.items()}
        # 2. Extract dataset used in request
        if instance.trainer_dataset_container:
            dataset = JobFactoryConverter.__get_dataset_creator(instance.trainer_dataset_container)
            dataset_representation = JobFactoryConverter.abstract_dataset_creator_representation(dataset)
            data["data"] = dataset_representation
        # 3. Create payload with settings, data, and fields
        data.update(fields)
        return data

    @staticmethod
    def __get_dataset_creator(dataset_container: TrainerDatasetsContainer) -> AbstractDatasetCreator:
        if DatasetRole.TRAIN in dataset_container:
            return dataset_container.get_creator(DatasetRole.TRAIN)
        if DatasetRole.EVAL in dataset_container:
            return dataset_container.get_creator(DatasetRole.EVAL)
        raise ValueError("Dataset not defined.")

    @staticmethod
    def abstract_dataset_creator_representation(instance: AbstractDatasetCreator) -> Dict:
        """
        Exports dataset creator to its API format.
        :param instance: The dataset creator to deserialize.
        :return: Dictionary containing API json.
        """
        steps = instance._pre_processor.steps
        steps_representation = [JobFactoryConverter.abstract_pre_processing_step_representation(step) for step in steps]
        return {
            "creator": ReflectionUtil.get_enum_key(SupportedDatasetCreator, instance),
            "params": ReflectionUtil.get_fields(instance, ParamScope.LOCAL),
            "preProcessingSteps": steps_representation
        }

    @staticmethod
    def abstract_pre_processing_step_representation(instance: AbstractPreProcessingStep):
        """
        Converts AbstractPreProcessingStep into JSON data.
        :param instance: The pre-processing step to convert.
        :return: Dictionary representing JSON representation.
        """
        return {
            "step": ReflectionUtil.get_enum_key(PreProcessingSteps, instance),
            "params": ReflectionUtil.get_fields(instance, ParamScope.LOCAL)
        }
