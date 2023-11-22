from typing import Type

from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.pipeline.abstract_pipeline import AbstractPipeline
from tgen.pipeline.abstract_pipeline_step import StateType
from tgen.pipeline.state import State
from tgen.summarizer.steps.step_cluster_artifacts import StepClusterArtifacts
from tgen.summarizer.steps.step_combine_project_summaries import StepCombineProjectSummaries
from tgen.summarizer.steps.step_create_project_summaries import StepCreateProjectSummaries
from tgen.summarizer.steps.step_create_summarized_dataset import StepCreateSummarizedDataset
from tgen.summarizer.steps.step_resummarize_artifacts import StepResummarizeArtifacts
from tgen.summarizer.steps.step_summarize_artifacts import StepSummarizeArtifacts
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_state import SummarizerState
from tgen.summarizer.summarizer_util import SummarizerUtil


class Summarizer(AbstractPipeline):
    steps = [StepSummarizeArtifacts, StepClusterArtifacts, StepCreateProjectSummaries, StepCombineProjectSummaries,
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
        super().__init__(args, steps=self.steps, skip_summarization=True)

    def summarize(self) -> PromptDataset:
        """
        Summarizes the project and artifacts
        :return: A dataset containing the summarized artifacts and project
        """
        self.state.dataset = self.dataset
        if not SummarizerUtil.needs_project_summary(self.state.dataset.project_summary, self.args) or self.args.no_project_summary:
            if self.args.do_resummarize_artifacts \
                    or not self.state.dataset.artifact_df.is_summarized(code_only=self.args.summarize_code_only):
                self.steps = [StepSummarizeArtifacts()]
            else:
                self.steps = []
        super().run(run_setup=False)
        if not self.state.summarized_dataset:
            self.state.summarized_dataset = self.state.dataset
        return self.state.summarized_dataset

    def state_class(self) -> Type[State]:
        """
        Gets the state class for the summarizer pipeline
        :return: The state class for the summarizer pipeline
        """
        return SummarizerState
