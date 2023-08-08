import os
import uuid

from tgen.common.util.file_util import FileUtil
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

    def init_state(self) -> DeltaState:
        """
        Initialized pipeline state.
        :return: the initialized state
        """
        if self.args.load_dir:
            return DeltaState.load_latest(self.args.load_dir, self.steps)
        return DeltaState()

    def run(self) -> None:
        """
        Runs the delta summarizer to create a summary of the changes in a PR
        :return: None
        """
        if not self.state.export_dir:
            export_path = os.path.join(self.args.export_dir, str(uuid.uuid4())) if self.args.export_dir else None
            FileUtil.create_dir_safely(export_path)
            self.state.export_dir = export_path

        super().run()
