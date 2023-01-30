import os
import sys

import dotenv
from accelerate import Accelerator
from transformers import AutoModelForSequenceClassification

dotenv.load_dotenv()
sys.path.append(os.environ["ROOT_PATH"])

if __name__ == "__main__":
    model_1 = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
    accelerate = Accelerator()
    model_1 = accelerate.prepare_model(model_1)
    model_2 = AutoModelForSequenceClassification.from_pretrained("roberta-base")
    accelerate.free_memory()
    accelerate.prepare_model(model_2)
    print("Done")
