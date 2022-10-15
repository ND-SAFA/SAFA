from typing import Dict, List, Tuple

from dataset.dataset_creators.trace_dataset_creator import TraceDatasetCreator
from jobs.abstract_args_builder import AbstractArgsBuilder
from jobs.trace_args import TraceArgs
from models.base_models.supported_base_model import SupportedBaseModel
from models.model_generator import ModelGenerator


class TraceArgsBuilder(AbstractArgsBuilder):

    def __init__(self, base_model: SupportedBaseModel, model_path: str, output_dir: str,
                 source_layers: List[Dict[str, str]] = None,
                 target_layers: List[Dict[str, str]] = None, links: List[Tuple[str, str]] = None,
                 pretraining_data_path: str = None, settings: dict = None):
        """
        Responsible for building training arguments for some pretrained model.
        :param base_model: supported base model name
        :param model_path: where the pretrained model will be loaded from
        :param output_dir: where the model will be saved to
        :param source_layers: mapping between source artifact ids and their tokens
        :param target_layers: mapping between target artifact ids and their tokens
        :param links: list of true links to fine-tune on
        :param settings: additional parameters passed into ModelTraceArgs
        """
        self.base_model = base_model
        self.links = links
        self.model_path = model_path
        self.output_dir = output_dir
        self.source_layers = source_layers
        self.target_layers = target_layers
        self.pretraining_data_path = pretraining_data_path
        self.settings = settings if settings else {}
        self.dataset_creator: TraceDatasetCreator = None

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
        return ModelGenerator(self.base_model, self.model_path)

    def _build_trace_dataset(self):
        return TraceDatasetCreator(source_layers=self.source_layers, target_layers=self.target_layers,
                                   true_links=self.links, model_generator=self.model_generator,
                                   validation_percentage=self.validation_percentage)

    @staticmethod
    def is_a_training_arg(arg_name):
        """
        Checks if a given arg name is a training attribute
        :return: True if the arg is a training attribute, else False
        """
        return arg_name in vars(TraceArgs).keys()

    def build(self) -> TraceArgs:
        """
        Builds training arguments for some pretrained model.
        :return: Arguments for trace job including training and predicting trace links
        """

        return TraceArgs(source_layers=self.source_layers, target_layers=self.target_layers,
                         links=self.links, model_generator=self._build_model_generator(),
                         output_dir=self.output_dir, pretraining_data_path=self.pretraining_data_path,
                         kwargs=self.settings, trace_dataset_creator=None)
