import os
from functools import reduce
from typing import Dict, List, Optional, Tuple

import pandas as pd

from experiments.experiment_step import ExperimentStep
from jobs.components.job_result import JobResult
from util.file_util import FileUtil
from util.json_util import JsonUtil
from util.logging.logger_manager import logger

METRICS = ["map", "map@1", "map@2", "map@3", "ap", "f2", "f1", "precision@1", "precision@2", "precision@3"]
DISPLAY_METRICS = ["map", "f2"]
OS_IGNORE = [".DS_Store"]
EXPERIMENTAL_VARS_IGNORE = ["job_args", "model_manager", "train_dataset_creator", "project_reader", "eval_dataset_creator",
                            "trainer_dataset_manager", "trainer_args"]
pd.set_option('display.max_colwidth', None)


class ExperimentReader:
    """
    Responsible for reading the results of an experiment.
    """
    HEADER = "-" * 10

    def __init__(self, experiment_path: str, experimental_vars_ignore: List[str] = None, metrics: List[str] = None,
                 display_metrics: List[str] = None):
        """
        Constructs reader of results for experiment at given path.
        :param experiment_path: Path to experiment containing experiments,
        :type experiment_path:
        :param experimental_vars_ignore:
        :type experimental_vars_ignore:
        :param metrics:
        :type metrics:
        :param display_metrics:
        :type display_metrics:
        """
        self.experiment_path = experiment_path
        if experimental_vars_ignore is None:
            self.experiment_vars_ignore = EXPERIMENTAL_VARS_IGNORE
        if metrics is None:
            self.metrics = METRICS
        if display_metrics is None:
            self.display_metrics = DISPLAY_METRICS
        self.eval_df = None
        self.val_df = None
        self.log_dir = os.path.join(experiment_path, "logs")
        
    def print_eval(self) -> None:
        """
        Prints the evaluation metrics.
        :return: None
        """
        logger.log_with_title("Evaluation Results", "")
        eval_df = self.get_eval_df()
        self.print_results(eval_df, self.metrics, self.display_metrics)

    def print_val(self) -> None:
        """
        Prints the validation metrics of experiment.
        :return: None
        """
        logger.log_with_title("Validation Results", "")
        val_df = self.get_val_df()
        self.print_results(val_df, self.metrics, self.display_metrics)

    def get_eval_df(self) -> pd.DataFrame:
        """
        :return:Returns dataframe containing evaluations in experiment.
        """
        if self.eval_df is None:
            self.read()
        return self.eval_df

    def get_val_df(self) -> pd.DataFrame:
        """
        :return: Returns dataframe containing validation metrics in experiment.
        """
        if self.val_df is None:
            self.read()
        return self.val_df

    def read(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Returns the results for validation and test sets.
        :return: Tuple of dataframe with former for validation and latter for test.
        """
        val_entries = []
        eval_entries = []
        experiment_jobs = self.read_experiment_jobs(self.experiment_path)
        for output_path in experiment_jobs:
            job_result = JsonUtil.read_json_file(output_path)
            JsonUtil.require_properties(job_result, [JobResult.EXPERIMENTAL_VARS])
            base_entry = {k: v for k, v in job_result[JobResult.EXPERIMENTAL_VARS].items() if k not in self.experiment_vars_ignore}
            validation_metrics = self.read_validation_entries(job_result, self.metrics, base_entry=base_entry)
            val_entries.extend(validation_metrics)
            eval_metric_entry = self.read_eval_entry(job_result, self.metrics, base_entry=base_entry)
            if eval_metric_entry:
                eval_entries.append(eval_metric_entry)
        self.val_df, self.eval_df = pd.DataFrame(val_entries), pd.DataFrame(eval_entries)
        return self.val_df, self.eval_df

    @staticmethod
    def read_validation_entries(job_result: Dict, metric_names: List[str], base_entry: Dict = None, entry_id_key: str = "epoch") -> \
            List[
                Dict]:
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
        JsonUtil.require_properties(job_result, [JobResult.VAL_METRICS])
        val_metric_entries = []
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
        JsonUtil.require_properties(job_result, [JobResult.EVAL_METRICS])
        if len(job_result[JobResult.EVAL_METRICS]) > 0:
            return {**base_entry, **JsonUtil.read_params(job_result[JobResult.EVAL_METRICS], metrics)}
        return None

    @staticmethod
    def read_experiment_jobs(experiment_path: str) -> List[str]:
        """
        Reads the paths to the files containing the metrics for each run in experiment path.
        :param experiment_path: Path to experiment.
        :return: List of paths corresponding to each output file in experiment.
        """
        experiments = ExperimentReader.ls_jobs(experiment_path, add_base_path=True)
        experiment_steps = [FileUtil.ls_filter(os.path.join(experiment_path, experiment_id), ignore=OS_IGNORE, add_base_path=True) for
                            experiment_id
                            in
                            experiments]
        step_jobs = [ExperimentReader.ls_jobs(step, add_base_path=True) for steps in experiment_steps for step in steps]
        step_jobs = reduce(lambda a, b: a + b, step_jobs)
        step_jobs = [os.path.join(p, ExperimentStep.OUTPUT_FILENAME) for p in step_jobs]
        return step_jobs

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
        else:
            output_df = df[display_metrics].mean()
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
