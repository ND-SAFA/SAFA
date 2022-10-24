from typing import List, Optional, Tuple

from tracer.train.trace_args import TraceArgs

Examples = List[Tuple[str, int]]
OptionalExamples = Optional[Examples]


class GanArgs(TraceArgs):
    """
    The arguments to define a gan model.
    """

    def __init__(self, output_dir: str, num_hidden_layers_g: int = 1, num_hidden_layers_d: int = 1, noise_size: int = 100,
                 out_dropout_rate: float = 0.2, print_each_n_step: int = 1, learning_rate_discriminator: float = 5e-5,
                 learning_rate_generator: float = 5e-5, epsilon: float = 1e-8, num_train_epochs: int = 10, multi_gpu: bool = True,
                 apply_scheduler: bool = False, warmup_proportion: float = 0.1, **kwargs):
        """
        The arguments for creating a GAN-BERT and the dataset to train on.
        :param num_hidden_layers_g: number of hidden layers in the generator, each of the size of the output space.
        :param num_hidden_layers_d: number of hidden layers in the discriminator, each of the size of the input space
        :param noise_size: size of the generator's input noisy vectors.
        :param out_dropout_rate: dropout to be applied to discriminator's input vectors.
        :param print_each_n_step: After now many steps should log be printed.
        """
        super().__init__(output_dir, **kwargs)
        self.num_hidden_layers_g = num_hidden_layers_g
        self.num_hidden_layers_d = num_hidden_layers_d
        self.noise_size = noise_size
        self.out_dropout_rate = out_dropout_rate
        self.print_each_n_step = print_each_n_step
        self.learning_rate_discriminator = learning_rate_discriminator
        self.learning_rate_generator = learning_rate_generator
        self.epsilon = epsilon
        self.num_train_epochs = num_train_epochs
        self.multi_gpu = multi_gpu
        self.apply_scheduler = apply_scheduler
        self.warmup_proportion = warmup_proportion
