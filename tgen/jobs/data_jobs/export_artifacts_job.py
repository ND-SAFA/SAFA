import os
from typing import Iterable

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.util.file_util import FileUtil


class ExportArtifactsJob(AbstractJob):
    """
    Exports projects artifacts across all levels to newline delimited file.
    """

    def __init__(self, trace_dataset_creator: TraceDatasetCreator, job_args: JobArgs = None, file_name: str = None,
                 delimiter: str = NEW_LINE):
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

    def _run(self) -> str:
        """
        Exports artifact bodies as delimited file. Any delimiter found in artifact bodies is removed.
        :return: JobResult containing export path.
        """
        trace_dataset = self.trace_dataset_creator.create()
        artifacts: Iterable[str] = trace_dataset.artifact_df[StructuredKeys.Artifact.CONTENT.value]
        artifacts = [a.replace(self.delimiter, "") for a in artifacts]
        content = self.delimiter.join(artifacts)
        file_path = os.path.join(self.job_args.output_dir, self.file_name)
        FileUtil.write(content, file_path)
        artifact_export_path = os.path.join(self.job_args.output_dir, "artifacts.csv")
        trace_dataset.artifact_df.to_csv(artifact_export_path)

        return file_path
