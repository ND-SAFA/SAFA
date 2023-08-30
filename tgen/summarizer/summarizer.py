import os

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.summarizer.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.projects.project_summarizer import ProjectSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs

ARTIFACT_FILE_NAME = "artifacts.csv"


class Summarizer:

    def __init__(self, summarizer_args: SummarizerArgs):
        """
        Responsiple for creating summaries of projects and artifacts
        :param summarizer_args: Arguments necessary for the summarizer
        """
        self.args = summarizer_args

    def summarize(self) -> PromptDataset:
        """
        Summarizes the project and artifacts
        :return: A dataset containing the summarized artifacts and project
        """
        project_summary = self._create_project_summary(self.args.dataset.artifact_df) \
            if not self.args.project_summary else self.args.project_summary

        artifact_df = self.args.dataset.artifact_df
        if self.args.summarize_artifacts:
            artifact_df = self._resummarize_artifacts(project_summary)
            if self.args.do_resummarize_project:
                project_summary = self._create_project_summary(artifact_df=artifact_df)
        return PromptDataset(artifact_df=artifact_df, project_summary=project_summary)

    @staticmethod
    def create_summarizer(args: SummarizerArgs, project_summary: str = None) -> ArtifactsSummarizer:
        """
        Creates a summarizer for the artifacts from the args
        :param args: The summarizer args
        :param project_summary: Optionally provide a summary of the project to use instead of the one in args
        :return: The summarizer for the artifacts
        """
        if not project_summary:
            project_summary = args.project_summary
        summarizer = ArtifactsSummarizer(args.llm_manager_for_artifact_summaries,
                                         project_summary=project_summary,
                                         code_summary_type=args.code_summary_type,
                                         code_or_exceeds_limit_only=args.summarize_code_only)
        return summarizer

    def _resummarize_artifacts(self, project_summary: str) -> ArtifactDataFrame:
        """
        Resummarizes the artifacts with the project summary
        :param project_summary: Summary of the project
        :return: The resummarized artifacts
        """
        orig_artifact_df = self.args.dataset.artifact_df
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: orig_artifact_df.index,
                                         ArtifactKeys.CONTENT: orig_artifact_df[ArtifactKeys.CONTENT],
                                         ArtifactKeys.LAYER_ID: orig_artifact_df[ArtifactKeys.LAYER_ID]})
        summarizer = self.create_summarizer(self.args, project_summary)
        artifact_df.summarize_content(summarizer)
        if self.args.export_dir:
            artifact_export_path = os.path.join(self.args.export_dir, ARTIFACT_FILE_NAME)
            artifact_df.to_csv(artifact_export_path)
        return artifact_df

    def _create_project_summary(self, artifact_df: ArtifactDataFrame = None) -> str:
        """
        Creates a project summary from the artifacts provided
        :param artifact_df: Artifacts to make the summary from
        :return: The project summary
        """
        args = SummarizerArgs(**vars(self.args))
        if artifact_df is not None:
            args.dataset = PromptDataset(artifact_df=artifact_df)
        return ProjectSummarizer(args).summarize()
