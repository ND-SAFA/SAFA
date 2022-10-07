import os

import numpy as np
import pandas as pd

from experiment.gan.constants import ID_PARAM, ProjectData, SKIP, TEXT_PARAM
from experiment.gan.data.common import create_data_df


def read_traceability_projects(folder_path: str):
    dataset_names = list(filter(lambda f: f[0] != ".", os.listdir(folder_path)))
    sources = []
    targets = []
    labels = []
    for dataset_name in dataset_names:
        if dataset_name in SKIP:
            continue
        print("Starting:", dataset_name)
        dataset_path = os.path.join(folder_path, dataset_name)
        dataset_sources, dataset_targets, dataset_labels = read_traceability_project(dataset_path)
        sources.extend(dataset_sources)
        targets.extend(dataset_targets)
        labels.extend(dataset_labels)
    return create_data_df(sources, targets, labels)


def read_traceability_project(folder_path: str) -> ProjectData:
    matrices_path = os.path.join(folder_path, "Oracles", "TracedMatrices")
    matrices_names = list(filter(lambda f: f[0] != ".", os.listdir(matrices_path)))
    sources = []
    targets = []
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
                source_row = source_df.iloc[row_i]
                target_row = target_df.iloc[col_i]

                source_text = source_row[TEXT_PARAM]
                source_id = source_row[ID_PARAM.lower()]

                target_text = target_row[TEXT_PARAM]
                target_id = target_row[ID_PARAM.lower()]

                sources.append((source_id, source_text))
                targets.append((target_id, target_text))
                labels.append(label)
    return sources, targets, labels


def read_artifact_file(base_path: str, source_index: int):
    artifact_file_name = "Level_%s.csv" % source_index
    source_file_path = os.path.join(base_path, "Artifacts", artifact_file_name)
    return pd.read_csv(source_file_path)
