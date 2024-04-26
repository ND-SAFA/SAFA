import random
from typing import Any

from tgen.contradictions.contradictions_args import ContradictionsArgs
from tgen.contradictions.contradictions_detector import ContradictionsDetector
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs


class HealthCheckJob(AbstractJob):
    RANDOM_SELECTION = "RANDOM"
    random.seed(0)

    def __init__(self, job_args: JobArgs, req_id: str):
        """
        Initializes the job to detect contradictions in requirements.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        """
        super().__init__(job_args, require_data=True)
        self.req_id = req_id if req_id.upper() != self.RANDOM_SELECTION else random.choice(self.job_args.dataset.artifact_df.index)

    def _run(self) -> Any:
        """
        Runs the job to detect duplicates.
        :return:
        """
        pipeline_params = self.job_args.get_args_for_pipeline(ContradictionsArgs)
        args = ContradictionsArgs(**pipeline_params)
        detector = ContradictionsDetector(args)
        conflicting_ids = detector.detect(self.req_id)
        return conflicting_ids
