from ast import Str
from typing import List, Set

from pydantic.v1.main import BaseModel, Field

from common_resources.graph.agents.base_agent import BaseAgent
from common_resources.graph.branches.conditions.condition import Condition
from common_resources.graph.branches.paths.path import Path
from common_resources.graph.branches.paths.path_selector import PathSelector
from common_resources.graph.io.graph_state import GraphState
from common_resources.graph.io.graph_state_vars import GraphStateVars
from common_resources.graph.llm_tools.tool_models import ExploreArtifactNeighborhood, RetrieveAdditionalInformation, STOP_TOOL_USE, \
    RequestAssistance
from common_resources.graph.nodes.abstract_node import AbstractNode
from common_resources.llm.response_managers.json_response_manager import JSONResponseManager
from common_resources.tools.constants.symbol_constants import EMPTY_STRING
from common_resources.tools.util.dict_util import DictUtil


class AnswerUser(BaseModel):
    """
    Response to the user query.
    """
    answer: str = Field(description="Your response to the question WITHOUT preamble")
    reference_ids: List[str] = Field(description="If documents from the context were used to answer the question, provide their ids.",
                                     default_factory=list)


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
        "\n- If none of the tools are valuable, or you have exhausted your strategy, and you still do not know the answer, "
        f"use the {RequestAssistance.__name__} tool. "
    )
    CONTEXT_ADDITION = "Remember to use the currently retrieved context to answer the question. " \
                       "The user does not have access to the context, " \
                       "so include any necessary details in your response. "

    def perform_action(self, state: GraphState):
        """
        Generate answer to user's question.
        :param state: The current graph state.
        :return: Generation added to the state.
        """
        response = self.get_agent().respond(state)
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
            AnswerUser,
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
        tools = PathSelector(
            # All tools should be available
            Path(condition=~ neighborhood_search_unavailable & ~ stop_retrieval,
                 action=[ExploreArtifactNeighborhood, RetrieveAdditionalInformation, RequestAssistance]),

            # Neighborhood search is unavailable
            Path(condition=neighborhood_search_unavailable & ~ stop_retrieval,
                 action=[RetrieveAdditionalInformation, RequestAssistance]),

            # Retrieval is stopped
            Path(condition=~ neighborhood_search_unavailable & stop_retrieval,
                 action=[ExploreArtifactNeighborhood, RequestAssistance]),

            # All tools are unavailable
            Path(action=[RequestAssistance]))
        return tools

    def _update_state(self, response: BaseModel, state: GraphState) -> None:
        """
        Updates the state based on the response.
        :param response: Response from the model.
        :param state: The current state.
        :return: None (update directly)
        """
        self._clear_previous_state_values(state)
        if isinstance(response, AnswerUser):
            state["generation"] = response.answer
            state["reference_ids"] = response.reference_ids
        elif isinstance(response, RetrieveAdditionalInformation):
            state["retrieval_query"] = self._get_input_for_context_tool_use(response.retrieval_query, state)
        elif isinstance(response, ExploreArtifactNeighborhood):
            artifact_ids = self._get_input_for_context_tool_use(response.artifact_ids, state)
            state["selected_artifact_ids"] = artifact_ids
        elif isinstance(response, RequestAssistance):
            state["relevant_information_learned"] = response.relevant_information_learned
            state["related_doc_ids"] = response.related_doc_ids
        state["tools_already_used"].append(f"{len(state['tools_already_used']) + 1}: {repr(response)}")

    @staticmethod
    def _get_input_for_context_tool_use(input_value: Str | List[str], state: GraphState) -> Set[str] | str:
        """
        Checks if the model is using a tool with new input - if so the input is returned as a set else the stop command is given.
        :param input_value: The original input value.
        :param state: The current state.
        :return: Any new input values returned as a set else the stop command is given.
        """
        input_value = {input_value} if isinstance(input_value, str) else set(input_value)
        new_input = input_value.difference(state.get("documents", {}))
        if new_input:
            return new_input
        return STOP_TOOL_USE  # LLM has produced the same tool call multiple times so disable the tool for next time
        # (prevents endless tool calling if the LLM does not get what it wants)

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
