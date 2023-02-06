import os
from typing import Iterable

from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.keys.structure_keys import StructuredKeys
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from util.file_util import FileUtil


class ExportArtifactsJob(AbstractJob):
    """
    Exports projects artifacts across all levels to newline delimited file.
    """

    def __init__(self, job_args: JobArgs, trace_dataset_creator: TraceDatasetCreator, file_name: str = None, delimiter: str = "\n"):
        """
        Initializes export job with args and with dataset creator to export.
        :param job_args: the arguments for the job
        :param trace_dataset_creator: The trace dataset containing artifacts to export.
        :param file_name: The name of the file to export to, otherwise dataset name is used.
        :param delimiter: The delimiter to use to separate artifact bodies.
        """
        super().__init__(job_args=job_args)
        self.trace_dataset_creator = trace_dataset_creator
        self.file_name = file_name if file_name else trace_dataset_creator.get_name() + ".txt"
        self.delimiter = delimiter

    def _run(self) -> JobResult:
        """
        Exports artifact bodies as delimited file. Any delimiter found in artifact bodies is removed.
        :return: JobResult containing export path.
        """
        self.trace_dataset_creator.create()
        artifacts: Iterable[str] = self.trace_dataset_creator.artifact_df[StructuredKeys.Artifact.BODY]
        artifacts = [a.replace(self.delimiter, "") for a in artifacts]
        content = self.delimiter.join(artifacts)
        file_path = os.path.join(self.job_args.output_dir, self.file_name)
        FileUtil.write(content, file_path)
        return JobResult.from_dict({JobResult.EXPORT_PATH: file_path})
