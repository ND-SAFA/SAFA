import argparse
import os
import subprocess
import sys

from dotenv import load_dotenv

from util.logging.logger_manager import logger

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
    from data.results.experiment_definition import ExperimentDefinition
    from data.results.experiment_reader import ExperimentReader

    parser = argparse.ArgumentParser(
        prog='Results reader',
        description='Reads experiment results.')
    parser.add_argument("experiment")
    args = parser.parse_args()
    file_path = os.path.join(RQ_PATH, args.experiment)
    export_file_name = args.experiment.split(".")[0]
    output_file = export_file_name + ".csv"
    job_definition = ExperimentDefinition.read_experiment_definition(file_path)

    OUTPUT_DIR = job_definition["output_dir"]

    result_reader = ExperimentReader(OUTPUT_DIR)
    val_df, eval_df = result_reader.read()
    logger.log_with_title("Validation:", str(len(val_df)))
    logger.log_with_title("Evaluation:", str(len(eval_df)))

    """
    Export Results
    """
    val_output_path = os.path.join(OUTPUT_DIR, "results-val.csv")
    eval_output_path = os.path.join(OUTPUT_DIR, "results-eval.csv")
    val_df.to_csv(val_output_path, index=False)
    eval_df.to_csv(eval_output_path, index=False)
    logger.info(f"Exported files: {eval_output_path} & {val_output_path}")
    """
    Push to bucket and tensorboard (TODO)
    """
    bucket_name = os.environ.get("BUCKET", None)
    if bucket_name:
        bucket_path = os.path.join(bucket_name, output_file)
        for output_path in [val_output_path, eval_output_path]:
            subprocess.run(["aws", "s3", "cp", output_path, bucket_path])
    """
    Print eval
    """
    result_reader.print_val()
    result_reader.print_eval()
