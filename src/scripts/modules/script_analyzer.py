import os
from typing import Dict, Iterator, Tuple

from constants import EXPERIMENT_ID_DEFAULT, OUTPUT_FILENAME
from data.datasets.dataset_role import DatasetRole
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult
from scripts.modules.script_runner import ScriptRunner
from train.trace_output.trace_prediction_output import TracePredictionOutput
from util.json_util import JsonUtil


class ScriptAnalyzer:
    """
    Reads evaluation output of jobs in experiment and runs statistics on them.
    """

    def __init__(self, script_runner: ScriptRunner):
        self.script_runner = script_runner

    def analyze(self):
        """
        Runs error analysis on experiment.
        :return:
        """
        for job, job_output in self.get_job_iterator():
            job.load_best_model()
            prediction_output = TracePredictionOutput(**job_output[JobResult.PREDICTION_OUTPUT])
            model_manager = job.model_manager
            eval_dataset = job.trainer_dataset_manager[DatasetRole.EVAL].to_trainer_dataset(model_manager)
            print("Analyzed job: ", job.id)

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

                if isinstance(job, AbstractTraceJob) and JobResult.PREDICTION_OUTPUT in job_output:
                    yield job, job_output
