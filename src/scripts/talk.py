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
    from datasets import disable_caching
    from models.model_manager import ModelManager
    from models.model_properties import ModelTask
    from util.json_util import JsonUtil

    modes = {
        "test": {
            "model": "microsoft/DialoGPT-small",
            "model_manager": ModelManager,
            "model_manager_args": {
                "model_task": ModelTask.CAUSAL_LM
            }
        },
        "prod": {
            "model": "decapoda-research/llama-7b-hf",
            "model_manager": LLaMAModelManager,
            "model_manager_args": {
                "model_task": LLaMATask.CASUAL_LM,
                "layers_to_freeze": 31
            }
        }
    }
    output_path = os.path.expanduser("~/desktop/safa/output")

    # Setup
    disable_caching()
    LoggerManager.configure_logger(LoggerConfig(output_dir=os.path.join(output_path, "logs")))

    # Paths
    mode = "test"
    output_path = os.path.expanduser("~/output/test_lm")
    dataset_output_path = os.path.join(output_path, "data")

    # Model Manager
    model_name = modes[mode]["model"]
    model_manager = modes[mode]["model_manager"](model_name, **modes[mode]["model_manager_args"])
    logger.info("Created model manager.")

    # Prepare dataset
    model = model_manager.get_model()
    deepspeed_config = JsonUtil.read_json_file(os.path.join(PROJ_PATH, "deepspeed.json"))
    ds_engine = deepspeed.init_inference(model,
                                         mp_size=4,
                                         dtype=torch.half,
                                         replace_with_kernel_inject=True)
    model = ds_engine.module

    # Generation
    prompt = "Hello, I am having a "
    tokenizer = model_manager.get_tokenizer()
    inputs = tokenizer(prompt)
    model_output = model.generate(inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
    print(model_output)
