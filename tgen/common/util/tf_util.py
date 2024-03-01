from typing import Dict, List

import torch
from torch import Tensor, nn


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
