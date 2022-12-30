import argparse
import os
import sys
from typing import Callable, Dict, List

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

IGNORE = ["job_args", "trainer_args"]


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


if __name__ == "__main__":
    from util.file_util import FileUtil

    parser = argparse.ArgumentParser(
        prog='Results reader',
        description='Reads experiment results.')
    parser.add_argument("path")
    args = parser.parse_args()
    base_path = os.path.expanduser(args.path)
    experiment_files = list(filter(lambda f: len(f.split("-")) >= 3, os.listdir(base_path)))

    entries = []
    for experiment_file in experiment_files:
        experiment_path = os.path.join(base_path, experiment_file)
        steps = list(filter(lambda f: f[0] != ".", os.listdir(experiment_path)))
        for step_index, step in enumerate(steps):
            step_path = os.path.join(experiment_path, step)
            step_output_path = os.path.join(step_path, "output.json")
            step_output = FileUtil.read_json_file(step_output_path)

            for job_id in step_output["jobs"]:
                print(experiment_file, step_index, job_id)
                entry = {}
                job_output_path = os.path.join(step_path, job_id, "output.json")
                job_output = FileUtil.read_json_file(job_output_path)


                def add_entries(paths: List[str], filter: Callable[[str], bool]):
                    subset_dict = get_path(job_output, paths)
                    subset_properties = filter_entries(subset_dict, filter)
                    entry.update(subset_properties)


                try:
                    add_entries(["experimental_vars"], lambda var: var not in IGNORE)
                    add_entries(["val_output", "metrics"], lambda s: "test_" not in s)
                    entries.append(entry)
                except Exception as e:
                    print(e)
                    print("Failed: E(%s) J(%s) S(%s)" % (experiment_file, job_id, step))

    entries_df = pd.DataFrame(entries)
    entries_df.to_csv(os.path.join(base_path, "results.csv"), index=False)
    print(entries_df)
