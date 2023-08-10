from typing import Dict, List

from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import NEW_LINE, EMPTY_STRING, SPACE, COMMA
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys, ArtifactDataFrame
from tgen.data.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.delta.change_type import ChangeType
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.delta.delta_util import get_prediction_output
from tgen.delta.steps.overview_change_summary_step import OverviewChangeSummaryStep
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class ImpactAnalysisStep(OverviewChangeSummaryStep):

    def _run(self, args: DeltaArgs, state: DeltaState) -> None:
        """
        Creates the complete summary of all changes made to the project
        :param args: The arguments for the delta summarizer
        :param state: The current state of the delta summarizer
        :return: None
        """
        logger.log_with_title("STEP 4 - Adding Potential Impact to Summary")
        impact_task_prompt: QuestionnairePrompt = SupportedPrompts.DELTA_IMPACTS.value
        artifacts_df_with_impact = self._create_diff_artifacts_df(state, include_impact=True)
        if not state.impact:
            state.impact = self._get_output(args, state, artifacts_df_with_impact,
                                                impact_task_prompt)[impact_task_prompt.response_manager.response_tag][0]
        state.save(self.get_step_name())
        impact_section = [PromptUtil.format_as_markdown_header("Potential Impact"), state.impact]
        all_sections = state.overview_section + impact_section + state.change_details_section
        state.final_summary = NEW_LINE.join(all_sections)
