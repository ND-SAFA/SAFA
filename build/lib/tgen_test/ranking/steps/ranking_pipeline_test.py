from typing import Dict, List

from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.llm.prompts.questionnaire_prompt import QuestionnairePrompt
from common_resources.tools.constants.symbol_constants import NEW_LINE
from common_resources.tools.util.prompt_util import PromptUtil

from tgen.common.constants.ranking_constants import RANKING_ARTIFACT_TAG, RANKING_ID_TAG, RANKING_PARENT_SUMMARY_TAG, RANKING_SCORE_TAG
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.summarizer.summary import Summary
from tgen.testres.test_data_manager import TestDataManager
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.trace_selectors.selection_methods import SupportedSelectionMethod

DEFAULT_PARENT_IDS = ["s4", "s5"]
DEFAULT_CHILDREN_IDS = ["t1", "t6"]
PARENT_ID = "parent_1"
CHILD_ID = "child_1"
SCORE = 4


class RankingPipelineTest:
    @staticmethod
    def create_ranking_structures(parent_ids: List[str] = None, children_ids: List[str] = None, state_kwargs: Dict = None, **kwargs):
        """
        Creates the args and state of a ranking pipeline.
        :param parent_ids: The parent ids to perform ranking for.
        :param children_ids: The children to rank children against.
        :param kwargs: Custom keyword arguments to ranking args.
        :return: Ranking args and state.
        """
        project_reader = TestDataManager.get_project_reader()
        artifact_df, _, _ = project_reader.read_project()

        types_to_trace = ("target_1", "source_1")
        if parent_ids is None:
            parent_ids = list(artifact_df.get_artifacts_by_type(types_to_trace[0]).index)
        if children_ids is None:
            children_ids = list(artifact_df.get_artifacts_by_type(types_to_trace[1]).index)
        if state_kwargs is None:
            state_kwargs = {}

        project_summary = kwargs.pop("project_summary") if "project_summary" in kwargs else None
        project_summary = Summary({k: {"title": k, "chunks": v} for k, v in project_summary.items()}) if project_summary else None

        args = RankingArgs(dataset=PromptDataset(artifact_df=artifact_df, project_summary=project_summary),
                           selection_method=SupportedSelectionMethod.SELECT_BY_THRESHOLD,
                           parent_ids=parent_ids, children_ids=children_ids, types_to_trace=types_to_trace, **kwargs)
        state = RankingState(**state_kwargs, artifact_map=artifact_df.to_map())
        return args, state

    @staticmethod
    def get_response_parts(task_prompt: QuestionnairePrompt):
        explanation_tags = RankingPipelineTest.get_explanation_tags(task_prompt)
        explanation_response = NEW_LINE.join([PromptUtil.create_xml(tag, tag.upper() + '{child_id_exp}') for tag in explanation_tags])
        parent_summary = f"<{RANKING_PARENT_SUMMARY_TAG}>Parent Summary.</{RANKING_PARENT_SUMMARY_TAG}>\n"
        base_response = (
            f"<{RANKING_ARTIFACT_TAG}>"
            f"<{RANKING_ID_TAG}>{'{child_id}'}</{RANKING_ID_TAG}>"
            f"{explanation_response}"
            f"<{RANKING_SCORE_TAG}>{'{score}'}</{RANKING_SCORE_TAG}>"
            f"</{RANKING_ARTIFACT_TAG}>"
        )
        return parent_summary, base_response

    @staticmethod
    def get_explanation_tags(task_prompt=SupportedPrompts.RANKING_QUESTION2.value):
        explanation_tags = [tag for tag in task_prompt.get_all_response_tags() if tag not in {RANKING_PARENT_SUMMARY_TAG,
                                                                                              RANKING_ARTIFACT_TAG,
                                                                                              RANKING_ID_TAG,
                                                                                              RANKING_SCORE_TAG}]
        return explanation_tags

    @staticmethod
    def get_response(score=SCORE, child_id=0, include_parent_summary: bool = True,
                     include_child_id_in_explanation: bool = False, task_prompt=SupportedPrompts.RANKING_QUESTION2.value):
        parent_summary, base_response = RankingPipelineTest.get_response_parts(task_prompt)
        response = parent_summary if include_parent_summary else ''
        child_id_exp = child_id if include_child_id_in_explanation else ''
        return response + base_response.format(score=score, child_id=child_id, child_id_exp=child_id_exp)
