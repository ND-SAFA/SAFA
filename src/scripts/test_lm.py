import os
import sys

from dotenv import load_dotenv
from transformers import AutoTokenizer, DataCollatorWithPadding, Trainer

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


if __name__ == "__main__":
    from train.trainer_args import TrainerArgs
    from constants import PROJ_PATH
    from data.creators.trace_dataset_creator import TraceDatasetCreator
    from data.readers.hub_project_reader import HubProjectReader
    from models.model_manager import ModelManager
    from util.logging.logger_config import LoggerConfig
    from util.logging.logger_manager import LoggerManager

    # import deepspeed
    #
    # deepspeed.ops.op_builder.CPUAdamBuilder().load()
    model_path = "gpt2-xl"
    # model_path = "hf-internal-testing/tiny-random-bert"
    dataset_name = "cm1"
    output_path = os.path.expanduser("~/output/test_lm")
    LoggerManager.configure_logger(LoggerConfig(output_dir=os.path.join(output_path, "logs")))

    # Model
    model_manager = ModelManager(model_path)

    # Dataset
    project_reader = HubProjectReader(dataset_name)
    trace_dataset_creator = TraceDatasetCreator(project_reader)
    trace_dataset = trace_dataset_creator.create()
    dataset = trace_dataset.to_hf_dataset(model_manager)

    # Construct objects
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = model_manager.get_model()
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    deepspeed_path = os.path.join(PROJ_PATH, "deepspeed.json")

    args = TrainerArgs(output_path)  # , deepspeed=deepspeed_path)
    args.remove_unused_columns = False
    args.__post_init__()

    # Prepare dataset
    add_padding_token(tokenizer, model.config)
    trainer = Trainer(model=model, args=args, data_collator=data_collator, train_dataset=dataset)

    # Predict
    outputs = trainer.train()
    response = outputs.predictions
    print("Predictions: \n", response)
