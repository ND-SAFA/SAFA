from jobs.abstract_job import AbstractJob
from tracer.models.base_models.supported_base_model import SupportedBaseModel


class JobFactory:
    def __init__(self, baseModel: SupportedBaseModel, modelPath: str, outputDir: str):
        """
        Storage of job arguments and creator of jobs.
        """
        self.base_model = baseModel
        self.model_path = modelPath
        self.output_dir = outputDir
        raise NotImplementedError()

    def build(self, add_mount_directory_to_output: bool = True) -> AbstractJob:
        """
        Creates job using job argument and any additional parameters.
        :return: Job
        """
        raise NotImplementedError()
