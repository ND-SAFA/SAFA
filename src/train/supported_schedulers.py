from torch.optim import Optimizer
from torch.optim.lr_scheduler import LinearLR

from train.supported_enum import SupportedEnum
from util.enum_util import FunctionalWrapper


class SupportedSchedulers(SupportedEnum):
    """
    Container for set of definable schedulers from job config.
    """
    LINEAR = FunctionalWrapper(LinearLR)

    @classmethod
    def create(cls, scheduler_name: str, optimizer: Optimizer, **kwargs):
        """
        Constructs learning rate scheduler for optimizer.
        :param scheduler_name: The name of the scheduler to create.
        :param optimizer: The optimizer the scheduler will be adjusting.
        :return: Constructed scheduler.
        """
        scheduler_constructor = cls.get_value(scheduler_name)
        return scheduler_constructor(optimizer, **kwargs)
