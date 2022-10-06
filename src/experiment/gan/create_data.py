import json
import os
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

ID_PARAM = "ID"
CONTENT_PARAM = "Content"
SOURCE_PARAM = "Source"
TARGET_PARAM = "Target"
TEXT_PARAM = "text"
LABEL_PARAM = "label"


def read_examples(data_file_path: str) -> pd.DataFrame:
    texts = []
    labels = []
    examples_df = pd.read_csv(data_file_path)
    for i, example in examples_df.iterrows():
        ex_text = example[TEXT_PARAM]
        ex_label = int(example[LABEL_PARAM])
        texts.append(ex_text)
        labels.append(ex_label)
    return create_df(texts, labels)


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
    return create_df(texts, labels)


def read_csv_layer(source_file_name: str, target_file_name: str, link_file_name: str):
    source_df = pd.read_csv(os.path.join(LHP_DATA_PATH, source_file_name))
    target_df = pd.read_csv(os.path.join(LHP_DATA_PATH, target_file_name))
    links_df = pd.read_csv(os.path.join(LHP_DATA_PATH, link_file_name))

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
    source_df = read_json_file(os.path.join(LHP_DATA_PATH, source_file_name))
    target_df = read_json_file(os.path.join(LHP_DATA_PATH, target_file_name))
    links_df = read_json_file(os.path.join(LHP_DATA_PATH, link_file_name))

    texts = []
    labels = []
    seen_traces = []
    for source_artifact in source_df["artifacts"]:
        for target_artifact in target_df["artifacts"]:
            source_name = source_artifact["name"]
            target_name = target_artifact["name"]
            trace_key = "%s-%s" % (source_name, target_name)
            if trace_key in seen_traces:
                continue
            query = list(filter(lambda t: t["sourceName"] == source_name and
                                          t["targetName"] == target_name,
                                links_df["traces"]))
            text = source_artifact["body"] + " [SEP] " + target_artifact["body"]
            label = 1 if len(query) > 0 else 0
            texts.append(text)
            labels.append(label)
            seen_traces.append(trace_key)

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


def create_df(text_examples: List[str], label_examples: List[int]) -> pd.DataFrame:
    df = pd.DataFrame()
    df[TEXT_PARAM] = text_examples
    df[LABEL_PARAM] = label_examples
    return df


# Path to [data](https://www.notion.so/nd-safa/Test-Project-Data-856f9df9092742d097f5984e03069bd2)
SOFTWARE_DATA_PATH = "/Users/albertorodriguez/projects/calpoly/LeveragingIntermediateArtifacts/datasets"
LHP_DATA_PATH = "/Users/albertorodriguez/desktop/safa data/validation/LHP/answer"
TRAINING_DATA_PATH = "/Users/albertorodriguez/desktop/safa data/validation/LHP/experiments"
BASE_MODEL_NAME = "bert-base-uncased"
MODEL_EXPORT_NAME = "gan-bert"
MODEL_EXPORT_PATH = os.path.join(LHP_DATA_PATH, MODEL_EXPORT_NAME)
DATA_FILE_PATH = "../../gan/se_projects.csv"
SKIP = ["TrainController", "Drone"]
TEST_SIZE = 0.5

if __name__ == "__main__":
    if not os.path.isfile(DATA_FILE_PATH):
        read_dataset_folder(SOFTWARE_DATA_PATH).to_csv(DATA_FILE_PATH, index=False)

    print("Data file created...")
    software_df = read_examples(DATA_FILE_PATH)
    lhp_df = create_data([
        ("swr.json", "SYS.json", "swr2SYS.json"),
        ("hwr.json", "SYS.json", "hwr2SYS.json"),
        ("SYS.json", "fsr.json", "SYS2fsr.json"),
        ("fsr.json", "sg.json", "fsr2sg.json")
    ])
    train_df, test_df = train_test_split(lhp_df, test_size=TEST_SIZE)

    train_df = pd.concat([train_df, software_df])

    train_export_path = os.path.join(TRAINING_DATA_PATH, "train.csv")
    test_export_path = os.path.join(TRAINING_DATA_PATH, "test.csv")
    train_df.to_csv(train_export_path, index=False)
    test_df.to_csv(test_export_path, index=False)

    print("Train", "-" * 25)
    print(len(train_df))
    print(train_df[LABEL_PARAM].value_counts())
