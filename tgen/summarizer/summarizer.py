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
        super().run(run_setup=False)
        self.state: SummarizerState
        return self.state.summarized_dataset

    def state_class(self) -> Type[State]:
        """
        Gets the state class for the summarizer pipeline
        :return: The state class for the summarizer pipeline
        """
        return SummarizerState
