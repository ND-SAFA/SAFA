import os
import sys

from datasets import load_dataset
from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer

from train.trainer_args import TrainerArgs

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])

if __name__ == "__main__":
    model_path = "gpt2-xl"

    dataset = load_dataset("rotten_tomatoes")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    args = TrainerArgs("~/output/test_lm")

    trainer = Trainer(model=model, args=args, data_collator=data_collator)

    outputs = trainer.predict(dataset)
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print("Response: \n", response)
