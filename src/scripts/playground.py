import os.path

import torch
from transformers import AutoModelForSequenceClassification

if __name__ == "__main__":
    print(torch.__version__)
    experiment = "best_model"
    path = f"~/projects/safa/tgen/test/output/{experiment}"
    path = os.path.expanduser(path)
    model = AutoModelForSequenceClassification.from_pretrained(path)
