from jobs.abstract_trace_job import AbstractTraceJob
from jobs.job_args import JobArgs
from jobs.results.job_result import JobResult


class CreateDatasetsJob(AbstractTraceJob):

    def __init__(self, job_args: JobArgs):
        """
        Responsible for creating and saving new datasets
        """
        job_args.save_dataset_splits = True
        super().__init__(job_args)

    def _run(self, **kwargs) -> JobResult:
        """
        Creates and saves the datasets
        :return: job results including location of saved datasets
        """
        assert len(self.saved_dataset_paths) > 0, "Either unable to save datasets or no datasets creators were provided"
        return JobResult.from_dict({JobResult.SAVED_DATASET_PATHS: self.saved_dataset_paths})
