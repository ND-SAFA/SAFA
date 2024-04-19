from typing import Any

from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs


class HealthCheckJob(AbstractJob):

    def __init__(self, job_args: JobArgs):
        """
        Initializes the job to detect contradictions in requirements.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        """
        super().__init__(job_args, require_data=True)

    def _run(self) -> Any:
        """
        Runs the job to detect duplicates.
        :return:
        """
