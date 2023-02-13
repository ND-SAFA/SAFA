import itertools
import os
from typing import Dict, Iterator, Set, Tuple

from analysis.results_analyzer import ResultsAnalyzer
from constants import EXPERIMENT_ID_DEFAULT, OUTPUT_FILENAME
from data.datasets.dataset_role import DatasetRole
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult
from scripts.modules.script_runner import ScriptRunner
from train.trace_output.trace_prediction_output import TracePredictionOutput
from util.file_util import FileUtil
from util.json_util import JsonUtil
from util.logging.logger_manager import logger

DATASET_ROLE = DatasetRole.EVAL


class ScriptAnalyzer:
    """
    Reads evaluation output of jobs in experiment and runs statistics on them.
    """

    def __init__(self, script_runner: ScriptRunner, output_dir: str):
        """
        Creates script analyzer for given runner and stores output at directory.
        :param script_runner: The runner containing the experiment to analyze.
        :param output_dir: Path of directory to save results to.
        """
        self.script_runner = script_runner
        self.output_dir = os.path.expanduser(output_dir)

    def analyze(self) -> None:
        """
        Runs error analysis on experiment.
        :return: None
        """
        analyzer_store: Dict[str, Dict[int, ResultsAnalyzer]] = {}
        for job, job_output in self.get_job_iterator():
            self.analyze_job(job, job_output, analyzer_store)

        for project in analyzer_store.keys():
            intersecting_mis_predicted_links: Dict[str, Set[int]] = {}
            project_analyzer = analyzer_store[project]
            for (job_id_a, analyzer_a), (job_id_b, analyzer_b) in itertools.product(project_analyzer.items(),
                                                                                    project_analyzer.items()):
                if job_id_a == job_id_b:
                    continue
                intersecting_links = analyzer_a.mis_predictions_intersection(analyzer_b)
                intersecting_mis_predicted_links[f"{job_id_a} {job_id_b}"] = intersecting_links
            project_output_path = os.path.join(self.output_dir, project + ".json")
            FileUtil.write(intersecting_mis_predicted_links, project_output_path)
            logger.info(f"Analysis written to: {project_output_path}")

    @staticmethod
    def analyze_job(job, job_output, analyzer_store) -> None:
        """
        Analyzes the output of job and adds analyzer to store.
        :param job: The job defining the parameters to store analyzer under.
        :param job_output: The output of the job.
        :param analyzer_store: The store containing all analyzers
        :return: None
        """
        job.load_best_model()
        prediction_output = TracePredictionOutput(**job_output[JobResult.PREDICTION_OUTPUT])
        model_manager = job.model_manager
        eval_dataset = job.trainer_dataset_manager[DATASET_ROLE]
        analyzer = ResultsAnalyzer(prediction_output, eval_dataset, model_manager)
        analyzer.analyze_and_save(job.job_args.output_dir)
        ScriptAnalyzer.add_analyzer(analyzer, analyzer_store, job)

    @staticmethod
    def add_analyzer(analyzer, analyzer_store, job) -> None:
        """
        Adds analyzer to store under project defined by job
        :param analyzer: The analyzer to store.
        :param analyzer_store: The store containing all analyzers.
        :param job: The job defining the project to store analyzer under.
        :return: None
        """
        project_creator = job.trainer_dataset_manager.get_creator(DATASET_ROLE)
        project_path = project_creator.get_name()
        if project_path not in analyzer_store:
            analyzer_store[project_path] = {}
        analyzer_store[project_path][job.id] = analyzer

    def get_job_iterator(self) -> Iterator[Tuple[AbstractTraceJob, Dict]]:
        """
        :return: Iterator of jobs whose
        """
        experiment = self.script_runner.get_experiment()
        for i, step in enumerate(experiment.steps):
            step_output_dir = experiment.get_step_output_dir(EXPERIMENT_ID_DEFAULT, i)
            step.update_output_path(step_output_dir)
            for job in step.jobs:
                output_file_path = os.path.join(job.job_args.output_dir, OUTPUT_FILENAME)
                job_output = JsonUtil.read_json_file(output_file_path)

                if JobResult.PREDICTION_OUTPUT in job_output:
                    yield job, job_output
