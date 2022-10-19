from jobs.abstract_job import AbstractJob
from server.storage.safa_storage import SafaStorage
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.models.model_generator import ModelGenerator


class JobFactory:
    def __init__(self, baseModel: SupportedBaseModel, modelPath: str, outputDir: str):
        """
        Storage of job arguments and creator of jobs.
        """
        self.base_model = baseModel
        self.model_path = modelPath
        self.output_dir = outputDir
        raise NotImplementedError()

    def build_model_generator(self) -> ModelGenerator:
        """
        Builds the model generator for the job
        """
        return ModelGenerator(base_model=self.base_model, model_path=self.model_path)

    def build(self, add_mount_directory_to_output: bool = True) -> AbstractJob:
        """
        Creates job using job argument and any additional parameters.
        :return: Job
        :rtype:
        """
        model_generator = self.build_model_generator()
        output_dir = SafaStorage.add_mount_directory(self.output_dir) if add_mount_directory_to_output else self.output_dir
        raise NotImplementedError()
