import argparse
import os
import sys
from typing import Callable, Dict, List

import pandas as pd
from dotenv import load_dotenv

from util.file_util import FileUtil

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

IGNORE = ["job_args", "trainer_args", "model_manager", "val_dataset_creator", "trainer_dataset_manager"]


def get_path(entry_dict: Dict, paths: List[str]):
    if len(paths) == 0:
        return entry_dict
    current_key = paths[0]
    next_keys = paths[1:]
    if current_key not in entry_dict:
        raise ValueError("Could not find %s in %s." % (current_key, entry_dict))
    return get_path(entry_dict[current_key], next_keys)


def filter_entries(entry_dict: Dict, filter: Callable[[str], bool] = lambda s: s):
    return {k: v for k, v in entry_dict.items() if filter(k)}


def ls_filter(path: str, f: Callable[[str], bool] = None, ignore: List[str] = None):
    if f is None:
        f = lambda s: s
    if ignore is None:
        ignore = []
    return list(filter(lambda p: f(p) and f not in ignore, os.listdir(path)))


def ls_jobs(path: str):
    return ls_filter(path, f=lambda p: len(p.split("-")) == 5)


def get_dict_path(data: Dict, instructions: List[str]):
    if len(instructions) == 0:
        return data
    return get_dict_path(data[instructions[0]], instructions[1:])


def extract_info(data: Dict, copy_paths: List[List[str]]):
    result = {}
    for path in copy_paths:
        value = get_dict_path(data, path)
        if isinstance(value, dict):
            filter_values = {k: v for k, v in value.items() if k not in IGNORE}
            result = {**result, **filter_values}
        else:
            result = {**result, path[-1]: value}

    return result


instructions = [["metrics", "map"], ["metrics", "epoch"], ["experimental_vars"]]
IGNORE = ["job_args", "trainer_dataset_manager", "trainer_args"]
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Results reader',
        description='Reads experiment results.')
    parser.add_argument("path")
    args = parser.parse_args()
    BASE_PATH = os.path.expanduser(args.path)
    TRAINER_PATH = os.path.join(BASE_PATH, "trainer")
    EPOCH_RUNS = ls_filter(TRAINER_PATH, ignore=[".DS_Store", "runs"])

    entries = []
    for epoch in EPOCH_RUNS:
        epoch_path = os.path.join(TRAINER_PATH, epoch)
        jobs = ls_jobs(epoch_path)
        for job_id in jobs:
            job_output_path = os.path.join(epoch_path, job_id, "output.json")
            job_output = FileUtil.read_json_file(job_output_path)
            entry = extract_info(job_output, instructions)
            entries.append(entry)
    entries_df = pd.DataFrame(entries)
    output_path = os.path.join(BASE_PATH, "result.csv")
    entries_df.to_csv(output_path, index=False)
