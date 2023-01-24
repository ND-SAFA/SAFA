import argparse
import os
import subprocess
import sys

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)
# TODO: Create entry per epoch (make stage a setting param)
# TODO: Test that thing look okay with bert model

IGNORE = ["job_args", "trainer_args", "model_manager", "val_dataset_creator", "trainer_dataset_manager",
          "train_dataset", "eval_dataset_creator", "job_args"]
METRICS = ["map", "map@1", "map@2", "map@3", "ap", "f1", "f2", "precision@1", "precision@2", "precision@3", "recall@1",
           "recall@2", "recall@3"]

METRIC_PATHS = ["eval_metrics", "metrics", METRICS]
COPY_PATHS = [["experimental_vars"]] + [METRIC_PATHS]
RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])

if __name__ == "__main__":
    #
    # Imports
    #
    from scripts.script_utils import extract_info, ls_filter, ls_jobs, read_job_definition
    from util.file_util import FileUtil

    #
    #
    #
    parser = argparse.ArgumentParser(
        prog='Results reader',
        description='Reads experiment results.')
    parser.add_argument("experiment")
    args = parser.parse_args()
    file_path = os.path.join(RQ_PATH, args.experiment)
    output_file = args.experiment.split(".")[0] + ".csv"
    job_definition = read_job_definition(file_path)

    OUTPUT_DIR = job_definition["output_dir"]
    experiments = ls_jobs(OUTPUT_DIR, add_base=True)
    experiment_steps = [ls_filter(os.path.join(OUTPUT_DIR, experiment_id), ignore=IGNORE, add_base=True) for experiment_id in
                        experiments]
    step_jobs = [ls_jobs(step, add_base=True) for steps in experiment_steps for step in steps]
    entries = []
    for experiment_steps in step_jobs:
        for step_path in experiment_steps:
            job_output_path = os.path.join(step_path, "output.json")
            job_output = FileUtil.read_json_file(job_output_path)
            step_entries = extract_info(job_output, COPY_PATHS, IGNORE)
            print(len(step_entries))
            for step_entry_container in step_entries:
                entries.append(step_entry_container[0])
    entries_df = pd.DataFrame(entries)
    output_path = os.path.join(OUTPUT_DIR, output_file)
    entries_df.to_csv(output_path, index=False)
    # Push to s3
    bucket_name = os.environ.get("BUCKET", None)
    if bucket_name:
        bucket_path = os.path.join(bucket_name, output_file)
        subprocess.run(["aws", "s3", "cp", output_path, bucket_path])
    print(entries_df)
    print(output_path)
