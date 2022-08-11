from typing import Dict, List, Tuple

from config.constants import LINKED_TARGETS_ONLY_DEFAULT, PRETRAIN_MODEL_PATH
from data.trace_dataset_creator import TraceDatasetCreator
from jobs.pretrain.pretrain_args import ModelPretrainArgs
from jobs.trace.trace_args import ModelTraceArgs
from models.base_models.supported_base_model import SupportedBaseModel
from models.model_generator import ModelGenerator
from models.model_properties import ModelSize
from pretrain.corpuses.domain import Domain


def build_trace_args(base_model_name: str, links: List[Tuple[str, str]], model_path: str, output_path: str,
                     sources: Dict[str, str], targets: Dict[str, str], **kwargs) -> ModelTraceArgs:
    """
    Creates training arguments for some pretrained model.
    :param base_model_name: supported base model name
    :param links: list of true links to fine-tune on
    :param model_path: where the pretrained model will be loaded from
    :param output_path: where the model will be saved to
    :param sources: mapping between source artifact ids and their tokens
    :param targets: mapping between target artifact ids and their tokens
    :param kwargs: additional parameters passed into ModelTraceArgs
    :return: Arguments for trace job including training and predicting trace links
    """
    model_generator = ModelGenerator(base_model_name, model_path)
    trace_dataset_creator = TraceDatasetCreator(source_artifacts=sources, target_artifacts=targets, true_links=links,
                                                model_generator=model_generator,
                                                linked_targets_only=LINKED_TARGETS_ONLY_DEFAULT)
    return ModelTraceArgs(model_generator=model_generator,
                          trace_dataset_creator=trace_dataset_creator,
                          output_path=output_path,
                          kwargs=kwargs)


def build_pretrain_args(output_path: str,
                        corpus_dir: str = None,
                        domain: Domain = Domain.BASE,
                        model_size: ModelSize = ModelSize.BASE,
                        **kwargs) -> ModelPretrainArgs:
    """
    Creates Pretraining arguments for pretraining a model.
    :param output_path: path to model checkpoint
    :param corpus_dir: path to directory containing pretraining files
    :param domain: domain this model is training for
    :param model_size: size of model being pretrained
    :param kwargs: additional parameters passed to PretrainArguments
    :return: Arguments for pretraining a model
    """
    model_generator = ModelGenerator(SupportedBaseModel.ELECTRA_TRACE_SINGLE.name,
                                     PRETRAIN_MODEL_PATH.format(model_size.value),
                                     model_size=model_size)
    return ModelPretrainArgs(
        model_generator=model_generator,
        output_path=output_path,
        corpus_dir=corpus_dir,
        domain=domain,
        kwargs=kwargs
    )
