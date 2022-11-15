from typing import Type

from jobs.abstract_job import AbstractJob


class JobFactory:
    def __init__(self, **kwargs):
        """
        Storage of job arguments and creator of jobs.
        """
        self.kwargs = kwargs
        self.replace_map = {
            "load_from_storage": "add_mount_directory_to_output"
        }

    def build(self, job_class: Type[AbstractJob]) -> AbstractJob:
        """
        Creates job using job argument and any additional parameters.
        :return: Job
        """
        kwargs = {}
        for property_name, property_value in vars(job_class):
            native_name = property_name
            if property_name in self.replace_map:
                native_name = self.replace_map[property_name]
            kwargs[property_name] = self.kwargs[native_name]
        return job_class(**kwargs)

    def __getattr__(self, attribute_name):
        if attribute_name in self.__dict__:
            return super().__getattribute__(attribute_name)
        elif attribute_name in self.kwargs:
            return self.kwargs[attribute_name]
        else:
            error = "%s does not contain field: %s" % (self.__class__.__name__, attribute_name)
            raise AttributeError(error)
