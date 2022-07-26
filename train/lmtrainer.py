from transformers.trainer_pt_utils import get_tpu_sampler, is_torch_tpu_available
from transformers.trainer import Trainer
from data.trace_dataset import TraceDataset
from jobs.job_args import LMArgs
from models.model_generator import BaseModelGenerator
from results.base_result import BaseResult
from torch.utils.data import DataLoader, RandomSampler
from torch.utils.data.distributed import DistributedSampler


class LMTrainer(Trainer):

    def __init__(self, args: LMArgs, model_generator: BaseModelGenerator, dataset: TraceDataset):
        model = model_generator.get_model()
        tokenizer = model_generator.get_tokenizer()
        self.args = args
        self.model_generator = model_generator
        self.model_generator.set_max_seq_length(self.args.max_seq_length)
        self.dataset = dataset
        super().__init__(model=model, args=args, tokenizer=tokenizer)

    # TODO
    def perform_training(self, checkpoint: str = None) -> BaseResult:
        output = self.train(resume_from_checkpoint=checkpoint)
        self.save_model()
        return BaseResult(output)

    # TODO
    def perform_prediction(self) -> BaseResult:
        self.eval_dataset = self.dataset.get_validation_data(self.args.dataset_size)
        output = self.predict(self.eval_dataset)
        return BaseResult(output)

    def get_train_dataloader(self):
        self.train_dataset = self.dataset.get_training_data(self.args.resample_rate)

        if is_torch_tpu_available():
            train_sampler = get_tpu_sampler(self.train_dataset, self.args.train_batch_size)
        else:
            train_sampler = (
                RandomSampler(self.train_dataset)
                if self.args.local_rank == -1
                else DistributedSampler(self.train_dataset)
            )

        data_loader = DataLoader(
            self.train_dataset,
            batch_size=self.args.train_batch_size,
            sampler=train_sampler,
            collate_fn=self.data_collator,
            drop_last=self.args.dataloader_drop_last,
        )
        return data_loader
