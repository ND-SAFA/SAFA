import os
import subprocess
from functools import reduce
from typing import Dict, List, Optional, Tuple

import pandas as pd

from constants import DISPLAY_METRICS, EXPERIMENTAL_VARS_IGNORE, METRICS, OS_IGNORE
from experiments.experiment_step import ExperimentStep
from jobs.components.job_result import JobResult
from scripts.results.script_definition import ScriptDefinition
from util.file_util import FileUtil
from util.json_util import JsonUtil
from util.logging.logger_manager import logger

pd.set_option('display.max_colwidth', None)


class ScriptOutputReader:
    """
    Reads the output of a script.
    """
    HEADER = "-" * 10

    def __init__(self, experiment_path: str, experimental_vars_ignore: List[str] = None, metrics: List[str] = None,
                 display_metrics: List[str] = None):
        """
        Initializes reader for experiment at path.
        :param experiment_path: Path to experiment to read.
        :param experimental_vars_ignore: List of experimental variables to ignore reading.
        :param metrics: List of metrics to read from jobs and save in results.
        :param display_metrics: List of metrics to display in CLI.
        """
        if experimental_vars_ignore is None:
            self.experiment_vars_ignore = EXPERIMENTAL_VARS_IGNORE
        if metrics is None:
            self.metrics = METRICS
        if display_metrics is None:
            self.display_metrics = DISPLAY_METRICS

        self.experiment_path = experiment_path
        self.script_name = ScriptDefinition.get_script_name(experiment_path)
        self.val_output_path = os.path.join(self.experiment_path, "validation_results.csv")
        self.eval_output_path = os.path.join(self.experiment_path, "test_results.csv")

        self.eval_df = None
        self.val_df = None

    def print_eval(self) -> None:
        """
        Prints the evaluation metrics.
        :return: None
        """
        logger.log_with_title("Evaluation Results", "")
        eval_df = self._get_eval_df()
        self.print_results(eval_df, self.metrics, self.display_metrics)

    def print_val(self) -> None:
        """
        Prints the validation metrics of experiment.
        :return: None
        """
        logger.log_with_title("Validation Results", "")
        val_df = self._get_val_df()
        self.print_results(val_df, self.metrics, self.display_metrics)

    def upload_to_s3(self) -> None:
        """
        Uploads results files to s3 bucket.
        :return: None
        """
        bucket_name = os.environ.get("BUCKET", None)
        if bucket_name:
            bucket_path = os.path.join(bucket_name, self.script_name)
            for output_path in [self.val_output_path, self.eval_output_path]:
                subprocess.run(["aws", "s3", "cp", output_path, bucket_path])

    def read(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Returns the results for validation and test sets.
        :return: Tuple of dataframe with former for validation and latter for test.
        """
        val_entries = []
        eval_entries = []
        job_paths = self.read_experiment_jobs(self.experiment_path)
        for job_path in job_paths:
            output_path = os.path.join(job_path, ExperimentStep.OUTPUT_FILENAME)
            job_result = JsonUtil.read_json_file(output_path)
            JsonUtil.require_properties(job_result, [JobResult.EXPERIMENTAL_VARS])
            base_entry = {k: v for k, v in job_result[JobResult.EXPERIMENTAL_VARS].items() if k not in self.experiment_vars_ignore}
            validation_metrics = self.read_validation_entries(job_result, self.metrics, base_entry=base_entry)
            val_entries.extend(validation_metrics)
            eval_metric_entry = self.read_eval_entry(job_result, self.metrics, base_entry=base_entry)
            if eval_metric_entry:
                eval_entries.append(eval_metric_entry)
        self.val_df, self.eval_df = pd.DataFrame(val_entries), pd.DataFrame(eval_entries)
        self.val_df.to_csv(self.val_output_path, index=False)
        self.eval_df.to_csv(self.eval_output_path, index=False)
        return self.val_df, self.eval_df

    def _get_eval_df(self) -> pd.DataFrame:
        """
        :return:Returns dataframe containing evaluations in experiment.
        """
        if self.eval_df is None:
            self.read()
        return self.eval_df

    def _get_val_df(self) -> pd.DataFrame:
        """
        :return: Returns dataframe containing validation metrics in experiment.
        """
        if self.val_df is None:
            self.read()
        return self.val_df

    @staticmethod
    def read_validation_entries(job_result: Dict, metric_names: List[str], base_entry: Dict = None, entry_id_key: str = "epoch") -> \
            List[Dict]:
        """
        Reads the validation metrics for job result
        :param job_result: The result of a job run.
        :param base_entry: The entry whose properties will be contained in each metric entry.
        :param metric_names: The names of the metrics to extract.
        :param entry_id_key: The name of the key used to identify each entry.
        :return: List of dictionary representing entries in validation metrics.
        """
        if base_entry is None:
            base_entry = {}
        val_metric_entries = []
        if JobResult.VAL_METRICS not in job_result or job_result[JobResult.VAL_METRICS] is None:
            return val_metric_entries

        for epoch_index, val_metric_entry in job_result[JobResult.VAL_METRICS].items():
            metric_entry = {**base_entry, **JsonUtil.read_params(val_metric_entry, metric_names), entry_id_key: epoch_index}
            val_metric_entries.append(metric_entry)
        return val_metric_entries

    @staticmethod
    def read_eval_entry(job_result: Dict, metrics: List[str], base_entry: Dict = None) -> Optional[Dict]:
        """
        Reads the results on the test set in results.
        :param job_result: The result of a job.
        :param metrics: The name of the metrics to extract.
        :param base_entry: Properties that each eval entry will contain.
        :return: List of evaluation entries.
        """
        if base_entry is None:
            base_entry = {}
        metric_key = ScriptOutputReader.find_eval_key(job_result, [JobResult.EVAL_METRICS, JobResult.METRICS])
        if metric_key is not None and len(job_result[metric_key]) > 0:
            return {**base_entry, **JsonUtil.read_params(job_result[metric_key], metrics)}
        return None

    @staticmethod
    def read_experiment_jobs(experiment_path: str) -> List[str]:
        """
        Reads the paths to the files containing the metrics for each run in experiment path.
        :param experiment_path: Path to experiment.
        :return: List of paths corresponding to each output file in experiment.
        """
        experiment_ids = ScriptOutputReader.ls_jobs(experiment_path, add_base_path=True)
        experiment_steps = [FileUtil.ls_filter(os.path.join(experiment_path, experiment_id), ignore=OS_IGNORE, add_base_path=True) for
                            experiment_id in experiment_ids]
        job_paths = [ScriptOutputReader.ls_jobs(step, add_base_path=True) for steps in experiment_steps for step in steps]
        job_paths = reduce(lambda a, b: a + b, job_paths)
        return job_paths

    @staticmethod
    def print_results(df: pd.DataFrame, metrics: List[str], display_metrics: List[str]) -> None:
        """
        Prints the metrics with grouped columns.
        :param df: The dataframe containing experimental vars and metrics.
        :param metrics: The metrics used to calculate with columns are the grouped columns.
        :param display_metrics: The metrics to print out in data frame.
        :return: None
        """

        group_metrics = [c for c in df.columns if c not in metrics and c != "random_seed"]
        if len(group_metrics) > 0:
            df = df.sort_values(by=group_metrics)
            output_df = df.groupby(group_metrics)[display_metrics].mean()
        elif all([c in df.columns for c in display_metrics]):
            output_df = df[display_metrics].mean()
        else:
            output_df = df
        logger.info(output_df.to_string())

    @staticmethod
    def ls_jobs(path: str, **kwargs) -> List[str]:
        """
        Returns jobs in path.
        :param path: The path to list jobs in.
        :param kwargs: Additional parameters passed to ls filter.
        :return: List of jobs in path.
        """
        return FileUtil.ls_filter(path, f=lambda p: len(p.split("-")) == 5, **kwargs)

    @staticmethod
    def find_eval_key(dict_obj: Dict, keys: List[str]) -> Optional[str]:
        """
        Returns key found in output dictionary. Return none if none found.
        :param dict_obj: The object to search key in.
        :param keys: The keys to search object key.
        :return: Key found in object.
        """
        for k in keys:
            if k in dict_obj:
                return k
        return None
