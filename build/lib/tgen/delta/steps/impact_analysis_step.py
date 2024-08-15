from common_resources.llm.prompts.questionnaire_prompt import QuestionnairePrompt
from common_resources.tools.constants.symbol_constants import NEW_LINE
from common_resources.tools.util.prompt_util import PromptUtil

from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.delta.steps.overview_change_summary_step import OverviewChangeSummaryStep
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class ImpactAnalysisStep(OverviewChangeSummaryStep):
    IMPACT_TITLE = "Potential Impact"

    def _run(self, args: DeltaArgs, state: DeltaState) -> None:
        """
        Creates the complete summary of all changes made to the project
        :param args: The arguments for the delta summarizer
        :param state: The current state of the delta summarizer
        :return: None
        """
        impact_task_prompt: QuestionnairePrompt = SupportedPrompts.DELTA_IMPACTS.value
        artifact_df_with_impact = self._create_diff_artifact_df(state, include_impact=True)
        if not state.impact:
            state.impact = self._get_output(args, state, artifact_df_with_impact,
                                            impact_task_prompt)[impact_task_prompt.response_manager.response_tag][0]
        state.save(self.get_step_name())
        impact_section = [PromptUtil.as_markdown_header(ImpactAnalysisStep.IMPACT_TITLE),
                          state.impact]
        all_sections = state.overview_section + impact_section + state.change_details_section
        state.final_summary = NEW_LINE.join(all_sections)
