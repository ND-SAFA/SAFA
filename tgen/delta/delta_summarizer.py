
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.delta.steps.diff_summary_step import DiffSummaryStep
from tgen.delta.steps.project_summary_step import ProjectSummaryStep
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline


class DeltaSummarizer(AbstractPipeline[DeltaArgs, DeltaState]):
    """
    Responsible for generating summaries of PR changes
    """
    steps = [ProjectSummaryStep,
             DiffSummaryStep]

    def __init__(self, args: DeltaArgs):
        """
        Initializes the summarizer with necessary args information
        :param args: The arguments required for the delta summarizer
        """
        super().__init__(args, DeltaSummarizer.steps)
        self.args = args

    def init_state(self) -> DeltaState:
        """
        Initialized pipeline state.
        :return: the initialized state
        """
        return DeltaState()

    def run(self) -> None:
        """
        Runs the delta summarizer to create a summary of the changes in a PR
        :return: None
        """
        super().run()


