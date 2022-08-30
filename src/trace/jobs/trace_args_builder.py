from typing import Dict, List, Tuple

from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.models.model_generator import ModelGenerator
from trace.data.trace_dataset_creator import TraceDatasetCreator
from trace.jobs.trace_args import TraceArgs


class TraceArgsBuilder(AbstractArgsBuilder):

    def __init__(self, base_model_name: str, model_path: str, output_dir: str, sources: Dict[str, str],
                 targets: Dict[str, str], links: List[Tuple[str, str]], validation_percentage: float, **kwargs):
        """
        Responsible for building training arguments for some pretrained model.
        :param base_model_name: supported base model name
        :param model_path: where the pretrained model will be loaded from
        :param output_dir: where the model will be saved to
        :param sources: mapping between source artifact ids and their tokens
        :param targets: mapping between target artifact ids and their tokens
        :param links: list of true links to fine-tune on
        :param kwargs: additional parameters passed into ModelTraceArgs
        """
        self.base_model_name = base_model_name
        self.links = links
        self.model_path = model_path
        self.output_dir = output_dir
        self.sources = sources
        self.targets = targets
        self.validation_percentage = validation_percentage
        self.kwargs = kwargs

    def build(self) -> TraceArgs:
        """
        Builds training arguments for some pretrained model.
        :return: Arguments for trace job including training and predicting trace links
        """

        model_generator = ModelGenerator(self.base_model_name, self.model_path)
        trace_dataset_creator = TraceDatasetCreator(source_artifacts=self.sources, target_artifacts=self.targets,
                                                    true_links=self.links,
                                                    model_generator=model_generator,
                                                    validation_percentage=self.validation_percentage)
        return TraceArgs(model_generator=model_generator,
                         trace_dataset_creator=trace_dataset_creator,
                         output_dir=self.output_dir,
                         kwargs=self.kwargs)
