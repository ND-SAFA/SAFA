import os
import sys

from datasets import load_dataset
from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer, DataCollatorWithPadding, Trainer

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])


def add_padding_token(tokenizer, config):
    config.pad_token_id = -1 if config.pad_token_id is None else config.pad_token_id
    vocab = tokenizer.get_vocab()
    vocab_tokens, vocab_indices = list(vocab.keys()), list(vocab.values())
    tokenizer.add_special_tokens({'pad_token': vocab_tokens[config.pad_token_id]})


if __name__ == "__main__":
    from train.trainer_args import TrainerArgs
    from constants import PROJ_PATH

    model_path = "gpt2-xl"
    # model_path = "hf-internal-testing/tiny-random-bert"
    # Construct objects
    dataset = load_dataset("rotten_tomatoes")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    deepspeed_path = os.path.join(PROJ_PATH, "deepspeed.json")
    args = TrainerArgs("~/output/test_lm", deepspeed=deepspeed_path)

    # Prepare dataset
    add_padding_token(tokenizer, model.config)


    def preprocess_function(examples):
        return tokenizer(examples["text"], truncation=True)


    tokenized_dataset = dataset["train"].map(preprocess_function, batched=True)
    trainer = Trainer(model=model, args=args, data_collator=data_collator, train_dataset=tokenized_dataset)

    # Predict
    outputs = trainer.train()
    response = outputs.predictions
    print("Predictions: \n", response)
