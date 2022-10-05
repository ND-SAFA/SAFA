import os

import pandas as pd

from gan.gan_args import GanArgs
from gan.gan_bert import GanBert
from gan.optimizer_args import OptimizerArgs
from gan.schedular_args import SchedulerArgs

PROJECT_PATH = "/Users/albertorodriguez/projects/safa/bend/resources/tests/before"
SOURCE_PATH = os.path.join(PROJECT_PATH, "Design.csv")
TARGET_PATH = os.path.join(PROJECT_PATH, "Requirement.csv")
LINK_PATH = os.path.join(PROJECT_PATH, "Design2Requirement.csv")
EXPORT_PATH = "results.csv"

ID_PARAM = "ID"
CONTENT_PARAM = "Content"
SOURCE_PARAM = "Source"
TARGET_PARAM = "Target"


def create_data(source_data_path: str, target_data_path: str, link_data_path: str, export_path: str):
    source_df = pd.read_csv(source_data_path)
    target_df = pd.read_csv(target_data_path)
    links_df = pd.read_csv(link_data_path)

    texts = []
    labels = []
    for source_index, source_item in source_df.iterrows():
        for target_index, target_item in target_df.iterrows():
            query = links_df[
                (links_df[SOURCE_PARAM] == source_item[ID_PARAM]) & (links_df[TARGET_PARAM] == target_item[ID_PARAM])]
            text = source_item[CONTENT_PARAM] + " [SEP]" + target_item[CONTENT_PARAM]
            label = 1 if len(query) > 0 else 0
            texts.append(text)
            labels.append(label)

    export_df = pd.DataFrame()
    export_df["text"] = texts
    export_df["label"] = labels
    export_df.to_csv(export_path, index=False)


def run_gan(file_path: str):
    gan_args = GanArgs(file_path)
    optimizer_args = OptimizerArgs()
    scheduler_args = SchedulerArgs()

    gan_bert = GanBert(gan_args, optimizer_args, scheduler_args)
    gan_bert.train()


if __name__ == "__main__":
    create_data(SOURCE_PATH, TARGET_PATH, LINK_PATH, EXPORT_PATH)

    run_gan(EXPORT_PATH)
