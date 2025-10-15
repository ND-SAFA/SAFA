import os
import uuid
from typing import Dict, Type

from gen_common.util.file_util import FileUtil
from gen.delta.delta_args import DeltaArgs
from gen.delta.delta_state import DeltaState
from gen.delta.steps.impact_analysis_step import ImpactAnalysisStep
from gen.delta.steps.individual_diff_summary_step import IndividualDiffSummaryStep
from gen.delta.steps.overview_change_summary_step import OverviewChangeSummaryStep
from gen_common.pipeline.abstract_pipeline import AbstractPipeline


class DeltaSummarizer(AbstractPipeline[DeltaArgs, DeltaState]):
    """
    Responsible for generating summaries of PR changes
    """
    steps = [
        IndividualDiffSummaryStep,
        OverviewChangeSummaryStep,
        ImpactAnalysisStep]

    def __init__(self, args: DeltaArgs):
        """
        Initializes the summarizer with necessary args information
        :param args: The arguments required for the delta summarizer
        """
        super().__init__(args, DeltaSummarizer.steps)

    def state_class(self) -> Type:
        """
        Gets the class used for the pipeline state.
        :return: the state class
        """
        return DeltaState

    def run(self, **kwargs) -> str:
        """
        Runs the delta summarizer to create a summary of the changes in a PR
        :return: The summary of the changes
        """
        if not self.state.export_dir:
            export_path = os.path.join(self.args.export_dir, str(uuid.uuid4())) if self.args.export_dir else None
            FileUtil.create_dir_safely(export_path)
            self.state.export_dir = export_path

        super().run(**kwargs)
        return self.state.final_summary

    def get_input_output_counts(self) -> Dict[str, int]:
        """
        Gets the number of change diffs
        :return: the number of change diffs
        """
        n_change_diffs = sum([len(diffs) for diffs in self.args.change_type_to_diffs.values()])
        return {"N Change Diffs": n_change_diffs}
