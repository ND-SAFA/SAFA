from typing import Dict, List, Type

import torch
from torch import Tensor, nn

from tgen.common.logging.logger_manager import logger
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.common.util.supported_enum import SupportedEnum


def move_input_to_device(device: str, features: List[Dict[str, Tensor]], labels: Tensor):
    """
    Moves the features and labels to device.
    :param device: The device to place features in.
    :param features: The features to give to model.
    :param labels: The associated labels of the features.
    :return: Features and labels on the device.
    """
    for feature in features:
        for k, v in feature.items():
            feature[k] = move_tensor_to_device(v, device)
    labels = move_tensor_to_device(labels, device)
    return features, labels


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


def freeze(*models: nn.Module) -> None:
    """
    Freezes the parameters of the models.
    :param models: The models to freeze.
    :return:None
    """
    for model in models:
        for param in model.parameters():
            param.requires_grad = False


def create_loss_function(loss_function_enum: Type[SupportedEnum], loss_function_name: str, possible_params: Dict = None, *args,
                         **kwargs):
    """
    Creates loss function.
    :param loss_function_enum: Enum mapping name to loss function class.
    :param loss_function_name: The name of the loss function to create.
    :param possible_params: Map of param to values to construct loss function with.
    :param kwargs: Additional constructor parameters to loss function.
    :return:
    """
    if possible_params is None:
        possible_params = {}

    loss_function_class = loss_function_enum.get_value(loss_function_name)
    loss_function_kwargs = {param: param_value for param, param_value in possible_params.items()
                            if ReflectionUtil.has_constructor_param(loss_function_class, param)}

    loss_function = loss_function_class(*args, **kwargs, **loss_function_kwargs)
    logger.info(f"Created loss function {loss_function_name}.")
    return loss_function
