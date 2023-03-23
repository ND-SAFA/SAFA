import os
import sys

import deepspeed
import torch
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])

if __name__ == "__main__":
    from constants import PROJ_PATH
    from util.logging.logger_config import LoggerConfig
    from util.logging.logger_manager import LoggerManager, logger
    from models.llama.llama_model_manager import LLaMAModelManager
    from models.llama.llama_task import LLaMATask
    from datasets import set_caching_enabled
    from models.model_manager import ModelManager
    from models.model_properties import ModelTask
    from util.json_util import JsonUtil

    modes = {
        "test": {
            "model": "hf-internal-testing/tiny-random-bert",
            "model_manager": ModelManager,
            "model_manager_args": {
                "model_task": ModelTask.CAUSAL_LM
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
                                         mp_size=4,
                                         dtype=torch.half,
                                         replace_with_kernel_inject=True)
    model = ds_engine.module

    # Generation
    prompt = "Hello, I am having a "
    inputs = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
    model_response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print(f"llama > {model_response}")
