import os
import sys

from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])

if __name__ == "__main__":
    from util.logging.logger_config import LoggerConfig
    from util.logging.logger_manager import LoggerManager, logger
    from models.llama.llama_model_manager import LLaMAModelManager
    from models.llama.llama_task import LLaMATask
    from datasets import disable_caching
    from models.model_manager import ModelManager
    from models.model_properties import ModelTask

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
    mode = "prod"
    output_path = os.path.expanduser("~/output/test_lm")
    dataset_output_path = os.path.join(output_path, "data")

    # Model Manager
    model_name = modes[mode]["model"]
    model_manager = modes[mode]["model_manager"](model_name, **modes[mode]["model_manager_args"])
    logger.info("Created model manager.")

    # Prepare dataset
    model = model_manager.get_model()

    # Generation
    prompt = "Hello, I am having a "
    tokenizer = model_manager.get_tokenizer()
    inputs = tokenizer(prompt, return_tensors="pt").input_ids
    model_output = model.generate(inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
    output = tokenizer.batch_decode(model_output, skip_special_tokens=True)
    print("Model Response:", output)
