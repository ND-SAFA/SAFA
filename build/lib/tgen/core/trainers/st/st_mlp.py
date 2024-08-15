from typing import List, Type, Union

import torch.nn as nn
from sentence_transformers import SentenceTransformer

from common_resources.tools.util.override import overrides


class STMLP(nn.Module):
    def __init__(self, input_size: int, hidden_sizes: List[int], output_size=1,
                 activations: Union[Type[nn.Module], List[Type[nn.Module]]] = None):
        """
        Initializes an MLP with an layer of input size, a series of hidden layer, and an output layer.
        :param input_size: The size of the input layer.
        :param hidden_sizes: The sizes of each hidden layer.
        :param output_size: The size of the final output layer.
        :param activations:
        """
        super(STMLP, self).__init__()
        layers = []
        sizes = [input_size] + hidden_sizes + [output_size]
        for i in range(len(sizes) - 1):
            layers.append(nn.Linear(sizes[i], sizes[i + 1]))
            if activations is not None and i < len(activations):
                layers.append(activations[i]())
        layers.append(nn.Sigmoid())
        self.layers = nn.Sequential(*layers)
        self.device = next(self.parameters()).device

    @overrides(nn.Module)
    def forward(self, x):
        """
        Passed concatenated embeddings through MLP and calculates class 1 propabilities.
        :param x: The concatenated embeddings.
        :return: Class 1 probabilities.
        """
        output = self.layers(x)
        scores = output.squeeze()
        return scores

    @staticmethod
    def build(model: SentenceTransformer, hidden_sizes: List[int], activations: List[nn.Module]):
        """
        Builds MLP on top of concatenated embeddings of given model.
        :param model: The model producing the embeddings to classify.
        :param hidden_sizes: List of sizes of each hidden layer.
        :param activations:The action function to use. If single, then used for all layers.
        :return: The constructed MLP.
        """
        if not isinstance(activations, list):
            activations = [activations] * (len(hidden_sizes))
        input_size = 2 * model.get_sentence_embedding_dimension()
        mlp_model = STMLP(input_size=input_size, hidden_sizes=hidden_sizes, activations=activations)
        return mlp_model
