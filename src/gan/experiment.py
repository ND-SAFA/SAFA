import json
import os
from typing import List, Tuple

import numpy as np
import pandas as pd

from gan.gan_args import Examples, GanArgs
from gan.gan_bert import GanBert
from gan.optimizer_args import OptimizerArgs
from gan.schedular_args import SchedulerArgs

ID_PARAM = "ID"
CONTENT_PARAM = "Content"
SOURCE_PARAM = "Source"
TARGET_PARAM = "Target"


def read_examples(data_file_path: str) -> Examples:
    examples = []
    examples_df = pd.read_csv(data_file_path).sample(n=100)
    for i, example in examples_df.iterrows():
        ex_text = example["text"]
        ex_label = int(example["label"])
        examples.append((ex_text, ex_label))
    return examples


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
    return [(text, label) for text, label in zip(texts, labels)]


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


def read_dataset_folder(folder_path: str):
    dataset_names = list(filter(lambda f: f[0] != ".", os.listdir(folder_path)))
    texts = []
    labels = []
    for dataset_name in dataset_names:
        if dataset_name in SKIP:
            continue
        print("Starting:", dataset_name)
        dataset_path = os.path.join(folder_path, dataset_name)
        dataset_texts, dataset_labels = create_dataset_examples(dataset_path)
        texts.extend(dataset_texts)
        labels.extend(dataset_labels)
    export_df = pd.DataFrame()
    export_df["text"] = texts
    export_df["label"] = labels
    return export_df


def create_dataset_examples(folder_path: str):
    matrices_path = os.path.join(folder_path, "Oracles", "TracedMatrices")
    matrices_names = list(filter(lambda f: f[0] != ".", os.listdir(matrices_path)))
    texts = []
    labels = []
    for matrix_name in matrices_names:
        source_index, target_index = matrix_name.replace(".npy", "").split("-")
        source_df = read_artifact_file(folder_path, source_index)
        target_df = read_artifact_file(folder_path, target_index)
        matrix_path = os.path.join(matrices_path, matrix_name)
        matrix = np.load(matrix_path)
        for row_i in range(matrix.shape[0]):
            for col_i in range(matrix.shape[1]):
                label = int(matrix[row_i][col_i])
                text = source_df.iloc[row_i]["text"] + " [SEP] " + target_df.iloc[col_i]["text"]
                texts.append(text)
                labels.append(label)
    return texts, labels


def read_artifact_file(base_path: str, source_index: int):
    artifact_file_name = "Level_%s.csv" % source_index
    source_file_path = os.path.join(base_path, "Artifacts", artifact_file_name)
    return pd.read_csv(source_file_path)


# Path to [data](https://www.notion.so/nd-safa/Test-Project-Data-856f9df9092742d097f5984e03069bd2)
FOLDER_PATH = "/Users/albertorodriguez/projects/calpoly/LeveragingIntermediateArtifacts/datasets"
PROJECT_PATH = "/Users/albertorodriguez/desktop/safa data/validation/LHP/answer"
SAVE_PATH = "/Users/albertorodriguez/desktop/safa data/validation/LHP/answer"
BASE_MODEL_NAME = "bert-base-uncased"
MODEL_EXPORT_NAME = "gan-bert"
MODEL_EXPORT_PATH = os.path.join(PROJECT_PATH, MODEL_EXPORT_NAME)
DATA_FILE_PATH = "se_projects.csv"
SKIP = ["TrainController", "Drone"]

if __name__ == "__main__":
    if not os.path.isfile(DATA_FILE_PATH):
        read_dataset_folder(FOLDER_PATH).to_csv(DATA_FILE_PATH, index=False)

    print("Data file created...")
    train_examples = read_examples(DATA_FILE_PATH)
    test_examples = create_data([
        ("swr.json", "SYS.json", "swr2SYS.json"),
        ("hwr.json", "SYS.json", "hwr2SYS.json"),
        ("SYS.json", "fsr.json", "SYS2fsr.json"),
        ("fsr.json", "sg.json", "fsr2sg.json")
    ])

    gan_args = GanArgs(train_examples, test_examples=test_examples, model_name=BASE_MODEL_NAME)
    optimizer_args = OptimizerArgs(num_train_epochs=10)
    scheduler_args = SchedulerArgs()

    gan_bert = GanBert(gan_args, optimizer_args, scheduler_args)
    bert_model, tokenizer = gan_bert.train()
    bert_model.save_pretrained(MODEL_EXPORT_PATH)
    tokenizer.save_pretrained(MODEL_EXPORT_PATH)
    tokenizer.save_vocabulary(MODEL_EXPORT_PATH)
