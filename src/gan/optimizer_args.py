class OptimizerArgs:
    """
    Optimization parameters (e.g. Adam)
    """

    def __init__(self, learning_rate_discriminator=5e-5, learning_rate_generator=5e-5, epsilon=1e-8,
                 num_train_epochs=10, multi_gpu=True):
        self.learning_rate_discriminator = learning_rate_discriminator
        self.learning_rate_generator = learning_rate_generator
        self.epsilon = epsilon
        self.num_train_epochs = num_train_epochs
        self.multi_gpu = multi_gpu
