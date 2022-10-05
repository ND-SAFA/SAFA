class GanArgs:
    """
    The arguments to define a gan model.
    """

    def __init__(self, labeled_file_path: str, unlabeled_file_path: str = None,
                 model_name="bert-base-uncased", test_size=0.1, max_seq_length=64, batch_size=64,
                 num_hidden_layers_g=1,
                 num_hidden_layers_d=1, noise_size=100,
                 out_dropout_rate=0.2, apply_balance=True, print_each_n_step=1):
        """
        The arguments for creating a GAN-BERT and the dataset to train on.
        :param max_seq_length: TODO
        :param batch_size: number of examples per batch.
        :param num_hidden_layers_g: number of hidden layers in the generator, each of the size of the output space.
        :param num_hidden_layers_d: number of hidden layers in the discriminator, each of the size of the input space
        :param noise_size: size of the generator's input noisy vectors.
        :param out_dropout_rate: dropout to be applied to discriminator's input vectors.
        :param apply_balance: Replicate labeled data to balance poorly represented datasets.
        :param print_each_n_step: After now many steps should log be printed.
        """
        self.labeled_file_path = labeled_file_path
        self.unlabeled_file_path = unlabeled_file_path
        self.model_name = model_name
        self.test_size = test_size
        self.max_seq_length = max_seq_length
        self.batch_size = batch_size
        self.num_hidden_layers_g = num_hidden_layers_g
        self.num_hidden_layers_d = num_hidden_layers_d
        self.noise_size = noise_size
        self.out_dropout_rate = out_dropout_rate
        self.apply_balance = apply_balance
        self.print_each_n_step = print_each_n_step
