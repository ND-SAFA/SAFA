import os
import sys

import deepspeed
import torch
from datasets import load_dataset
from dotenv import load_dotenv

from models.model_manager import ModelManager
from models.model_properties import ModelTask
from util.json_util import JsonUtil

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


def create_dataset_manager(dataset_name="cm1"):
    project_reader = HubProjectReader(dataset_name)
    trace_dataset_creator = TraceDatasetCreator(project_reader)
    split_dataset_creator = SplitDatasetCreator(val_percentage=0.8)
    trace_dataset_manager = TrainerDatasetManager(train_dataset_creator=trace_dataset_creator,
                                                  val_dataset_creator=split_dataset_creator)
    return trace_dataset_manager


def create_trace_dataset(dataset_name="cm1", create=True):
    # Export Dataset Split
    if create:
        trace_dataset_manager = create_dataset_manager(dataset_name)
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


if __name__ == "__main__":
    from constants import PROJ_PATH
    from data.creators.trace_dataset_creator import TraceDatasetCreator
    from util.logging.logger_config import LoggerConfig
    from util.logging.logger_manager import LoggerManager, logger
    from data.readers.csv_project_reader import CsvProjectReader
    from data.datasets.dataset_role import DatasetRole
    from data.managers.trainer_dataset_manager import TrainerDatasetManager
    from data.readers.hub_project_reader import HubProjectReader
    from models.llama.llama_model_manager import LLaMAModelManager
    from models.llama.llama_task import LLaMATask
    from data.creators.split_dataset_creator import SplitDatasetCreator
    from datasets import set_caching_enabled

    modes = {
        "test": {
            "model": "hf-internal-testing/tiny-random-bert",
            "model_manager": ModelManager,
            "model_manager_args": {
                "model_task": ModelTask.CASUAL_LM
            },
            "params": ["per_device_train_batch_size"]
        },
        "prod": {
            "model": "decapoda-research/llama-7b-hf",
            "model_manager": LLaMAModelManager,
            "model_manager_args": {
                "model_task": LLaMATask.CASUAL_LM,
                "layers_to_freeze": 31
            },
            "params": ["deepspeed", "per_device_train_batch_size", "remove_unused_columns", "gradient_accumulation_steps"]
        }
    }
    set_caching_enabled(False)

    mode = "test"
    # Paths
    output_path = os.path.expanduser("~/output/test_lm")
    dataset_output_path = os.path.join(output_path, "data")
    LoggerManager.configure_logger(LoggerConfig(output_dir=os.path.join(output_path, "logs")))

    # Model Manager
    logger.info("Creating model manager...")
    model_name = modes[mode]["model"]
    model_manager = modes[mode]["model_manager"](model_name, **modes[mode]["model_manager_args"])
    tokenizer = model_manager.get_tokenizer()
    logger.info("Done.")

    # Prepare dataset
    logger.info("Creating trainer...")
    model = model_manager.get_model()
    deepspeed_config = JsonUtil.read_json_file(os.path.join(PROJ_PATH, "deepspeed.json"))
    ds_engine = deepspeed.init_inference(model,
                                         mp_size=2,
                                         dtype=torch.half,
                                         replace_with_kernel_inject=True)
    model = ds_engine.module

    # Generation
    prompt = "Hello, I am having a "
    inputs = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
    model_response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print(f"llama > {model_response}")
