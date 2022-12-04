import os
from typing import Dict, List, Type

import tensorflow as tf
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
from rest_framework import serializers

from jobs.abstract_job import AbstractJob
from jobs.job_factory import JobFactory

load_dotenv()


class BaseScript:
    """
    Container for script that creates and runs job.
    """

    def __init__(self, args, serializer: Type[serializers.Serializer], job: Type[AbstractJob],
                 path_vars: List[str] = None):
        """
        Initializes script with arguments, serializer, and job with default path variables.
        :param args: The arguments to the script. A result of calling parse_args on ArgumentParser.
        :param serializer: The serializer used to read JSON data.
        :param job: The job constructed by serializer.
        :param path_vars: The arguments whose paths should be verified and expanded if contains user shortcut.
        """
        self.args = args
        self.serializer = serializer
        self.job = job
        self.path_vars = path_vars if path_vars else ["data", "output"]
        self.application = get_wsgi_application()
        self.assert_path_vars_exists()
        print("# of gpus: ", tf.config.list_physical_devices('GPU'))

    def assert_path_vars_exists(self):
        """
        Expands each path variable and verifies that file or directory exists.
        :return: None
        """
        for path_var in self.path_vars:
            path_value = getattr(self.args, path_var)
            path_value = os.path.expanduser(path_value)
            setattr(self.args, path_var, path_value)
            assert os.path.exists(path_value), path_value

    def run(self, data: Dict):
        """
        Serializes data into job and runs it.
        :param data: The data read by serializer to create the job.
        :return: None
        """
        serializer = self.serializer(data=data)
        assert serializer.is_valid(), serializer.errors
        job_factory: JobFactory = serializer.save()
        job = job_factory.build(self.job)
        job.run()
