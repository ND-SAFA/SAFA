import os
import uuid

from tgen.common.util.file_util import FileUtil
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.delta.steps.overview_change_summary_step import OverviewChangeSummaryStep
from tgen.delta.steps.impact_analysis_step import ImpactAnalysisStep
from tgen.delta.steps.individual_diff_summary_step import IndividualDiffSummaryStep
from tgen.delta.steps.project_summary_step import ProjectSummaryStep
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline


class DeltaSummarizer(AbstractPipeline[DeltaArgs, DeltaState]):
    """
    Responsible for generating summaries of PR changes
    """
    steps = [ProjectSummaryStep,
             IndividualDiffSummaryStep,
             OverviewChangeSummaryStep,
             ImpactAnalysisStep]

    def __init__(self, args: DeltaArgs):
        """
        Initializes the summarizer with necessary args information
        :param args: The arguments required for the delta summarizer
        """
        super().__init__(args, DeltaSummarizer.steps)

    def init_state(self) -> DeltaState:
        """
        Initialized pipeline state.
        :return: the initialized state
        """
        if self.args.load_dir:
            return DeltaState.load_latest(self.args.load_dir, self.steps)
        return DeltaState()

    def run(self) -> str:
        """
        Runs the delta summarizer to create a summary of the changes in a PR
        :return: The summary of the changes
        """
        if not self.state.export_dir:
            export_path = os.path.join(self.args.export_dir, str(uuid.uuid4())) if self.args.export_dir else None
            FileUtil.create_dir_safely(export_path)
            self.state.export_dir = export_path

        super().run()
        return self.state.final_summary
