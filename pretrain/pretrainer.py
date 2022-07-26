from jobs.job_args import PretrainArgs
from pretrain.electra.build_pretraining_dataset import write_examples
from pretrain.electra.run_pretraining import train_or_eval
import multiprocessing
import os
from transformers.models.electra.convert_tf_checkpoint_to_pytorch import convert_tf_checkpoint_to_pytorch


class Pretrainer:
    def __init__(self, config: PretrainArgs):
        self.config = config

    # TODO - improve
    def save_vocab(self):
        tokenizer = self.config.model_generator.get_tokenizer()
        tokenizer.save_pretrained(self.config.output_dir)
        return os.path.join(self.config.output_dir, "vocab.txt")

    def build_pretraining_data(self):
        if self.config.num_processes == 1:
            write_examples(0, self.config)
        else:
            jobs = []
            for i in range(self.config.num_processes):
                job = multiprocessing.Process(target=write_examples, args=(i, self.config))
                jobs.append(job)
                job.start()
            for job in jobs:
                job.join()

    def train(self):
        train_or_eval(self.config)
        self.tf_checkpoint_to_pytorch()

    def tf_checkpoint_to_pytorch(self):
        electra_config_file = os.path.join(self.config.model_dir, "config.json")
        pytorch_dump_path = os.path.join(self.config.model_dir, "pytorch_model.bin")
        convert_tf_checkpoint_to_pytorch(self.config.model_dir, electra_config_file, pytorch_dump_path, "discriminator")

    def eval(self):
        output = train_or_eval(self.config)
        return output
