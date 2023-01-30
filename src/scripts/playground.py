import os
import sys
from threading import Thread

import dotenv
from accelerate import Accelerator
from transformers import AutoModelForSequenceClassification

dotenv.load_dotenv()
sys.path.append(os.environ["ROOT_PATH"])


class ThreadExample(Thread):
    accelerate = None

    def __init__(self, model_path: str):
        super().__init__()
        self.model_path = model_path

    def run(self):
        model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        accelerate = self.get_accelerate()
        accelerate.prepare_model(model)
        print(f"Prepared {self.model_path}")

    def get_accelerate(self):
        if self.accelerate is None:
            self.accelerate = Accelerator()
        return self.accelerate


if __name__ == "__main__":
    print("Starting...")
    bert_thread = ThreadExample("bert-base-uncased")
    roberta_thread = ThreadExample("roberta-base")

    bert_thread.start()
    bert_thread.join()
    roberta_thread.start()
    roberta_thread.join()
    print("Done")
