import argparse
import os
import sys

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

IGNORE = ["job_args", "trainer_args", "model_manager", "val_dataset_creator", "trainer_dataset_manager",
          "train_dataset"]
COPY_PATHS = [["metrics", "map"], ["metrics", "f1"], ["metrics", "f2"], ["experimental_vars"]]
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
    job_definition = read_job_definition(args.experiment)

    OUTPUT_DIR = job_definition["output_dir"]

    entries = []
    for experiment_id in ls_jobs(OUTPUT_DIR):
        experiment_path = os.path.join(OUTPUT_DIR, experiment_id)
        for step in ls_filter(experiment_path, ignore=IGNORE):
            step_path = os.path.join(experiment_path, step)
            for job_id in ls_jobs(step_path):
                job_output_path = os.path.join(step_path, job_id, "output.json")
                job_output = FileUtil.read_json_file(job_output_path)
                entry = extract_info(job_output, COPY_PATHS, IGNORE)
                entries.append(entry)

    entries_df = pd.DataFrame(entries)
    output_path = os.path.join(OUTPUT_DIR, "result.csv")
    entries_df.to_csv(output_path, index=False)
    print(entries_df)
