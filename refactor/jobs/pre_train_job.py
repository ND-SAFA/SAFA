import os
import uuid
from typing import List

from transformers import DataCollatorForLanguageModeling, LineByLineTextDataset

from jobs.abstract_trainer_job import AbstractTrainerJob
from jobs.trace_args import TraceArgs
from jobs.trace_args_builder import JobArgsBuilder
from pre_processing.pre_processing_options import PreProcessingOptions
from pre_processing.pre_processor import PreProcessor
from storage.safa_storage import SafaStorage


class MLMPreTrainJob(AbstractTrainerJob):
    TRAINING_DIR = SafaStorage.add_mount_directory("jobs/pretrain/mlm")
    BLOCK_SIZE = 128
    MLM_PROBABILITY = 0.15

    def __init__(self, args_builder: JobArgsBuilder):
        super().__init__(args_builder)

    def _run(self):
        args: TraceArgs = self.args
        tokenizer = args.model_generator.get_tokenizer()

        # Step - Create training file
        training_file_path = self.create_training_data(args.pretraining_data_path)

        dataset = LineByLineTextDataset(
            tokenizer=tokenizer,
            file_path=training_file_path,
            block_size=self.BLOCK_SIZE,
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, mlm=True, mlm_probability=self.MLM_PROBABILITY
        )

        trainer = self.get_trainer(data_collator=data_collator, train_dataset=dataset)
        result = trainer.train()

        trainer.save_model(args.output_dir)

        os.remove(training_file_path)
        return result

    def create_training_data(self, data_path: str) -> str:
        """
        Reads text files in given data_path and returns a temporary file containing collection.
        :param data_path: Path to txt file or folder containing txt files.
        :return: Path to temporary file containing formatted training examples.
        """
        training_examples = []
        if os.path.isfile(data_path):
            training_examples.extend(self._read_file_examples(data_path))
        elif os.path.isdir(data_path):
            for file_name in os.listdir(data_path):
                if file_name[0] == ".":
                    continue
                file_path = os.path.join(data_path, file_name)
                training_examples.extend(self._read_file_examples(file_path))
        else:
            raise Exception("Unable to read dataset path:" + data_path)
        return self._write_training_examples(training_examples)

    @staticmethod
    def _read_file_examples(file_path: str) -> List[str]:
        file_content = MLMPreTrainJob._read_file(file_path)
        pre_processing_options = {
            PreProcessingOptions.FILTER_MIN_LENGTH: True,
        }
        pre_processor = PreProcessor(pre_processing_options)
        return pre_processor.run(file_content.split("\n"))

    @staticmethod
    def _read_file(data_path: str):
        with open(data_path) as data_file:
            return data_file.read()

    @staticmethod
    def _write_training_examples(examples: List[str], delimiter: str = "\n", extension: str = ".txt") -> str:
        training_file_content = delimiter.join(examples)
        training_file_name = str(uuid.uuid4()) + extension
        training_file_path = os.path.join(MLMPreTrainJob.TRAINING_DIR, training_file_name)
        os.makedirs(os.path.dirname(training_file_path), exist_ok=True)
        print("Exporting:", training_file_path)
        with open(training_file_path, "w") as training_file:
            training_file.write(training_file_content)
        return training_file_path
