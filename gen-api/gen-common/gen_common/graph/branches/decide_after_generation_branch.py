from gen_common.graph.branches.base_branch import BaseBranch
from gen_common.graph.branches.paths.path import Path
from gen_common.graph.branches.paths.path_choices import PathChoices
from gen_common.graph.io.graph_state_vars import GraphStateVars
from gen_common.graph.llm_tools.tool_models import RetrieveAdditionalInformation, ExploreArtifactNeighborhood, AnswerUser
from gen_common.graph.nodes.supported_nodes import SupportedNodes


class DecideAfterGenerationBranch(BaseBranch):

    @property
    def path_choices(self) -> PathChoices:
        """
        Contains all possible paths that can be taken based on the state.
        :return:  All possible paths that can be taken based on the state.
        """
        answered_question = ~ GraphStateVars.GENERATION.is_(None)
        requested_assistance = ~ GraphStateVars.RELEVANT_INFORMATION.is_(None)
        bad_response = GraphStateVars.BLACKLISTED_TOOLS.contains(AnswerUser.__name__)
        finished_generation = answered_question | requested_assistance | bad_response

        stop_retrieval = GraphStateVars.BLACKLISTED_TOOLS.contains(RetrieveAdditionalInformation.__name__)
        stop_explore_neighbors = GraphStateVars.BLACKLISTED_TOOLS.contains(ExploreArtifactNeighborhood.__name__)

        request_context = GraphStateVars.RETRIEVAL_QUERY.exists() & ~stop_retrieval
        request_neighborhood_search = GraphStateVars.SELECTED_ARTIFACT_IDS.exists() & ~stop_explore_neighbors

        choices = PathChoices([Path(condition=finished_generation, action=SupportedNodes.CONTINUE),
                               Path(condition=request_context, action=SupportedNodes.RETRIEVE),
                               Path(condition=request_neighborhood_search, action=SupportedNodes.EXPLORE_NEIGHBORS)],
                              default=SupportedNodes.GENERATE)
        return choices
