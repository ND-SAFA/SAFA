from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_summarizer import DeltaSummarizer
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs


class DeltaSummarizerJob(AbstractJob):

    def __init__(self, delta_args: DeltaArgs, job_args: JobArgs = None):
        """
        :param delta_args: The args to use for the delta summarizer
        :param job_args: job args used to configure job params.
        """
        self.delta_args = delta_args
        self.delta_summarizer = DeltaSummarizer(self.delta_args)
        super().__init__(job_args)

    def _run(self) -> None:
        """
        Runs the delta summarizer
        :return: The result of the job
        """
        self.delta_summarizer.run()
        return None
