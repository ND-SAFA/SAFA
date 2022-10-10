from abc import abstractmethod, ABC
from typing import Dict, List, Tuple

from common.models.base_models.supported_base_model import SupportedBaseModel
from common.models.model_generator import ModelGenerator
from trace.data.datasets.trace_dataset_creator import TraceDatasetCreator
from trace.jobs.trace_args import TraceArgs


class AbstractArgsBuilder(ABC):

    def __init__(self, base_model: SupportedBaseModel, model_path: str, output_dir: str, settings: dict = None):
        """
        Responsible for building training arguments for some pretrained model.
        :param base_model: supported base model name
        :param model_path: where the pretrained model will be loaded from
        :param output_dir: where the model will be saved to
        :param settings: additional parameters passed into ModelTraceArgs
        """
        self.base_model = base_model
        self.model_path = model_path
        self.output_dir = output_dir
        self.settings = settings if settings else {}

    def set_extra_attrs(self, **kwargs) -> None:
        """
        Sets additional attributes, not passed into init
        :param kwargs: additional attributes
        :return: None
        """
        for key, val in kwargs:
            if hasattr(self, key):
                setattr(self, key, val)

    def _build_model_generator(self):
        """
        Builds the model generator
        """
        return ModelGenerator(self.base_model, self.model_path)

    @abstractmethod
    def _build_trace_dataset(self):
        """
        Builds
        """
        pass

    @staticmethod
    def is_a_training_arg(arg_name):
        """
        Checks if a given arg name is a training attribute
        :return: True if the arg is a training attribute, else False
        """
        return arg_name in vars(TraceArgs).keys()

    @abstractmethod
    def build(self) -> TraceArgs:
        """
        Builds training arguments for some pretrained model.
        :return: Arguments for trace job including training and predicting trace links
        """
        pass

