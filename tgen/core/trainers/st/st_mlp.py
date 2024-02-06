from typing import List, Type, Union

import torch.nn as nn
from sentence_transformers import SentenceTransformer


class MLP(nn.Module):
    def __init__(self, input_size: int, hidden_sizes: List[int], output_size=1,
                 activations: Union[Type[nn.Module], List[Type[nn.Module]]] = None):
        """
        Initializes an MLP with an layer of input size, a series of hidden layer, and an output layer.
        :param input_size: The size of the input layer.
        :param hidden_sizes: The sizes of each hidden layer.
        :param output_size: The size of the final output layer.
        :param activations:
        """
        super(MLP, self).__init__()
        layers = []
        sizes = [input_size] + hidden_sizes + [output_size]
        for i in range(len(sizes) - 1):
            layers.append(nn.Linear(sizes[i], sizes[i + 1]))
            if activations is not None and i < len(activations):
                layers.append(activations[i]())
        self.layers = nn.Sequential(*layers)

    @staticmethod
    def build(model: SentenceTransformer, hidden_sizes: List[int], activations: List[nn.Module]):
        if not isinstance(activations, list):
            activations = [activations] * (len(hidden_sizes) + 1)
        input_size = 2 * model.get_sentence_embedding_dimension()
        mlp_model = MLP(input_size=input_size, hidden_sizes=hidden_sizes, activations=activations)
        return mlp_model

    def forward(self, x):
        return self.layers(x)
