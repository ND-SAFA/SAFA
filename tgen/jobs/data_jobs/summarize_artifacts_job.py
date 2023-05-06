from typing import Dict

from tgen.constants.open_ai_constants import GENERATION_MODEL_DEFAULT
from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
import pandas as pd

from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.train.args.open_ai_args import OpenAIArgs


class SummarizeArtifactsJob(AbstractJob):
    """
    Handles summarization of artifacts
    """
    TYPE_KEY = "type"

    def __init__(self, artifacts: Dict[Dict], summarizer: Summarizer = None, job_args: JobArgs = None):
        """
        Summarizes a given dataset using the given summarizer
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content and type (e.g. java, py, nl)
        :param summarizer: The summarizer to use to create the summarizations
        :param job_args: The arguments to the job.
        """
        super().__init__(job_args)
        if summarizer is None:
            summarizer = Summarizer(OpenAIManager(OpenAIArgs(model=GENERATION_MODEL_DEFAULT)))
        self.artifacts = artifacts
        self.id2chunker = {id_: SupportedChunker.determine_from_ext(type_) for id_, type_ in artifacts.items()}
        self.artifact_df = pd.DataFrame(artifacts)
        self.summarizer = summarizer

    def _run(self) -> JobResult:
        """
        Performs the summarization of all artifacts and returns the summaries as the new artifact content
        :return: The job result containing all artifacts mapped to their summarized content
        """
        summarized_df = self.summarizer.summarize_dataframe(self.artifact_df, ArtifactKeys.CONTENT.value, self.id2chunker)
        return JobResult({JobResult.ARTIFACTS: summarized_df.to_dict(orient='index')})
