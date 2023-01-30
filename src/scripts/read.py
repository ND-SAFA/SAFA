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

METRIC_PATHS = ["val_metrics", "metrics", METRICS]
COPY_PATHS = [["experimental_vars"]] + [METRIC_PATHS]
RQ_PATH = os.path.expanduser(os.environ["RQ_PATH"])

if __name__ == "__main__":
    #
    # Imports
    #
    from scripts.script_utils import ls_filter, ls_jobs, read_job_definition, read_params
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
    export_file_name = args.experiment.split(".")[0]
    output_file = export_file_name + ".csv"
    job_definition = read_job_definition(file_path)

    OUTPUT_DIR = job_definition["output_dir"]
    experiments = ls_jobs(OUTPUT_DIR, add_base=True)
    experiment_steps = [ls_filter(os.path.join(OUTPUT_DIR, experiment_id), ignore=IGNORE, add_base=True) for experiment_id in
                        experiments]
    step_jobs = [ls_jobs(step, add_base=True) for steps in experiment_steps for step in steps]
    METRICS = ["map", "f2"]
    IGNORE = ["job_args", "model_manager"]
    val_entries = []
    eval_entries = []
    for job in ls_jobs(OUTPUT_DIR):
        job_path = os.path.join(OUTPUT_DIR, job)
        for step in ls_filter(job_path, ignore=[".DS_Store"]):
            step_path = os.path.join(job_path, step)
            for step_job in ls_jobs(step_path):
                step_job_path = os.path.join(step_path, step_job)
                output_path = os.path.join(step_job_path, "output.json")
                output_json = FileUtil.read_json_file(output_path)
                base_entry = {k: v for k, v in output_json["experimental_vars"].items() if k not in IGNORE}

                for epoch_index, metrics in output_json["val_metrics"].items():
                    metrics_entry = metrics["metrics"]
                    # print(metrics.keys())
                    entry = {**base_entry, **read_params(metrics_entry, METRICS), "epoch": epoch_index}
                    val_entries.append(entry)
                if len(output_json["eval_metrics"]) > 0:
                    eval_entries.append({**base_entry, **read_params(output_json["eval_metrics"], METRICS)})
    print("Validation:", len(val_entries))
    print("Evaluation:", len(eval_entries))

    """
    Export Results
    """
    val_output_path = os.path.join(OUTPUT_DIR, export_file_name + "-" + "val.csv")
    eval_output_path = os.path.join(OUTPUT_DIR, export_file_name + "-" + "eval.csv")
    val_df = pd.DataFrame(val_entries)
    # val_df.to_csv(val_output_path, index=False)
    eval_df = pd.DataFrame(eval_entries)
    # eval_df.to_csv(eval_output_path, index=False)
    # Push to s3
    bucket_name = os.environ.get("BUCKET", None)
    if bucket_name:
        bucket_path = os.path.join(bucket_name, output_file)
        for output_path in [val_output_path, eval_output_path]:
            subprocess.run(["aws", "s3", "cp", output_path, bucket_path])
    """
    Print eval
    """
    GROUP_METRICS = [c for c in eval_df.columns if c not in METRICS and c != "random_seed"]
    if len(GROUP_METRICS) > 0:
        print(eval_df.groupby(GROUP_METRICS)[METRICS].mean())
    else:
        print(val_df[METRICS].mean())
    print(f"Exported files: {eval_output_path} & {val_output_path}")
