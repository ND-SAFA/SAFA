from common_resources.graph.branches.base_branch import BaseBranch
from common_resources.graph.branches.paths.path import Path
from common_resources.graph.branches.paths.path_choices import PathChoices
from common_resources.graph.io.graph_state_vars import GraphStateVars
from common_resources.graph.llm_tools.tool_models import STOP_TOOL_USE
from common_resources.graph.nodes.supported_nodes import SupportedNodes


class DecideAfterGenerationBranch(BaseBranch):

    @property
    def path_choices(self) -> PathChoices:
        """
        Contains all possible paths that can be taken based on the state.
        :return:  All possible paths that can be taken based on the state.
        """
        answered_question = ~ GraphStateVars.GENERATION.is_(None)
        requested_assistance = ~ GraphStateVars.RELEVANT_INFORMATION.is_(None)
        finished_generation = answered_question | requested_assistance

        stop_retrieval = GraphStateVars.RETRIEVAL_QUERY == STOP_TOOL_USE
        stop_explore_neighbors = GraphStateVars.SELECTED_ARTIFACT_IDS == STOP_TOOL_USE
        bad_tool_use = stop_retrieval | stop_explore_neighbors

        request_context = GraphStateVars.RETRIEVAL_QUERY.exists()
        request_neighborhood_search = GraphStateVars.SELECTED_ARTIFACT_IDS.exists()

        choices = PathChoices([Path(condition=bad_tool_use, action=SupportedNodes.GENERATE),
                               Path(condition=finished_generation, action=SupportedNodes.CONTINUE),
                               Path(condition=request_context, action=SupportedNodes.RETRIEVE),
                               Path(condition=request_neighborhood_search, action=SupportedNodes.EXPLORE_NEIGHBORS)],
                              default=SupportedNodes.CONTINUE)
        return choices
