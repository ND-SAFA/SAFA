import json
from typing import Any, Callable, Type
from uuid import UUID

from django.http import HttpRequest
from rest_framework import serializers

from tgen.common.constants.dataset_constants import NO_CHECK
from tgen.common.util.status import Status
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs


class ViewUtil:
    """
    Contains utility methods for handling requests threw views.
    """

    @staticmethod
    def run_job(abstract_job: AbstractJob, on_failure: Callable = None):
        """
        Runs job and performs error handling.
        :param abstract_job: The job to run.
        :param on_failure: Callback called after failure has occurred and job has been stopped.
        :return: The result of the job.
        """
        job_result = abstract_job.run()
        job_status = job_result.status
        job_result = job_result.to_json(as_dict=True)
        if job_status == Status.FAILURE:
            if on_failure:
                on_failure()
            raise Exception(job_result["body"])
        job_body = job_result["body"]
        return job_body

    @staticmethod
    def read_request(request: HttpRequest, serializer_class: Type[serializers.Serializer]) -> Any:
        """
        Converts a HttpRequest to a dictionary
        :param request: the HttpRequest
        :param serializer_class: The class used to serialize request body
        :return: a dictionary containing the information from the request body
        """
        data = json.loads(request.body)
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return obj, data

    @staticmethod
    def is_uuid(model_id: str, version=4) -> bool:
        """
        Returns whether given id is a uuid
        :param model_id: The model id to check.
        :param version: The UUID version.
        :return: True if uuid is given.
        """
        try:
            uuid_obj = UUID(model_id, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == model_id

    @staticmethod
    def create_job_args_from_api_definition(dataset_definition: ApiDefinition, **additional_args) -> JobArgs:
        """
        Creates job args from an api definition of a datset.
        :param dataset_definition: The api definition used for datasets.
        :param additional_args: Any additional args for the job.
        """
        eval_project_reader = ApiProjectReader(api_definition=dataset_definition)
        eval_dataset_creator = TraceDatasetCreator(project_reader=eval_project_reader, allowed_orphans=NO_CHECK)
        prompt_dataset_creator = PromptDatasetCreator(trace_dataset_creator=eval_dataset_creator,
                                                      project_summary=dataset_definition.summary)
        job_args = JobArgs(dataset_creator=prompt_dataset_creator, **additional_args)
        return job_args