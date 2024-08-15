import random
from typing import List

import torch
from torch import nn
from tqdm import tqdm

DEFAULT_HIDDEN_SIZE = [20, 100]


class SingleLayerModel(nn.Module):

    def __init__(self, input_size: int, output_size: int = 2, hidden_sizes: List[int] = None):
        """
        Creates a linear model with multiple hidden layers.
        :param input_size: The size of the input to the model.
        :param output_size: The size of the output of the model.
        :param hidden_sizes: The size of each of the hidden layers.
        """
        if hidden_sizes is None:
            hidden_sizes = DEFAULT_HIDDEN_SIZE
        super().__init__()
        hidden_sizes.append(output_size)
        self.starting_layers: List[nn.Module] = [nn.Linear(input_size, hidden_size1), nn.ReLU()]
        self.hidden_layers: List[nn.Module] = [nn.Linear(hidden_sizes[i], hidden_sizes[i + 1]) for i in range(len(hidden_sizes) - 1)]
        self.final_layers: List[nn.Module] = [nn.Softmax()]
        self.layers: List[nn.Module] = self.starting_layers + self.hidden_layers + self.final_layers

    def forward(self, x):
        """
        Performs the forward pass on the model with given inputs.
        :param x: The data in batch.
        :return: The output of the model.
        """
        curr = x
        for layer in self.layers:
            curr = layer(curr)
        return curr


def train(model: SingleLayerModel, training_data: List[List[float]], labels: List[float], n_epochs: int = 10) -> List[int]:
    """
    Simple training method for the the single layer model
    :param model: The model to train
    :param training_data: The data to train on
    :param labels: The ground truth labels
    :param n_epochs: Number of epochs to use for training
    :return: The cost at each epoch
    """
    data2shuffle = list(enumerate(training_data))
    random.shuffle(data2shuffle)
    indices, shuffled_data = zip(*data2shuffle)
    shuffled_data = torch.tensor(shuffled_data, dtype=torch.float32)
    shuffled_labels = torch.tensor([labels[i] for i in indices])
    # Define the training loop
    epochs = n_epochs
    loss = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())
    cost = []
    for epoch in tqdm(range(epochs), desc="Training..."):
        total = 0
        for input_, label in zip(shuffled_data, shuffled_labels):
            yhat = model(input_)
            output = loss(yhat, label)
            output.backward()
            optimizer.step()
            optimizer.zero_grad()
            # get total loss
            step_loss = output.item()
            total += step_loss
        cost.append(total)
    return cost


def predict(model: SingleLayerModel, prediction_data: List[List[float]]) -> List[float]:
    """
    Uses the model to predict
    :param model: The model to use
    :param prediction_data: The data to predict on
    :return: A list of predictions
    """
    prediction_data = torch.tensor(prediction_data, dtype=torch.float32)
    predictions = []
    for input_ in prediction_data:
        y_hat = model(input_)
        predictions.append(y_hat.detach().numpy().tolist()[1])
    return predictions
