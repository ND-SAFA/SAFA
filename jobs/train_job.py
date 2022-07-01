from jobs.base_job import BaseJob
from transformers import default_data_collator, DataCollatorWithPadding

from trainer.lmtrainer import LMTrainer


class TrainJob(BaseJob):

    def _get_checkpoint(self) -> str:
        pass

    def _start(self):
        checkpoint = self._get_checkpoint()
        trainer = self._get_trainer()
        results = trainer.train(checkpoint=checkpoint)
        results.save()

    def __get_data_collator(self):
        data_collator = (
            default_data_collator
            if self.args.pad_to_max_length
            else DataCollatorWithPadding(
                self.args.model_generator.get_tokenizer(), pad_to_multiple_of=8 if self.args.fp16 else None
            )
        )
        return data_collator
    

