import os.path
from typing import Any, Dict, List

import pandas as pd

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs


class SummarizeArtifactsJob(AbstractJob):
    """
    Handles summarization of artifacts
    """
    TYPE_KEY = "type"

    def __init__(self, artifacts: List[Dict] = None, artifact_reader: ArtifactProjectReader = None,
                 summarizer: Summarizer = None, project_summary_path: str = None, export_path: str = None, job_args: JobArgs = None,
                 **kwargs):
        """
        Summarizes a given dataset using the given summarizer
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content and type (e.g. java, py, nl)
        :param job_args: The arguments to the job.
        """
        assert artifacts is not None or artifact_reader is not None, "Expected artifacts or artifact reader to be defined."
        assert artifacts is None or artifact_reader is None, "Cannot defined both artifact reader and artifacts."
        if artifact_reader:
            artifact_df = artifact_reader.read_project()
            artifacts = artifact_df.to_artifacts()
        artifacts = [EnumDict(a) for a in artifacts]
        super().__init__(job_args)
        if project_summary_path:
            project_summary = FileUtil.read_file(os.path.expanduser(project_summary_path))
            kwargs["project_summary"] = project_summary
        if summarizer is None:
            summarizer = Summarizer(**kwargs)
        self.artifacts = artifacts
        self.artifact_df = pd.DataFrame(self.artifacts).set_index(ArtifactKeys.ID.value).dropna()
        self.summarizer = summarizer
        self.export_path = export_path

    def _run(self) -> Dict[Any, str]:
        """
        Performs the summarization of all artifacts and returns the summaries as the new artifact content
        :return: The job result containing all artifacts mapped to their summarized content
        """
        self.artifact_df[ArtifactKeys.SUMMARY.value] = self.summarizer.summarize_dataframe(self.artifact_df,
                                                                                           col2summarize=ArtifactKeys.CONTENT.value,
                                                                                           col2use4chunker=ArtifactKeys.ID.value)
        if self.export_path:
            self.artifact_df.to_csv(self.export_path)
        print("\n", self.artifact_df.iloc[0][ArtifactKeys.SUMMARY.value], "\n")
        return self.artifact_df.to_dict(orient='index')
