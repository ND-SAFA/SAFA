import itertools
import os
import subprocess
from typing import Dict, Iterator, List, Set, Tuple

from analysis.results_analyzer import ResultsAnalyzer
from constants import EXPERIMENTAL_VARS_IGNORE, EXPERIMENT_ID_DEFAULT, OUTPUT_FILENAME
from data.datasets.dataset_role import DatasetRole
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult
from scripts.modules.analysis_types import JobCollection, MultiJobAnalysis
from scripts.modules.script_runner import ScriptRunner
from train.trace_output.trace_prediction_output import TracePredictionOutput
from util.file_util import FileUtil
from util.json_util import JsonUtil
from util.logging.logger_manager import logger

DATASET_ROLE = DatasetRole.EVAL
GROUPING_VARS = ["name", "project_path", "random_seed"]
LinkStore = Dict[str, Dict]
AnalyzerStore = Dict[str, Dict[int, Dict[str, ResultsAnalyzer]]]


class ScriptAnalyzer:
    """
    Reads evaluation output of jobs in experiment and runs statistics on them.
    """

    def __init__(self, script_runners: List[ScriptRunner], output_dir: str):
        """
        Creates script analyzer for given runner and stores output at directory.
        :param script_runners: The runners containing the experiment to analyze.
        :param output_dir: Path of directory to save results to.
        """
        self.script_runners = script_runners
        self.name = "-".join([r.script_name for r in script_runners])
        self.output_dir = os.path.expanduser(output_dir)
        self.analyzer_store: AnalyzerStore = {}
        self.link_analysis_store: LinkStore = {}
        self.jobs: JobCollection = {}

    def analyze(self) -> None:
        """
        Runs error analysis on experiment.
        :return: None
        """
        for job, job_output in self.get_job_iterator():
            job.trainer_dataset_manager.get_datasets()  # sets construction variables
            self.analyze_job(job, job_output)

        intersection_analysis = {}
        for project in self.analyzer_store.keys():
            intersection_analysis[project] = {}
            for random_seed in self.analyzer_store[project].keys():
                intersection_analysis[project][random_seed] = {}
                intersecting_mis_predicted_links: Dict[str, Set[int]] = {}
                project_analyzer = self.analyzer_store[project][random_seed]
                for (job_id_a, analyzer_a), (job_id_b, analyzer_b) in itertools.product(project_analyzer.items(),
                                                                                        project_analyzer.items()):
                    analysis_id = f"{job_id_a} x {job_id_b}"
                    reverse_analysis_id = f"{job_id_b} x {job_id_a}"
                    if job_id_a == job_id_b or reverse_analysis_id in intersecting_mis_predicted_links:
                        continue
                    intersecting_links = analyzer_a.mis_predictions_intersection(analyzer_b)
                    intersection_analysis[project][random_seed][analysis_id] = intersecting_links
        file_name = f"{self.name}.json"
        output_path = os.path.join(self.output_dir, file_name)
        final_analysis = MultiJobAnalysis(jobs=self.jobs,
                                          job_analysis=self.link_analysis_store,
                                          intersections=intersection_analysis)
        FileUtil.write(final_analysis, output_path)
        if "BUCKET" in os.environ:
            subprocess.run(["aws", "s3", "cp", output_path, f"s3://safa-datasets-open/results/analysis/{file_name}"])
        logger.info(f"Analysis written to: {output_path}")

    def analyze_job(self, job, job_output) -> None:
        """
        Analyzes the output of job and adds analyzer to store.
        :param job: The job defining the parameters to store analyzer under.
        :param job_output: The output of the job.
        :return: None
        """
        job_id = self.get_job_id(job)
        project_name = self.get_project_name(job)
        random_seed = job.job_args.random_seed

        job.load_best_model()
        prediction_output = TracePredictionOutput(**job_output[JobResult.PREDICTION_OUTPUT])
        model_manager = job.model_manager
        eval_dataset = job.trainer_dataset_manager[DATASET_ROLE]
        analyzer = ResultsAnalyzer(prediction_output, eval_dataset, model_manager)
        job_analysis = analyzer.analyze()
        if project_name not in self.link_analysis_store:
            self.link_analysis_store[project_name] = {}
        if random_seed not in self.link_analysis_store[project_name]:
            self.link_analysis_store[project_name][random_seed] = {}
        if project_name not in self.jobs:
            self.jobs[project_name] = {}
        if random_seed not in self.jobs[project_name]:
            self.jobs[project_name][random_seed] = []

        self.link_analysis_store[project_name][random_seed][job_id] = job_analysis
        self.jobs[project_name][random_seed].append(job_id)
        self.add_analyzer(analyzer, job)

    def add_analyzer(self, analyzer, job) -> None:
        """
        Adds analyzer to store under project defined by job
        :param analyzer: The analyzer to store.
        :param job: The job defining the project to store analyzer under.
        :return: None
        """
        project_creator = job.trainer_dataset_manager.get_creator(DATASET_ROLE)
        project_path = project_creator.get_name()
        random_seed = job.job_args.random_seed
        if project_path not in self.analyzer_store:
            self.analyzer_store[project_path] = {}
        if random_seed not in self.analyzer_store[project_path]:
            self.analyzer_store[project_path][random_seed] = {}
        job_id = ScriptAnalyzer.get_job_id(job)
        self.analyzer_store[project_path][random_seed][job_id] = analyzer

    def get_job_iterator(self) -> Iterator[Tuple[AbstractTraceJob, Dict]]:
        """
        :return: Iterator of jobs whose
        """
        for script_runner in self.script_runners:
            experiment = script_runner.get_experiment()
            for i, step in enumerate(experiment.steps):
                step_output_dir = experiment.get_step_output_dir(EXPERIMENT_ID_DEFAULT, i)
                step.update_output_path(step_output_dir)
                for job in step.jobs:
                    output_file_path = os.path.join(job.job_args.output_dir, OUTPUT_FILENAME)
                    if not os.path.isfile(output_file_path):
                        continue

                    job_output = JsonUtil.read_json_file(output_file_path)

                    if JobResult.PREDICTION_OUTPUT in job_output:
                        yield job, job_output

    @staticmethod
    def get_job_id(job: AbstractTraceJob) -> str:
        """
        Returns readable job id from the experimental vars.
        :param job: The job whose id is returned.
        :return: Stringified Experimental vars of job.
        """
        experimental_vars = job.result[JobResult.EXPERIMENTAL_VARS]
        id_vars = []
        for experimental_variable in experimental_vars:
            if experimental_variable in GROUPING_VARS or experimental_variable in EXPERIMENTAL_VARS_IGNORE:
                continue
            var = experimental_vars[experimental_variable]
            var = var.replace("/", "-")
            id_vars.append(f"{var}")
        return "*".join(id_vars) if len(id_vars) else "NO_EXPERIMENT_VARIABLES"

    @staticmethod
    def get_project_name(job: AbstractTraceJob) -> str:
        """
        Returns the name of the project used for training.
        :param job: The job whose training dataset name is returned.
        :return: Dataset name.
        """
        project_creator = job.trainer_dataset_manager.get_creator(DATASET_ROLE)
        return project_creator.get_name()
