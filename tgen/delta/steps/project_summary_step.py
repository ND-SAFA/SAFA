from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.summarizer.project_summarizer import ProjectSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs


class ProjectSummaryStep(AbstractPipelineStep[DeltaArgs, DeltaState]):

    def _run(self, args: DeltaArgs, state: DeltaState) -> None:
        """
        Gets the summary of the project
        :param args: The delta summarizer args
        :param state:  The delta summarizer state
        :return: None
        """
        summarizer = ProjectSummarizer(SummarizerArgs(dataset=PromptDataset(trace_dataset=args.dataset)))
        summary = summarizer.summarize()
        state.project_summary = summary
