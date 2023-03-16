import os
import sys

import deepspeed
from deepspeed.runtime.zero.stage3 import estimate_zero3_model_states_mem_needs_all_live
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])
if __name__ == "__main__":
    from models.model_manager import ModelManager
    from models.model_properties import ModelTask

    models = ["bert-base-uncased", "bert-large-uncased"]
    for model in models:
        print("-" * 10, model, "-" * 10)
        with deepspeed.zero.Init():
            model_manager = ModelManager("bert-large-uncased", model_task=ModelTask.AUTO)
            model = model_manager.get_model()
            estimate_zero3_model_states_mem_needs_all_live(model, num_gpus_per_node=4, num_nodes=1)
