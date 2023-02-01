from copy import deepcopy
from typing import Any

from accelerate import Accelerator
from accelerate.utils import LoggerType

from util.reflection_util import ReflectionUtil


class AcceleratorSingleton:
    """
    Singleton of the Accelerator
    """

    INIT_DEFAULTS = {"split_batches": True, "step_scheduler_with_optimizer": False, "log_with": [LoggerType.TENSORBOARD]}
    __accelerator: Accelerator = None

    @staticmethod
    def get() -> Accelerator:
        """
        Gets the instance of the __accelerator
        :return: The current __accelerator instance
        """
        if not AcceleratorSingleton.exists():
            AcceleratorSingleton.__initialize()
        return AcceleratorSingleton.__accelerator

    @staticmethod
    def update(**kwargs) -> Accelerator:
        """
        Updates the internal instance of the __accelerator
        :param kwargs:
        :return:
        """
        if AcceleratorSingleton.exists():
            AcceleratorSingleton.clear()
            AcceleratorSingleton.__update_attrs(**kwargs)
        else:
            AcceleratorSingleton.__initialize(**kwargs)
        return AcceleratorSingleton.get()

    @staticmethod
    def exists() -> bool:
        """
        Returns True if the internal __accelerator exists, else False
        :return: True if the internal __accelerator exists, else False
        """
        return AcceleratorSingleton.__accelerator is not None

    @staticmethod
    def clear():
        if AcceleratorSingleton.exists():
            AcceleratorSingleton.__accelerator.clear()

    @staticmethod
    def __update_attrs(**attrs) -> None:
        """
        Updates the attributes of the accelerator
        :param attrs: A dictionary containing the attributes to set
        :return: None
        """
        AcceleratorSingleton.__accelerator = ReflectionUtil.set_attributes(AcceleratorSingleton.get(), attrs)

    @staticmethod
    def __initialize(**kwargs) -> None:
        """
        Initializes the accelerator
        :param kwargs: any additional arguments to pass to the accelerator
        :return:
        """
        params = deepcopy(AcceleratorSingleton.INIT_DEFAULTS)
        params.update(kwargs)
        AcceleratorSingleton.__accelerator = Accelerator(**params)

    @classmethod
    def __getattr__(cls, attr: str) -> Any:
        """
        Gets attribute from self if exists, otherwise will get from the accelerator
        :param attr: The attribute to get
        :return: The attribute value
        """
        if hasattr(cls, attr):
            return super().__getattribute__(cls, attr)
        return getattr(AcceleratorSingleton.get(), attr)

    def __bool__(self) -> bool:
        """
        Returns True if the internal __accelerator exists, else False
        :return: True if the internal __accelerator exists, else False
        """
        return self.exists()


TraceAccelerator = AcceleratorSingleton()
