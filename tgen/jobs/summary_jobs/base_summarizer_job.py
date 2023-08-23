import os
from abc import ABC
from typing import List, Dict

from tgen.common.util.file_util import FileUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.summarizer.summarizer_args import SummarizerArgs


class BaseSummarizerJob(AbstractJob, ABC):

    def __init__(self, artifacts: List[Dict] = None, artifact_reader: ArtifactProjectReader = None,
                 project_summary: str = None, job_args: JobArgs = None, **kwargs):
        """
        Responsible for setting up project summary and artifact summarization jobs
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content
        :param artifact_reader: Reads the artifacts to use instead of the dictionary
        :param project_summary: The summary of the project to use instead of generating a new one
        :param job_args: The arguments to the job.
        """
        assert artifacts is not None or artifact_reader is not None, "Expected artifacts or artifact reader to be defined."
        assert artifacts is None or artifact_reader is None, "Cannot defined both artifact reader and artifacts."
        self.artifacts = artifacts
        self.artifact_reader = artifact_reader
        self.project_summary = project_summary
        self.kwargs = kwargs
        super().__init__(job_args)

    def create_summarizer_args(self) -> SummarizerArgs:
        """
        Creates the arguments for the summarizer
        :return: The summarizer args
        """
        artifact_df = self.artifact_reader.read_project() if self.artifact_reader else ArtifactDataFrame(self.artifacts)
        return SummarizerArgs(dataset=PromptDataset(artifact_df=artifact_df), project_summary=self.project_summary, **self.kwargs)
