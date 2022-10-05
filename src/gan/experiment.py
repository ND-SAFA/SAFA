import json
import os
from typing import List, Tuple

import pandas as pd

from gan.gan_args import GanArgs
from gan.gan_bert import GanBert
from gan.optimizer_args import OptimizerArgs
from gan.schedular_args import SchedulerArgs

# Path to [data](https://www.notion.so/nd-safa/Test-Project-Data-856f9df9092742d097f5984e03069bd2)
PROJECT_PATH = "/Users/albertorodriguez/desktop/safa data/validation/LHP/answer"
SAVE_PATH = "/Users/albertorodriguez/desktop/safa data/validation/LHP/answer"
MODEL_NAME = "gan-bert"
MODEL_PATH = os.path.join(PROJECT_PATH, MODEL_NAME)
EXPORT_PATH = "results.csv"

ID_PARAM = "ID"
CONTENT_PARAM = "Content"
SOURCE_PARAM = "Source"
TARGET_PARAM = "Target"


def create_data(artifact_levels: List[Tuple[str, str, str]]):
    texts = []
    labels = []
    for artifact_level in artifact_levels:
        if ".csv" in artifact_level[0]:
            layer_texts, layer_labels = read_csv_layer(artifact_level[0], artifact_level[1], artifact_level[2])
            texts.extend(layer_texts)
            labels.extend(layer_labels)
        elif ".json" in artifact_level[0]:
            layer_texts, layer_labels = read_json_layer(artifact_level[0], artifact_level[1], artifact_level[2])
            texts.extend(layer_texts)
            labels.extend(layer_labels)
    export_df = pd.DataFrame()
    export_df["text"] = texts
    export_df["label"] = labels
    return export_df


def read_csv_layer(source_file_name: str, target_file_name: str, link_file_name: str):
    source_df = pd.read_csv(os.path.join(PROJECT_PATH, source_file_name))
    target_df = pd.read_csv(os.path.join(PROJECT_PATH, target_file_name))
    links_df = pd.read_csv(os.path.join(PROJECT_PATH, link_file_name))

    texts = []
    labels = []
    for source_index, source_item in source_df.iterrows():
        for target_index, target_item in target_df.iterrows():
            query = links_df[
                (links_df[SOURCE_PARAM] == source_item[ID_PARAM]) & (links_df[TARGET_PARAM] == target_item[ID_PARAM])]
            text = source_item[CONTENT_PARAM] + " [SEP] " + target_item[CONTENT_PARAM]
            label = 1 if len(query) > 0 else 0
            texts.append(text)
            labels.append(label)

    return texts, labels


def read_json_layer(source_file_name: str, target_file_name: str, link_file_name: str):
    source_df = read_json_file(os.path.join(PROJECT_PATH, source_file_name))
    target_df = read_json_file(os.path.join(PROJECT_PATH, target_file_name))
    links_df = read_json_file(os.path.join(PROJECT_PATH, link_file_name))

    texts = []
    labels = []
    for source_artifact in source_df["artifacts"]:
        for target_artifact in target_df["artifacts"]:
            query = list(filter(lambda t: t["sourceName"] == source_artifact["name"] and
                                          t["targetName"] == target_artifact["name"],
                                links_df["traces"]))
            text = source_artifact["body"] + " [SEP] " + target_artifact["body"]
            label = 1 if len(query) > 0 else 0
            texts.append(text)
            labels.append(label)

    return texts, labels


def read_json_file(file_path: str):
    with open(file_path, "r") as json_file:
        return json.loads(json_file.read())


def run_gan(file_path: str, save_path: str):
    gan_args = GanArgs(file_path, model_name="thearod5/automotive")
    optimizer_args = OptimizerArgs(num_train_epochs=1)
    scheduler_args = SchedulerArgs()

    gan_bert = GanBert(gan_args, optimizer_args, scheduler_args)
    bert_model, tokenizer = gan_bert.train()
    bert_model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
    tokenizer.save_vocabulary(save_path)


if __name__ == "__main__":
    data_df = create_data([
        ("swr.json", "SYS.json", "swr2SYS.json"),
        ("hwr.json", "SYS.json", "hwr2SYS.json"),
        ("SYS.json", "fsr.json", "SYS2fsr.json"),
        ("fsr.json", "sg.json", "fsr2sg.json")
    ])
    print(len(data_df), EXPORT_PATH)
    data_df.to_csv(EXPORT_PATH, index=False)

    run_gan(EXPORT_PATH, MODEL_PATH)
