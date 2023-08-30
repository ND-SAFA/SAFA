from tgen.common.constants.tracing.ranking_constants import RANKING_ARTIFACT_TAG, RANKING_ID_TAG, RANKING_SCORE_TAG
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.supported_prompts.default_ranking_prompts import SCORE_INSTRUCTIONS

DEFAULT_SEARCH_GOAL = "You are a search bar for a software system. " \
                      "Below is a search query followed by the software artifacts in the system. " \
                      "Rank artifacts from most to least related to the search query."
DEFAULT_SEARCH_INSTRUCTIONS = f"{PromptUtil.as_markdown_header('Instructions')}\n"
DEFAULT_SEARCH_QUERY_TAG = "query"
DEFAULT_SEARCH_LINK_TAG = "search-results"

Q1 = (
    "Output your interpretation of the query. "
    f"Use the context of the system to make assumptions about what this might mean. ",
    PromptResponseManager(response_tag=DEFAULT_SEARCH_QUERY_TAG)
)

Q2 = (
    "Rank the selected, related software artifacts from most to least related to query. "
    f"Enclose each artifact in {PromptUtil.create_xml(RANKING_ARTIFACT_TAG)} containing its id within {PromptUtil.create_xml(RANKING_ID_TAG)}. "
    f"Also, within {PromptUtil.create_xml(RANKING_ARTIFACT_TAG)} enclosed in {PromptUtil.create_xml(RANKING_SCORE_TAG)}, {SCORE_INSTRUCTIONS}",
    PromptResponseManager(response_tag={RANKING_ARTIFACT_TAG: [RANKING_ID_TAG, RANKING_SCORE_TAG]},
                          expected_response_type={"id": int, "score": float})
)

DEFAULT_SEARCH_QUESTIONS = [Q1, Q2]
