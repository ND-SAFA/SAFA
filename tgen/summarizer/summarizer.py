import os
from copy import deepcopy
from typing import Optional

import pandas as pd

from tgen.common.constants.dataset_constants import ARTIFACT_FILE_NAME
from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.math_util import MathUtil
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
        if FileUtil.safely_check_path_exists(self._get_artifact_save_path()):
            self._load_artifacts_from_file()
        project_summary = self._create_project_summary(self.dataset)
        artifact_df = self.dataset.artifact_df
        self._save_artifact_summaries(artifact_df)
        if self.args.do_resummarize_artifacts or not artifact_df.is_summarized(code_only=self.args.summarize_code_only):
            artifact_df = self._resummarize_artifacts(self.dataset.artifact_df, project_summary)
            if self.args.do_resummarize_project:
                project_summary = self._create_project_summary(PromptDataset(artifact_df=artifact_df),
                                                               reload_existing=False)
        summarized_dataset = deepcopy(self.dataset)
        summarized_dataset.update_artifact_df(artifact_df)
        summarized_dataset.project_summary = project_summary
        return summarized_dataset

    def _load_artifacts_from_file(self) -> None:
        """
        Loads artifact summaries from a file
        :return: None
        """
        loaded_artifact_df = ArtifactDataFrame(pd.read_csv(self._get_artifact_save_path()))
        original_artifacts = set(self.dataset.artifact_df.index)
        added_artifacts = set(loaded_artifact_df.index).difference(original_artifacts)
        loaded_artifact_df.remove_rows(list(added_artifacts))
        for a_id in original_artifacts:
            orig_artifact = self.dataset.artifact_df.get_artifact(a_id)
            loaded_artifact = loaded_artifact_df.get_artifact(a_id)
            if loaded_artifact and orig_artifact[ArtifactKeys.CONTENT] != loaded_artifact[ArtifactKeys.CONTENT]:
                loaded_artifact_df.remove_row(a_id)
            if a_id not in loaded_artifact_df:
                loaded_artifact_df.add_artifact(**orig_artifact)
        self.dataset.update_artifact_df(loaded_artifact_df)
        logger.info(f"Loaded artifact summaries from {self._get_artifact_save_path()}")

    def _resummarize_artifacts(self, orig_artifact_df: ArtifactDataFrame,
                               project_summary: Summary) -> ArtifactDataFrame:
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
        self._save_artifact_summaries(artifact_df)
        return artifact_df

    def _save_artifact_summaries(self, artifact_df: ArtifactDataFrame) -> Optional[str]:
        """
        Saves a checkpoint of the summarized artifacts
        :param artifact_df: The artifact df containing the summarized artifacts
        :return: The export path if successfully exported
        """
        if self.args.export_dir:
            os.makedirs(self.args.export_dir, exist_ok=True)
            artifact_export_path = self._get_artifact_save_path()
            artifact_df.to_csv(artifact_export_path)
            return artifact_export_path

    def _get_artifact_save_path(self) -> str:
        """
        Gets the path to save the summarized artifacts to
        :return: The path to save the summarized artifacts to
        """
        return FileUtil.safely_join_paths(self.args.export_dir, ARTIFACT_FILE_NAME)

    def _create_project_summary(self, dataset: PromptDataset, reload_existing: bool = True) -> Summary:
        """
        Creates a project summary from the artifacts provided
        :param dataset: contains artifacts to make the summary from
        :param reload_existing: If True, reloads an existing project summary if it exists
        :return: The project summary
        """
        args = SummarizerArgs(**vars(self.args))
        return ProjectSummarizer(args, dataset=dataset, reload_existing=reload_existing).summarize()
