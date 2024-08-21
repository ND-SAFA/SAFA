from typing import List

from pydantic.v1.main import BaseModel, Field

from gen_common.constants.symbol_constants import EMPTY_STRING
from gen_common.graph.agents.base_agent import BaseAgent
from gen_common.graph.branches.conditions.condition import Condition
from gen_common.graph.branches.paths.path import Path
from gen_common.graph.branches.paths.path_selector import PathSelector
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.io.graph_state_vars import GraphStateVars
from gen_common.graph.llm_tools.tool import BaseTool
from gen_common.graph.llm_tools.tool_models import ExploreArtifactNeighborhood, RequestAssistance, RetrieveAdditionalInformation, \
    STOP_TOOL_USE
from gen_common.graph.nodes.abstract_node import AbstractNode
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager
from gen_common.util.dict_util import DictUtil


class AnswerUser(BaseTool):
    """
    Response to the user query.
    """
    answer: str = Field(description="Your response to the question WITHOUT preamble")
    reference_ids: List[str] = Field(description="If documents from the context were used to answer the question, provide their ids.",
                                     default_factory=list)

    def update_state(self, state: GraphState) -> None:
        """
        Updates the state with the response information.
        :param state: The state.
        """
        state["generation"] = self.answer
        state["reference_ids"] = self.reference_ids


class GenerateNode(AbstractNode):
    RESPONSE_TAG = "answer"

    DEFAULT_PROMPT = (
        "You are an assistant for question-answering tasks, working on a software project."
        "\n\n# Project Description\n"
        "This project contains a graph of artifact's, connected by trace links representing different types of relationships. "
        "These artifact's and their relationships will be useful to answering the question and can be accessed "
        "using the available tools. "
        "\n\n# Task\n"
        f"1. Consider whether you can answer the question using your own knowledge or "
        f"any documents provided. "
        "Answer the user's query as accurately and specifically as possible "
        "{}"
        "\n- If you can't answer, use the other tools available to assist you. "
        "Pay attention to what tools have already been used so you do not repeat past steps. "
    )
    ASSISTANCE_ADDITION = (
        "\n- If none of the tools are valuable, or you have exhausted your strategy, and you still do not know the answer, "
        f"use the {RequestAssistance.__name__} tool. ")
    CONTEXT_ADDITION = ("Remember to use the currently retrieved context to answer the question. "
                        "The user does not have access to the context, "
                        "so include any necessary details in your response. ")

    def __init__(self, graph_args: GraphArgs, response_model: BaseTool = AnswerUser, allow_request_assistance: bool = True):
        """
        Performs decision-making and creates responses to user queries.
        :param graph_args: Starting arguments to the graph.
        :param response_model: The final response expected from the model.
        :param allow_request_assistance: If True, allows the LLM to request assistance if it doesnt know the answer.
        """
        self.response_model = response_model
        self.allow_request_assistance = allow_request_assistance
        super().__init__(graph_args)

    def perform_action(self, state: GraphState, run_async: bool = False) -> GraphState:
        """
        Generate answer to user's question.
        :param state: The current graph state.
        :param run_async: If True, runs in async mode else synchronously.
        :return: Generation added to the state.
        """
        response = self.get_agent().respond(state, run_async)
        self._update_state(response, state)
        return state

    def create_agent(self) -> BaseAgent:
        """
        Gets the agent used for the QA.
        :return: The agent.
        """
        tools = self._get_tool_selector()
        system_prompt = PathSelector(Path(condition=~ GraphStateVars.DOCUMENTS,
                                          action=self.DEFAULT_PROMPT.format(EMPTY_STRING)),
                                     Path(action=self.DEFAULT_PROMPT.format(self.CONTEXT_ADDITION)))
        response_manager = JSONResponseManager.from_langgraph_model(
            self.response_model,
            response_instructions_format=f"Respond WITHOUT preamble!!\n{JSONResponseManager.response_instructions_format}")
        agent = BaseAgent(system_prompt=system_prompt,
                          response_manager=response_manager,
                          state_vars_for_context=[GraphStateVars.USER_QUESTION,
                                                  GraphStateVars.ART_REF_IN_QUESTION,
                                                  GraphStateVars.DOCUMENTS,
                                                  GraphStateVars.TOOLS_ALREADY_USED,
                                                  GraphStateVars.CHAT_HISTORY],
                          allowed_missing_state_vars={GraphStateVars.DOCUMENTS,
                                                      GraphStateVars.TOOLS_ALREADY_USED,
                                                      GraphStateVars.ART_REF_IN_QUESTION,
                                                      GraphStateVars.CHAT_HISTORY},
                          tools=tools)
        return agent

    def _get_tool_selector(self) -> PathSelector:
        """
        Gets the selector for choosing a tool based on state.
        :return: The selector for choosing a tool based on state.
        """
        no_context = ~ GraphStateVars.DOCUMENTS
        stop_neighborhood_search = GraphStateVars.SELECTED_ARTIFACT_IDS == STOP_TOOL_USE
        no_traces = Condition((self.graph_args.dataset.trace_dataset, "is", None))
        neighborhood_search_unavailable = no_context | no_traces | stop_neighborhood_search

        stop_retrieval = GraphStateVars.RETRIEVAL_QUERY == STOP_TOOL_USE

        base_tools = [RequestAssistance] if self.allow_request_assistance else []
        tools = PathSelector(
            # All tools should be available
            Path(condition=~ neighborhood_search_unavailable & ~ stop_retrieval,
                 action=[ExploreArtifactNeighborhood, RetrieveAdditionalInformation] + base_tools),

            # Neighborhood search is unavailable
            Path(condition=neighborhood_search_unavailable & ~ stop_retrieval,
                 action=[RetrieveAdditionalInformation] + base_tools),

            # Retrieval is stopped
            Path(condition=~ neighborhood_search_unavailable & stop_retrieval,
                 action=[ExploreArtifactNeighborhood] + base_tools),

            # All tools are unavailable
            Path(action=base_tools))
        return tools

    def _update_state(self, response: BaseModel, state: GraphState) -> None:
        """
        Updates the state based on the response.
        :param response: Response from the model.
        :param state: The current state.
        :return: None (update directly)
        """
        self._clear_previous_state_values(state)
        if isinstance(response, BaseTool):
            response.update_state(state)

        state["tools_already_used"].append(f"{len(state['tools_already_used']) + 1}: {repr(response)}")

    @staticmethod
    def _clear_previous_state_values(state: GraphState) -> None:
        """
        Clears all values from previous generate step so don't confuse next steps.
        :param state: The current state.
        :return: None.
        """
        DictUtil.update_kwarg_values(state, generation=None, reference_ids=None,
                                     retrieval_query=None, selected_artifact_ids=None,
                                     selected_artifact_types=None)
