import torch
from transformers import AutoConfig, AutoModel, AutoTokenizer

from gan.descriminator import Discriminator
from gan.gan_args import GanArgs
from gan.gan_dataset import GanDataset
from gan.generator import Generator
from gan.gpu_support import get_device
from gan.optimizer_args import OptimizerArgs


class GanBuilder:
    def __init__(self, args: GanArgs, optimizer_args: OptimizerArgs):
        self.args = args
        self.optimizer_args = optimizer_args

    def build(self):
        device = get_device()
        transformer = AutoModel.from_pretrained(self.args.model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.args.model_name)
        dataset = GanDataset(self.args, tokenizer)

        config = AutoConfig.from_pretrained(self.args.model_name)
        hidden_size = int(config.hidden_size)
        # Define the number and width of hidden layers
        hidden_levels_g = [hidden_size for i in range(0, self.args.num_hidden_layers_g)]
        hidden_levels_d = [hidden_size for i in range(0, self.args.num_hidden_layers_d)]

        # -------------------------------------------------
        #   Instantiate the Generator and Discriminator
        # -------------------------------------------------
        generator = Generator(noise_size=self.args.noise_size, output_size=hidden_size, hidden_sizes=hidden_levels_g,
                              dropout_rate=self.args.out_dropout_rate)
        discriminator = Discriminator(input_size=hidden_size, hidden_sizes=hidden_levels_d,
                                      num_labels=len(dataset.label_list),
                                      dropout_rate=self.args.out_dropout_rate)

        # Put everything in the GPU if available
        if torch.cuda.is_available():
            generator.cuda()
            discriminator.cuda()
            transformer.cuda()
            if self.optimizer_args.multi_gpu:
                transformer = torch.nn.DataParallel(transformer)
        return generator, discriminator, transformer, tokenizer, device
