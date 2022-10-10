from typing import Dict, List, Tuple, Type

from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.models.base_models.supported_base_model import SupportedBaseModel
from common.models.model_generator import ModelGenerator
from trace.data.datasets.trace_dataset_creator import TraceDatasetCreator
from trace.jobs.trace_args import TraceArgs


class PretrainArgsBuilder(AbstractArgsBuilder):

    def __init__(self, model_path: str, output_dir: str, pretraining_data_path: str,
                 base_model: SupportedBaseModel = SupportedBaseModel.BERT_FOR_MASKED_LM, settings: dict = None):
        """
        Responsible for building training arguments for some pretrained model.
        :param base_model: supported base model name
        :param model_path: where the pretrained model will be loaded from
        :param output_dir: where the model will be saved to
        :param settings: additional parameters passed into ModelTraceArgs
        """
        super().__init__(base_model, model_path, output_dir, settings)
        self.base_model = base_model
        self.model_path = model_path
        self.output_dir = output_dir
        self.pretraining_data_path = pretraining_data_path
        self.settings = settings if settings else {}

    def _build_trace_dataset(self):
        return TraceDatasetCreator(source_layers=self.source_layers, target_layers=self.target_layers,
                                   true_links=self.links, model_generator=self.model_generator,
                                   validation_percentage=self.validation_percentage)

    def build(self) -> TraceArgs:
        """
        Builds training arguments for some pretrained model.
        :return: Arguments for trace job including training and predicting trace links
        """
        model_generator = self._build_model_generator()
        trace_dataset_creator = self._build_trace_dataset()
        return TraceArgs(model_generator=model_generator, output_dir=self.output_dir,
                         pretraining_data_path=self.pretraining_data_path, trace_dataset_creator=trace_dataset_creator,
                         **self.settings)
