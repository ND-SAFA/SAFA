from typing import Type

from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from tgen.pipeline.abstract_pipeline import AbstractPipeline
from common_resources.tools.state_management.state import State
from tgen.summarizer.project.project_summarizer import ProjectSummarizer
from tgen.summarizer.steps.step_combine_project_summaries import StepCombineProjectSummaries
from tgen.summarizer.steps.step_create_artifact_batches import StepCreateArtifactBatches
from tgen.summarizer.steps.step_create_project_summaries import StepCreateProjectSummaries
from tgen.summarizer.steps.step_create_summarized_dataset import StepCreateSummarizedDataset
from tgen.summarizer.steps.step_filter_dataset import StepFilterDataset
from tgen.summarizer.steps.step_resummarize_artifacts import StepResummarizeArtifacts
from tgen.summarizer.steps.step_summarize_artifacts import StepSummarizeArtifacts
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_state import SummarizerState
from tgen.summarizer.summarizer_util import SummarizerUtil


class Summarizer(AbstractPipeline):
    steps = [StepFilterDataset, StepSummarizeArtifacts, StepCreateArtifactBatches, StepCreateProjectSummaries,
             StepCombineProjectSummaries,
             StepResummarizeArtifacts, StepCreateSummarizedDataset]

    def __init__(self, args: SummarizerArgs, dataset: PromptDataset):
        """
        Responsible for creating summaries of projects and artifacts
        :param args: Arguments necessary for the summarizer
        :param dataset: The dataset to summarize.
        """
        self.args = args
        self.dataset = dataset
        if self.args.no_project_summary:
            self.args.project_summary_sections = []
        super().__init__(args, steps=self.steps, skip_summarization=True, log_state_exception=False)

    def summarize(self) -> PromptDataset:
        """
        Summarizes the project and artifacts
        :return: A dataset containing the summarized artifacts and project
        """
        self.state.dataset = self.dataset if self.state.dataset is None else self.state.dataset
        if not SummarizerUtil.needs_project_summary(self.state.dataset.project_summary, self.args) or self.args.no_project_summary:
            if self.args.do_resummarize_artifacts \
                    or not self.state.dataset.artifact_df.is_summarized(code_or_above_limit_only=self.args.summarize_code_only):
                self.steps = [StepSummarizeArtifacts()]
            else:
                self.steps = []
        super().run(log_start=len(self.steps) > 0)
        if not self.state.summarized_dataset:
            self.state.summarized_dataset = self.state.dataset
        if self.state.final_project_summary and self.state.export_dir:
            save_path = ProjectSummarizer.get_save_path(self.state.export_dir, as_json=False)
            self.state.final_project_summary.save(save_path)
        return self.state.summarized_dataset

    def state_class(self) -> Type[State]:
        """
        Gets the state class for the summarizer pipeline
        :return: The state class for the summarizer pipeline
        """
        return SummarizerState
