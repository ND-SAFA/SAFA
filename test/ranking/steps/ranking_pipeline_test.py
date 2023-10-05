from typing import Dict, List

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.tracing.ranking_constants import RANKING_PARENT_SUMMARY_TAG, RANKING_ARTIFACT_TAG, RANKING_ID_TAG, \
    RANKING_SCORE_TAG
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.testres.test_data_manager import TestDataManager
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState

DEFAULT_PARENT_IDS = ["s4", "s5"]
DEFAULT_CHILDREN_IDS = ["t1", "t6"]
PARENT_ID = "parent_1"
CHILD_ID = "child_1"
SCORE = 4
TASK_PROMPT: QuestionnairePrompt = SupportedPrompts.RANKING_QUESTION2.value
EXPLANATION_TAG = [tag for tag in TASK_PROMPT.response_manager.get_all_tag_ids() if tag not in {RANKING_PARENT_SUMMARY_TAG,
                                                                                                RANKING_ARTIFACT_TAG,
                                                                                                RANKING_ID_TAG,
                                                                                                RANKING_SCORE_TAG}]
EXPLANTION_RESPONSE = NEW_LINE.join([PromptUtil.create_xml(tag, tag.upper()) for tag in EXPLANATION_TAG])
PARENT_SUMMARY = f"<{RANKING_PARENT_SUMMARY_TAG}>Parent Summary.</{RANKING_PARENT_SUMMARY_TAG}>\n"
TEST_RESPONSE = (
    f"<{RANKING_ARTIFACT_TAG}>"
    f"<{RANKING_ID_TAG}>{'{child_id}'}</{RANKING_ID_TAG}>"
    f"{EXPLANTION_RESPONSE}"
    f"<{RANKING_SCORE_TAG}>{'{score}'}</{RANKING_SCORE_TAG}>"
    f"</{RANKING_ARTIFACT_TAG}>"
)


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
        if parent_ids is None:
            parent_ids = []
        if children_ids is None:
            children_ids = []
        if state_kwargs is None:
            state_kwargs = {}
        project_reader = TestDataManager.get_project_reader()
        artifact_df, _, _ = project_reader.read_project()
        project_summary = kwargs.pop("project_summary") if "project_summary" in kwargs else None

        args = RankingArgs(dataset=PromptDataset(artifact_df=artifact_df, project_summary=project_summary),
                           parent_ids=parent_ids, children_ids=children_ids, **kwargs)
        state = RankingState(**state_kwargs)
        return args, state

    @staticmethod
    def get_response(score=SCORE, child_id=0, include_parent_summary: bool = True):
        response = PARENT_SUMMARY if include_parent_summary else ''
        return response + TEST_RESPONSE.format(score=score, child_id=child_id)