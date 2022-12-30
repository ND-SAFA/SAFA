import argparse
import os

import pandas as pd

from util.file_util import FileUtil

IGNORE = ["job_args", "trainer_args"]

if __name__ == "__main__":
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
                entry = {}
                job_output_path = os.path.join(step_path, job_id, "output.json")
                job_output = FileUtil.read_json_file(job_output_path)
                for var_name, var_value in job_output["experimental_vars"].items():
                    if var_name in IGNORE:
                        continue
                    entry[var_name] = var_value

                for metric_name, metric_value in job_output["val_output"]["metrics"].items():
                    if "test_" not in metric_name:
                        entry[metric_name] = metric_value
                entries.append(entry)

    entries_df = pd.DataFrame(entries)
    entries_df.to_csv(os.path.join(base_path, "results.csv"), index=False)
