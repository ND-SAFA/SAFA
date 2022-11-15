from typing import Dict, List, Tuple

from jobs.abstract_job import AbstractJob
from tracer.models.base_models.supported_base_model import SupportedBaseModel


class JobFactory:
    def __init__(self, base_model: SupportedBaseModel, model_path: str, output_dir: str, load_from_storage: bool,
                 source_layers: List[Dict[str, str]] = None, target_layers: List[Dict[str, str]] = None,
                 settings: Dict[str, str] = None, links: List[Tuple[str, str]] = None):
        """
        Storage of job arguments and creator of jobs.
        """
        self.base_model = base_model
        self.model_path = model_path
        self.output_dir = output_dir
        self.load_from_storage = load_from_storage
        self.source_layers = source_layers
        self.target_layers = target_layers
        self.links = links
        self.settings = settings

    def build(self, add_mount_directory_to_output: bool = True) -> AbstractJob:
        """
        Creates job using job argument and any additional parameters.
        :return: Job
        """
        raise NotImplementedError()
