import os
from functools import reduce
from typing import Dict, List, Optional, Tuple

import pandas as pd

from tgen.common.constants.experiment_constants import OUTPUT_FILENAME
from tgen.common.constants.script_constants import DISPLAY_METRICS, EXPERIMENTAL_VARS_IGNORE, METRIC_NAMES
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.json_util import JsonUtil
from tgen.jobs.components.job_result import JobResult

pd.set_option('display.max_colwidth', None)


class ScriptOutputReader:
    """
    Reads the output of a script.
    """
    HEADER = "-" * 10

    METRICS = "metrics"
    VAL_METRICS = "val_metrics"
    EVAL_METRICS = "eval_metrics"
    PREDICTION_OUTPUT = "prediction_output"

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
            self.metric_names = METRIC_NAMES
        if display_metrics is None:
            self.display_metrics = DISPLAY_METRICS

        self.experiment_path = experiment_path
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
        self.print_results(eval_df, self.metric_names, self.display_metrics)

    def print_val(self) -> None:
        """
        Prints the validation metrics of experiment.
        :return: None
        """

    def read(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Returns the results for validation and test sets.
        :return: Tuple of dataframe with former for validation and latter for test.
        """
        job_paths = self.read_experiment_jobs(self.experiment_path)
        for job_path in job_paths:
            output_path = os.path.join(job_path, OUTPUT_FILENAME)
            if not os.path.exists(output_path):
                continue
            job_result = JobResult.from_dict(JsonUtil.read_json_file(output_path))

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
    def read_validation_entries(job_output: Dict, metric_names: List[str], base_entry: Dict = None, entry_id_key: str = "epoch") -> \
            List[Dict]:
        """
        Reads the validation metrics for job result
        :param job_output: The result of a job run.
        :param base_entry: The entry whose properties will be contained in each metric entry.
        :param metric_names: The names of the metrics to extract.
        :param entry_id_key: The name of the key used to identify each entry.
        :return: List of dictionary representing entries in validation metrics.
        """
        if base_entry is None:
            base_entry = {}
        val_metric_entries = []
        if ScriptOutputReader.VAL_METRICS not in job_output or job_output[ScriptOutputReader.VAL_METRICS] is None:
            return val_metric_entries

        for epoch_index, val_metric_entry in job_output[ScriptOutputReader.VAL_METRICS].items():
            metric_entry = {**base_entry, **JsonUtil.read_params(val_metric_entry, metric_names), entry_id_key: epoch_index}
            val_metric_entries.append(metric_entry)
        return val_metric_entries

    @staticmethod
    def read_eval_entry(job_output: Dict, metrics: List[str], base_entry: Dict = None) -> Optional[Dict]:
        """
        Reads the results on the test set in results.
        :param job_output: The result of a job.
        :param metrics: The name of the metrics to extract.
        :param base_entry: Properties that each eval entry will contain.
        :return: List of evaluation entries.
        """
        if base_entry is None:
            base_entry = {}
        job_output = job_output[
            ScriptOutputReader.PREDICTION_OUTPUT] if ScriptOutputReader.PREDICTION_OUTPUT in job_output else job_output
        metric_key = ScriptOutputReader.find_eval_key(job_output, [ScriptOutputReader.EVAL_METRICS, ScriptOutputReader.METRICS])
        if metric_key is not None and job_output[metric_key] is not None and len(job_output[metric_key]) > 0:
            return {**base_entry, **JsonUtil.read_params(job_output[metric_key], metrics)}
        return None

    @staticmethod
    def read_experiment_jobs(experiment_path: str) -> List[str]:
        """
        Reads the paths to the files containing the metrics for each run in experiment path.
        :param experiment_path: Path to experiment.
        :return: List of paths corresponding to each output file in experiment.
        """
        experiment_paths = FileUtil.ls_dir(experiment_path)
        experiment_step_paths = [FileUtil.ls_dir(experiment_path) for experiment_path in experiment_paths]
        job_paths = [FileUtil.ls_dir(experiment_step_job_path) for experiment_step_path in experiment_step_paths
                     for experiment_step_job_path in experiment_step_path]
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
