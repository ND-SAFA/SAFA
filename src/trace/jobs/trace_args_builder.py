from typing import Dict, List, Tuple

from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.models.base_models.supported_base_model import SupportedBaseModel
from common.models.model_generator import ModelGenerator
from trace.jobs.trace_args import TraceArgs


class TraceArgsBuilder(AbstractArgsBuilder):

    def __init__(self, base_model: SupportedBaseModel, model_path: str, output_dir: str,
                 source_layers: List[Dict[str, str]] = None,
                 target_layers: List[Dict[str, str]] = None, links: List[Tuple[str, str]] = None,
                 settings: dict = None):
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
        self.settings = settings if settings else {}

    @staticmethod
    def is_a_training_arg(arg_name):
        return arg_name in vars(TraceArgs).keys()

    def build(self) -> TraceArgs:
        """
        Builds training arguments for some pretrained model.
        :return: Arguments for trace job including training and predicting trace links
        """

        model_generator = ModelGenerator(self.base_model, self.model_path)
        return TraceArgs(source_layers=self.source_layers, target_layers=self.target_layers,
                         links=self.links, model_generator=model_generator,
                         output_dir=self.output_dir,
                         kwargs=self.settings)
