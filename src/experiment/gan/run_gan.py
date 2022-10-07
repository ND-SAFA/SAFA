from typing import List, Tuple

import pandas as pd

from experiment.gan.constants import BASE_MODEL_NAME, MODEL_EXPORT_PATH
from experiment.gan.create_data import LABEL_PARAM, TEST_EXPORT_PATH, TEXT_PARAM, TRAIN_EXPORT_PATH
from gan.gan_args import GanArgs
from gan.gan_bert import GanBert
from gan.optimizer_args import OptimizerArgs
from gan.schedular_args import SchedulerArgs


def df_to_examples(df: pd.DataFrame) -> List[Tuple[str, int]]:
    texts = df[TEXT_PARAM]
    labels = df[LABEL_PARAM]
    examples = []
    for text, label in zip(texts, labels):
        examples.append((text, label))
    return examples


if __name__ == "__main__":
    train_df = pd.read_csv(TRAIN_EXPORT_PATH)
    test_df = pd.read_csv(TEST_EXPORT_PATH)

    train_examples = df_to_examples(train_df)
    test_examples = df_to_examples(test_df)
    gan_args = GanArgs(train_examples, test_examples=test_examples, model_name=BASE_MODEL_NAME)
    optimizer_args = OptimizerArgs(num_train_epochs=10)
    scheduler_args = SchedulerArgs()

    gan_bert = GanBert(gan_args, optimizer_args, scheduler_args)
    bert_model, tokenizer = gan_bert.train()
    bert_model.save_pretrained(MODEL_EXPORT_PATH)
    tokenizer.save_pretrained(MODEL_EXPORT_PATH)
    tokenizer.save_vocabulary(MODEL_EXPORT_PATH)
