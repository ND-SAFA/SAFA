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

    def start(self):
        model_1 = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
        accelerate = self.get_accelerate()
        model_1 = accelerate.prepare_model(model_1)
        model_2 = AutoModelForSequenceClassification.from_pretrained("roberta-base")
        accelerate.free_memory()
        accelerate.prepare_model(model_2)
        print("Done")

    def get_accelerate(self):
        if self.accelerate is None:
            self.accelerate = Accelerator()
        return self.accelerate


if __name__ == "__main__":
    thread = ThreadExample()
    thread.run()
