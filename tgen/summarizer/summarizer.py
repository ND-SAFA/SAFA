from copy import deepcopy

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.summarizer.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.project_summarizer import ProjectSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs


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
        initial_project_summary = self._create_project_summary(self.args.dataset.artifact_df) \
            if not self.args.project_summary else self.args.project_summary
        artifacts_df = self._resummarize_artifacts(initial_project_summary)
        if self.args.export_dir:
            artifacts_df.to_csv(self.args.export_dir)
        final_project_summary = self._create_project_summary(artifact_df=artifacts_df) \
            if self.args.do_resummarize_project else initial_project_summary
        return PromptDataset(artifact_df=artifacts_df, project_summary=final_project_summary)

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
        summarizer = ArtifactsSummarizer(self.args.llm_manager_for_artifact_summaries,
                                         project_summary=project_summary,
                                         code_summary_type=self.args.code_summary_type)
        artifact_df.summarize_content(summarizer)
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
