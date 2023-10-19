import os
from copy import deepcopy

from tgen.common.constants.dataset_constants import ARTIFACT_FILE_NAME
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.project.project_summarizer import ProjectSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summary import Summary


class Summarizer:

    def __init__(self, summarizer_args: SummarizerArgs, dataset: PromptDataset):
        """
        Responsiple for creating summaries of projects and artifacts
        :param summarizer_args: Arguments necessary for the summarizer
        """
        self.args = summarizer_args
        self.dataset = dataset

    def summarize(self) -> PromptDataset:
        """
        Summarizes the project and artifacts
        :return: A dataset containing the summarized artifacts and project
        """
        project_summary = self._create_project_summary(self.dataset)
        artifact_df = self.dataset.artifact_df
        if self.args.do_resummarize_artifacts or not artifact_df.is_summarized(code_only=self.args.summarize_code_only):
            artifact_df = self._resummarize_artifacts(self.dataset.artifact_df, project_summary)
            if self.args.do_resummarize_project:
                project_summary = self._create_project_summary(PromptDataset(artifact_df=artifact_df))
        summarized_dataset = deepcopy(self.dataset)
        summarized_dataset.update_artifact_df(artifact_df)
        summarized_dataset.project_summary = project_summary
        return summarized_dataset

    def _resummarize_artifacts(self, orig_artifact_df: ArtifactDataFrame, project_summary: Summary) -> ArtifactDataFrame:
        """
        Resummarizes the artifacts with the project summary
        :param orig_artifact_df: Contains the original artifacts to re-summarize
        :param project_summary: Summary of the project
        :return: The resummarized artifacts
        """
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: orig_artifact_df.index,
                                         ArtifactKeys.CONTENT: orig_artifact_df[ArtifactKeys.CONTENT],
                                         ArtifactKeys.LAYER_ID: orig_artifact_df[ArtifactKeys.LAYER_ID]})
        summarizer = ArtifactsSummarizer(self.args, project_summary=project_summary)
        artifact_df.summarize_content(summarizer, re_summarize=True)
        if self.args.export_dir:
            os.makedirs(self.args.export_dir, exist_ok=True)
            artifact_export_path = os.path.join(self.args.export_dir, ARTIFACT_FILE_NAME)
            artifact_df.to_csv(artifact_export_path)
        return artifact_df

    def _create_project_summary(self, dataset: PromptDataset) -> Summary:
        """
        Creates a project summary from the artifacts provided
        :param dataset: contains artifacts to make the summary from
        :return: The project summary
        """
        args = SummarizerArgs(**vars(self.args))
        return ProjectSummarizer(args, dataset=dataset).summarize()
