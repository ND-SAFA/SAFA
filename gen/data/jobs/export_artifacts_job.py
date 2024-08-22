import os
from typing import Iterable

from gen_common.constants.symbol_constants import EMPTY_STRING, NEW_LINE
from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs
from gen_common.util.file_util import FileUtil


class ExportArtifactsJob(AbstractJob):
    """
    Exports projects artifacts across all levels to newline delimited file.
    """

    def __init__(self, job_args: JobArgs, file_name: str = None, delimiter: str = NEW_LINE):
        """
        Initializes export job with args and with dataset creator to export.
        :param job_args: the arguments for the job
        :param file_name: The name of the file to export to, otherwise dataset name is used.
        :param delimiter: The delimiter to use to separate artifact bodies.
        """
        super().__init__(job_args=job_args, require_data=True)
        assert file_name or job_args.dataset_creator, "Must provide a file name to export to"
        self.file_name = file_name if file_name else job_args.dataset_creator.get_name() + ".txt"
        self.delimiter = delimiter

    def _run(self) -> str:
        """
        Exports artifact bodies as delimited file. Any delimiter found in artifact bodies is removed.
        :return: JobResult containing export path.
        """
        artifacts: Iterable[str] = self.job_args.dataset.artifact_df[StructuredKeys.Artifact.CONTENT.value]
        artifacts = [a.replace(self.delimiter, EMPTY_STRING) for a in artifacts]
        content = self.delimiter.join(artifacts)
        file_path = os.path.join(self.job_args.output_dir, self.file_name)
        FileUtil.write(content, file_path)
        artifact_export_path = os.path.join(self.job_args.output_dir, "artifacts.csv")
        self.job_args.dataset.artifact_df.to_csv(artifact_export_path)

        return file_path
