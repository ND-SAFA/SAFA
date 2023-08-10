from typing import Any, Dict, List

import pandas as pd

from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs


class SummarizeArtifactsJob(AbstractJob):
    """
    Handles summarization of artifacts
    """
    TYPE_KEY = "type"

    def __init__(self, artifacts: List[Dict], summarizer: Summarizer = None, job_args: JobArgs = None, **kwargs):
        """
        Summarizes a given dataset using the given summarizer
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content and type (e.g. java, py, nl)
        :param job_args: The arguments to the job.
        """
        artifacts = [EnumDict(a) for a in artifacts]
        super().__init__(job_args)
        if summarizer is None:
            summarizer = Summarizer(**kwargs)
        self.artifacts = artifacts
        self.artifact_df = pd.DataFrame(self.artifacts).set_index(ArtifactKeys.ID.value)
        self.summarizer = summarizer

    def _run(self) -> Dict[Any, str]:
        """
        Performs the summarization of all artifacts and returns the summaries as the new artifact content
        :return: The job result containing all artifacts mapped to their summarized content
        """
        summarized_df = self.summarizer.summarize_dataframe(self.artifact_df, ArtifactKeys.CONTENT.value, self.TYPE_KEY)
        return summarized_df.to_dict(orient='index')
