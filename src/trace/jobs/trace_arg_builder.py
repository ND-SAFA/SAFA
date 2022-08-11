from typing import Dict, List, Tuple

from trace.config.constants import LINKED_TARGETS_ONLY_DEFAULT
from common.jobs.arg_builder import ArgBuilder
from common.models.model_generator import ModelGenerator
from trace.data.trace_dataset_creator import TraceDatasetCreator

from trace.jobs.trace_args import ModelTraceArgs


class TraceArgBuilder(ArgBuilder):

    def __init__(self, base_model_name: str, links: List[Tuple[str, str]], model_path: str, output_path: str,
                sources: Dict[str, str], targets: Dict[str, str], **kwargs):
        """
        Responsible for building training arguments for some pretrained model.
        :param base_model_name: supported base model name
        :param links: list of true links to fine-tune on
        :param model_path: where the pretrained model will be loaded from
        :param output_path: where the model will be saved to
        :param sources: mapping between source artifact ids and their tokens
        :param targets: mapping between target artifact ids and their tokens
        :param kwargs: additional parameters passed into ModelTraceArgs
        """
        self.base_model_name = base_model_name
        self.links = links
        self.model_path = model_path
        self.output_path = output_path
        self.sources = sources
        self.targets = targets
        self.kwargs = kwargs

    def build(self) -> ModelTraceArgs:
        """
        Builds training arguments for some pretrained model.
        :return: Arguments for trace job including training and predicting trace links
        """

        model_generator = ModelGenerator(self.base_model_name, self.model_path)
        trace_dataset_creator = TraceDatasetCreator(source_artifacts=self.sources, target_artifacts=self.targets,
                                                    true_links=self.links,
                                                    model_generator=model_generator,
                                                    linked_targets_only=LINKED_TARGETS_ONLY_DEFAULT)
        return ModelTraceArgs(model_generator=model_generator,
                              trace_dataset_creator=trace_dataset_creator,
                              output_path=self.output_path,
                              kwargs=self.kwargs)
