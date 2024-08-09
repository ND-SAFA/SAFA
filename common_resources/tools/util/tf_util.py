from typing import Dict, Iterable, List, Type

import torch
from torch import Tensor
from torch.nn.parameter import Parameter

from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.reflection_util import ReflectionUtil
from common_resources.tools.util.supported_enum import SupportedEnum


class TFUtil:

    @staticmethod
    def move_features_to_device(device: torch.device, features: List[Dict[str, Tensor]]) -> None:
        """
        Moves features to device.
        :param device: The device to place features on.
        :param features: The features to move.
        :return: None
        """
        if not isinstance(features, list):
            features = [features]

        for feature in features:
            for k, v in feature.items():
                feature[k] = TFUtil.move_tensor_to_device(v, device)

    @staticmethod
    def move_tensor_to_device(tensor: Tensor, model_device: torch.device):
        """
        Moves the tensor to device, if not already there.
        :param tensor: The tensor to move.
        :param model_device: The device to move tensor to.
        :return: Tensor on the device specified.
        """
        if tensor.device != model_device:
            tensor = tensor.to(model_device)
        return tensor

    @staticmethod
    def set_gradients(parameters: Iterable[Parameter], requires_grad: bool) -> None:
        """
        Freezes the parameters of the models.
        :param parameters: The parameters to train.
        :param requires_grad: Whether the parameter should require gradients.
        :return:None
        """
        n_params = 0
        for param in parameters:
            param.requires_grad = requires_grad
            n_params += 1
        logger.info(f"{n_params} parameters was set to requires_grad={requires_grad}")

    @staticmethod
    def create_loss_function(loss_function_enum: Type[SupportedEnum], loss_function_name: str, default: str,
                             possible_params: Dict = None,
                             *args, **kwargs):
        """
        Creates loss function.
        :param loss_function_enum: Enum mapping name to loss function class.
        :param loss_function_name: The name of the loss function to create.
        :param default: The default loss function to use if name is None.
        :param possible_params: Map of param to values to construct loss function with.
        :param kwargs: Additional constructor parameters to loss function.
        :return:
        """
        if possible_params is None:
            possible_params = {}
        if default and loss_function_name is None:
            loss_function_name = default

        loss_function_class = loss_function_enum.get_value(loss_function_name)
        loss_function_kwargs = {param: param_value for param, param_value in possible_params.items()
                                if ReflectionUtil.has_constructor_param(loss_function_class, param)}

        loss_function = loss_function_class(*args, **kwargs, **loss_function_kwargs)
        logger.info(f"Created loss function {loss_function_name}.")
        return loss_function
