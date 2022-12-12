import os
from typing import Any, Dict, List, Type

import tensorflow as tf
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
from rest_framework import serializers

from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult
from jobs.job_factory import JobFactory

load_dotenv()


class BaseScript:
    """
    Container for script that creates and runs job.
    """

    def __init__(self, serializer: Type[serializers.Serializer], job: Type[AbstractJob]):
        """
        Initializes script with arguments, serializer, and job with default path variables.
        :param args: The arguments to the script. A result of calling parse_args on ArgumentParser.
        :param serializer: The serializer used to read JSON data.
        :param job: The job constructed by serializer.
        :param path_vars: The arguments whose paths should be verified and expanded if contains user shortcut.
        """
        self.serializer = serializer
        self.job = job
        self.application = get_wsgi_application()
        print("GPUS : ", tf.config.list_physical_devices('GPU'))

    def run(self, data: Dict, path_vars=None):
        """
        Serializes data into job and runs it.
        :param data: The data read by serializer to create the job.
        :param path_vars: The path variable to verify exists.
        :return: None
        """
        if path_vars is None:
            path_vars = []
        self.assert_path_vars_exists(data, path_vars)
        serializer = self.serializer(data=data)
        assert serializer.is_valid(), serializer.errors
        job_factory: JobFactory = serializer.save()
        job = job_factory.build(self.job)
        job.run()
        print(job.result.to_json([JobResult.VAL_METRICS, JobResult.METRICS]))

    @staticmethod
    def assert_path_vars_exists(args: Dict, path_vars: List[str]):
        """
        Expands each path variable and verifies that file or directory exists.
        :return: None
        """
        for path_var in path_vars:
            if isinstance(path_var, list):
                path_value = BaseScript.get_path(path_var, args)
                path_value = os.path.expanduser(path_value)
                assert os.path.exists(path_value), path_value
                BaseScript.set_path(path_var, args, path_value)
            elif path_var in args:
                path_value = args[path_var]
                path_value = os.path.expanduser(path_value)
                assert os.path.exists(path_value), path_value
                args[path_var] = path_value

    @staticmethod
    def get_path(path: List[str], obj: dict):
        if len(path) == 0:
            return obj
        current_path = path[0]
        next_paths = path[1:]
        assert current_path in obj, "Expected %s to exist in %s." % (current_path, obj)
        return BaseScript.get_path(next_paths, obj[current_path])

    @staticmethod
    def set_path(path: List[str], obj: dict, value: Any):
        if len(path) == 1:
            obj[path[0]] = value
            return
        return BaseScript.set_path(path[1:], obj[path[0]], value)
