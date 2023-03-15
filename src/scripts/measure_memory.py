import os
import sys

from deepspeed.runtime.zero.stage3 import estimate_zero3_model_states_mem_needs_all_live
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])
if __name__ == "__main__":
    from models.llama.llama_model_manager import LLaMAModelManager

    model_manager = LLaMAModelManager("decapoda-research/llama-7b-hf")
    model = model_manager.get_model()
    estimate_zero3_model_states_mem_needs_all_live(model, num_gpus_per_node=4, num_nodes=1)
