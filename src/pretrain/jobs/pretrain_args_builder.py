from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.models.base_models.supported_base_model import SupportedBaseModel
from common.models.model_generator import ModelGenerator
from common.models.model_properties import ModelSize
from pretrain.config.constants import PRETRAIN_MODEL_PATH
from pretrain.data.corpuses.domain import Domain
from pretrain.jobs.pretrain_args import PretrainArgs


class PretrainArgBuilder(AbstractArgsBuilder):

    def __init__(self, output_path: str, corpus_dir: str = None, domain: Domain = Domain.BASE,
                 model_size: ModelSize = ModelSize.BASE, **kwargs):
        """
        Responsible for building Pretraining arguments for pretraining a model.
        :param output_path: path to model checkpoint
        :param corpus_dir: path to directory containing pretraining files
        :param domain: domain this model is training for
        :param model_size: size of model being pretrained
        :param kwargs: additional parameters passed to PretrainArguments
        """
        self.output_path = output_path
        self.corpus_dir = corpus_dir
        self.domain = domain
        self.model_size = model_size
        self.kwargs = kwargs

    def build(self) -> PretrainArgs:
        """
        Creates Pretraining arguments for pretraining a model.
        :return: Arguments for pretraining a model
        """
        model_generator = ModelGenerator(SupportedBaseModel.ELECTRA_TRACE_SINGLE,
                                         PRETRAIN_MODEL_PATH.format(self.model_size.value),
                                         model_size=self.model_size)
        return PretrainArgs(
            model_generator=model_generator,
            output_path=self.output_path,
            corpus_dir=self.corpus_dir,
            domain=self.domain,
            kwargs=self.kwargs
        )
