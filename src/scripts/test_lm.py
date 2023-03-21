import os
import sys

from datasets import load_dataset
from dotenv import load_dotenv
from transformers import DataCollatorWithPadding, Trainer

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])


def add_padding_token(tokenizer, config):
    config.pad_token_id = -1 if config.pad_token_id is None else config.pad_token_id
    vocab = tokenizer.get_vocab()
    vocab_tokens, vocab_indices = list(vocab.keys()), list(vocab.values())
    tokenizer.add_special_tokens({'pad_token': vocab_tokens[config.pad_token_id]})


def create_trace_dataset(dataset_name="cm1", create=True):
    # Export Dataset Split
    if create:
        project_reader = HubProjectReader(dataset_name)
        trace_dataset_creator = TraceDatasetCreator(project_reader)
        split_dataset_creator = SplitDatasetCreator(val_percentage=0.80)
        trace_dataset_manager = TrainerDatasetManager(train_dataset_creator=trace_dataset_creator,
                                                      val_dataset_creator=split_dataset_creator)
        trace_dataset_manager.export_dataset_splits(dataset_output_path)
        dataset_name = trace_dataset_manager.get_dataset_filename(DatasetRole.TRAIN)
        del trace_dataset_manager
    dataset_name = "cm1_train.csv"
    dataset_path = os.path.join(dataset_output_path, dataset_name)
    # del trace_dataset_manager

    # Load split as CSV
    project_reader = CsvProjectReader(dataset_path)
    trace_dataset_creator = TraceDatasetCreator(project_reader)
    trace_dataset = trace_dataset_creator.create()
    dataset = trace_dataset.to_hf_dataset(model_manager)
    return dataset


def create_test_dataset(**kwargs):
    full_dataset = load_dataset("rotten_tomatoes")

    def preprocess_function(examples):
        return tokenizer(examples["text"], truncation=True)

    return full_dataset["train"].map(preprocess_function, batched=True)


modes = {
    "test": {
        "model": "hf-internal-testing/tiny-random-bert",
        "dataset": create_test_dataset,
        "params": ["per_device_train_batch_size"]
    },
    "prod": {
        "model": "gpt2-xl",
        "dataset": create_trace_dataset,
        "params": ["deepspeed", "per_device_train_batch_size", "remove_unused_columns"]
    }
}

if __name__ == "__main__":
    from train.trainer_args import TrainerArgs
    from constants import PROJ_PATH
    from data.creators.trace_dataset_creator import TraceDatasetCreator
    from models.model_manager import ModelManager
    from util.logging.logger_config import LoggerConfig
    from util.logging.logger_manager import LoggerManager
    from data.readers.csv_project_reader import CsvProjectReader
    from data.creators.split_dataset_creator import SplitDatasetCreator
    from data.datasets.dataset_role import DatasetRole
    from data.managers.trainer_dataset_manager import TrainerDatasetManager
    from data.readers.hub_project_reader import HubProjectReader
    import gc

    mode = "prod"
    # Paths
    output_path = os.path.expanduser("~/output/test_lm")
    dataset_output_path = os.path.join(output_path, "data")
    LoggerManager.configure_logger(LoggerConfig(output_dir=os.path.join(output_path, "logs")))

    # Construct objects
    model_manager = ModelManager(modes[mode]["model"])
    tokenizer = model_manager.get_tokenizer()
    dataset = modes[mode]["dataset"](create=True)
    model = model_manager.get_model()
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer, padding="max_length", max_length=256)
    deepspeed_path = os.path.join(PROJ_PATH, "deepspeed.json")
    arg_params = {"deepspeed": deepspeed_path, "per_device_train_batch_size": 1, "remove_unused_columns": False}
    arg_params = {k: v for k, v in arg_params.items() if k in modes[mode]["params"]}
    args = TrainerArgs(output_path, **arg_params)
    args.__post_init__()

    # Prepare dataset
    add_padding_token(tokenizer, model.config)
    trainer = Trainer(model=model, args=args, data_collator=data_collator, train_dataset=dataset)

    # Predict
    gc.collect()
    outputs = trainer.train()
    response = outputs.predictions
    print("Predictions: \n", response)
