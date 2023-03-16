import os
import sys

import deepspeed
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])
if __name__ == "__main__":
    from models.model_manager import ModelManager
    from models.model_properties import ModelTask

    with deepspeed.zero.Init():
        model_manager = ModelManager("bigscience/bloom", model_task=ModelTask.AUTO)
        model = model_manager.get_model()
        print("done!")
