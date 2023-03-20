import torch
from torch.optim import Optimizer
from transformers import PreTrainedModel

from util.enum_util import FunctionalWrapper
from util.supported_enum import SupportedEnum


class SupportedOptimizers(SupportedEnum):
    """
    Represents set of optimizers that can be selected from job configuration.
    """
    ADAMW_HF = FunctionalWrapper(torch.optim.Adam)

    @classmethod
    def create(cls, optimizer_name: str, model: PreTrainedModel, **kwargs) -> Optimizer:
        """
        Creates optimizer from training args and model parameters.
        :param optimizer_name: The name of the optimizer to construct
        :param model: The model whose parameters will be updated by optimizer.
        :return: Constructed optimizer.
        """
        optimizer_constructor = cls.get_value(optimizer_name)
        return optimizer_constructor(model.parameters(), **kwargs)
