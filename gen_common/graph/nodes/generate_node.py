from typing import List

from pydantic.v1.main import BaseModel

from gen_common.constants.symbol_constants import NEW_LINE
from gen_common.graph.agents.base_agent import BaseAgent
from gen_common.graph.branches.conditions.condition import Condition
from gen_common.graph.branches.paths.path import Path
from gen_common.graph.branches.paths.path_selector import PathSelector
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.io.graph_state_vars import GraphStateVars
from gen_common.graph.llm_tools.tool import BaseTool
from gen_common.graph.llm_tools.tool_models import AnswerUser, ExploreArtifactNeighborhood, RequestAssistance, \
    RetrieveAdditionalInformation
from gen_common.graph.nodes.abstract_node import AbstractNode
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager
from gen_common.util.dict_util import DictUtil


class PromptComponents:
    ROLE_DESCRIPTION = "You are an assistant for {} task, working on a software project."
    PROJ_DESCRIPTION = ("\n# Project Description\n"
                        "This project contains a graph of artifact's, "
                        "connected by trace links representing different types of relationships. "
                        "These artifact's and their relationships will be useful to answering the question and can be accessed "
                        "using the available tools. ")
    BASE_TASK = ("\n# Task\n"
                 f"Consider whether you can answer the question using your own knowledge or "
                 f"any documents provided. "
                 "Answer the user's query as accurately and specifically as possible ")
    TOOL_USE = ("Note: If you can't answer, use the other tools available to assist you. "
                "Pay attention to what tools have already been used so you do not repeat past steps. ")
    DONT_KNOW_OPTION = (
        "- If none of the tools are valuable, or you have exhausted your strategy, and you still do not know the answer, "
        f"use the {RequestAssistance.__name__} tool. ")
    CONTEXT_PROVIDED = ("- Remember to use the currently retrieved context to answer the question. "
                        "The user does not have access to the context, "
                        "so include any necessary details in your response. ")


class GenerateNode(AbstractNode):

    def __init__(self, graph_args: GraphArgs, response_model: BaseTool = AnswerUser,
                 allow_request_assistance: bool = True, prompt_components: List[str] = None):
        """
        Performs decision-making and creates responses to user queries.
        :param graph_args: Starting arguments to the graph.
        :param response_model: The final response expected from the model.
        :param allow_request_assistance: If True, allows the LLM to request assistance if it doesnt know the answer.
        :param prompt_components: List of prompt elements that will be joined by newlines to create the system prompt.
        """
        prompt_components = self._get_default_system_prompt() if not prompt_components else prompt_components
        if allow_request_assistance:
            prompt_components += PromptComponents.DONT_KNOW_OPTION
        self.system_prompt = self._join_prompt_components(*prompt_components)
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
                                          action=self.system_prompt),
                                     Path(action=self._join_prompt_components(self.system_prompt, PromptComponents.CONTEXT_PROVIDED)))
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
        stop_neighborhood_search = GraphStateVars.BLACKLISTED_TOOLS.contains(ExploreArtifactNeighborhood.__name__)
        no_traces = Condition((self.graph_args.dataset.trace_dataset, "is", None))
        neighborhood_search_unavailable = no_context | no_traces | stop_neighborhood_search

        stop_retrieval = GraphStateVars.BLACKLISTED_TOOLS.contains(RetrieveAdditionalInformation.__name__)

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

    @staticmethod
    def _join_prompt_components(*prompt_components: str) -> str:
        """
        Joins the prompt components into a single prompt.
        :param prompt_components: The components of the prompt.
        :return: Single prompt, with all components joined by newline
        """
        return f"{NEW_LINE}{NEW_LINE}".join(prompt_components)

    @staticmethod
    def _get_default_system_prompt() -> List[str]:
        """
        Default prompt for the question-answering task.
        :return: List of prompt components for the default task.
        """
        default_prompt = [PromptComponents.ROLE_DESCRIPTION.format("question-answering"),
                          PromptComponents.PROJ_DESCRIPTION,
                          PromptComponents.BASE_TASK,
                          PromptComponents.TOOL_USE]
        return default_prompt

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

        repr_response = repr(response)
        if repr_response in state["tools_already_used"]:
            state["backlisted_tools"].add(response.__class__.__name__)
        state["tools_already_used"].append(repr_response)

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
