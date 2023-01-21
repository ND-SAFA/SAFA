from torch import nn


class Generator(nn.Module):
    """
    https://www.aclweb.org/anthology/2020.acl-main.191/
    https://github.com/crux82/ganbert
    """

    def __init__(self, noise_size=100, output_size=512, hidden_sizes=[512], dropout_rate=0.1):
        """
        Generator for GAN
        :param noise_size: the size of the noise/input layer
        :param output_size: the size of the trace_output layer
        :param hidden_sizes: list of sizes for all hidden layers
        :param dropout_rate: the rate at which to apply dropout
        """
        super(Generator, self).__init__()
        layers = []
        hidden_sizes = [noise_size] + hidden_sizes
        for i in range(len(hidden_sizes) - 1):
            layers.extend([nn.Linear(hidden_sizes[i], hidden_sizes[i + 1]), nn.LeakyReLU(0.2, inplace=True),
                           nn.Dropout(dropout_rate)])

        layers.append(nn.Linear(hidden_sizes[-1], output_size))
        self.layers = nn.Sequential(*layers)

    def forward(self, noise):
        """
        Performed on forward pass
        :param noise: the noise
        :return: the trace_output representation
        """
        output_rep = self.layers(noise)
        return output_rep
