import os
from copy import deepcopy
from typing import Any, Dict, List

import pandas as pd

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.util.file_util import FileUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.summary_jobs.base_summarizer_job import BaseSummarizerJob
from tgen.jobs.summary_jobs.summary_response import SummaryResponse
from tgen.summarizer.summarizer import ARTIFACT_FILE_NAME, Summarizer


class SummarizeArtifactsJob(BaseSummarizerJob):
    """
    Handles summarization of artifacts
    """

    def __init__(self, artifacts: List[Dict] = None, artifact_reader: ArtifactProjectReader = None,
                 project_summary: str = None, export_dir: str = None, do_resummarize_project: bool = True,
                 is_subset: bool = False, job_args: JobArgs = None, trace_file_path: str = None, **kwargs):
        """
        Summarizes a given dataset using the given summarizer
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content
        :param artifact_reader: A reader to read in the artifacts if not provided
        :param project_summary: The summary of the project to use instead of generating a new one
        :param export_dir: The path to save to
        :param is_subset: True if not all of the artifacts are provided
        :param job_args: The arguments to the job.
        """
        self.do_resummarize_project = do_resummarize_project
        self.is_subset = is_subset
        self.trace_df = None if trace_file_path is None else TraceDataFrame(pd.read_csv(trace_file_path))
        project_summary = FileUtil.get_str_or_read(project_summary)
        super().__init__(artifacts=artifacts, artifact_reader=artifact_reader,
                         project_summary=project_summary, export_dir=export_dir, job_args=job_args,
                         do_resummarize_project=do_resummarize_project,
                         **kwargs)

    def _run(self) -> Dict[Any, str]:
        """
        Performs the summarization of all artifacts and returns the summaries as the new artifact content
        :return: The job result containing all artifacts mapped to their summarized content
        """
        args = self.create_summarizer_args()
        use_traces_to_summarize = self.trace_df is not None
        orig_artifact_df = args.dataset.artifact_df
        if use_traces_to_summarize:
            args.dataset = PromptDataset(artifact_df=self._get_artifacts_to_summarize(orig_artifact_df, self.trace_df))

        if self.is_subset and not self.project_summary:
            summary = None
            args.dataset.artifact_df.summarize_content(Summarizer.create_summarizer(args))
        else:
            args.dataset = Summarizer(args).summarize()
            summary = args.dataset.project_summary if self.do_resummarize_project else None

        if use_traces_to_summarize:
            args.dataset.artifact_df = self._convert_artifact_content_back(args.dataset.artifact_df, orig_artifact_df)
            artifact_export_path = os.path.join(args.export_dir, ARTIFACT_FILE_NAME)
            args.dataset.artifact_df.to_csv(artifact_export_path)

        artifacts = args.dataset.artifact_df.to_artifacts()
        return SummaryResponse(summary=summary, artifacts=artifacts)

    @staticmethod
    def _convert_artifact_content_back(new_artifact_df: ArtifactDataFrame, orig_artifact_df: ArtifactDataFrame) -> ArtifactDataFrame:
        """
        Converts the content of the newly summarized artifacts back to the original content (pre-combining source, target content)
        :param new_artifact_df: The newly summarized artifacts
        :param orig_artifact_df: The original artifacts
        :return: The summarized artifacts with the original content
        """
        orig_artifact_df[ArtifactKeys.SUMMARY] = new_artifact_df[ArtifactKeys.SUMMARY]
        return orig_artifact_df

    @staticmethod
    def _get_artifacts_to_summarize(artifact_df: ArtifactDataFrame, trace_df: TraceDataFrame) -> ArtifactDataFrame:
        """
        Combines the content of the source and targets for all trace links and updates the target to have the combined content
        :param artifact_df: The original artifacts
        :param trace_df: The traces between artifacts
        :return: The version of the artifacts to summarize
        """
        artifacts2summarize = deepcopy(artifact_df)
        for i, trace in trace_df.itertuples():
            source = artifact_df.get_artifact(trace[TraceKeys.SOURCE])
            target = artifact_df.get_artifact(trace[TraceKeys.TARGET])
            content = f"{source[ArtifactKeys.CONTENT]}{NEW_LINE}{target[ArtifactKeys.CONTENT]}"
            artifacts2summarize.update_value(column2update=ArtifactKeys.CONTENT, id2update=trace[TraceKeys.TARGET], new_value=content)
        return artifacts2summarize
