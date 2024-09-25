import json
from typing import List, Set

from pydantic.v1.main import Field

from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.llm_tools.tool import BaseTool


def get_input_for_context_tool_use(input_value: str | List[str], state: GraphState) -> Set[str] | str | None:
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
    return  # LLM has produced the same tool call multiple times so disable the tool for next time
    # (prevents endless tool calling if the LLM does not get what it wants)


class RetrieveAdditionalInformation(BaseTool):
    """
    Invoking this tool will perform a keyword-based search for artifacts in the project containing those words.
    This is useful if you currently do not have enough context/information to answer the user's question
    and would like to see further information about a set of topics in the project.

    To use this function, translate the user's question into a set of keyword-based search queries.
    Look at the input and try to reason about the underlying semantic intent / meaning.
    Provide the retrieval query as a list of search queries.
    """
    retrieval_query: str | List[str] = Field(description=json.dumps(["word1 word2", "word3 word4"]))

    def update_state(self, state: GraphState) -> None:
        """
        Updates the state with the response information.
        :param state: The state.
        :return: None.
        """
        state["retrieval_query"] = get_input_for_context_tool_use(self.retrieval_query, state)


class ExploreArtifactNeighborhood(BaseTool):
    """
    Invoking this tool will identify artifacts that are linked to any of the artifact(s) from the context.
    This is useful if you would like to see additional context and other types of information surrounding a specific artifact.

    To use this function, select the artifact or artifacts that you would like to see neighbors for.
    All one hop neighbors to the artifacts will be retrieved.
    """
    artifact_ids: str | Set[str] | List[str] = Field(description="The id of the artifact whose neighbors will be retrieved. "
                                                                 "A list of artifact ids can also be provided "
                                                                 "to explore the neighborhood of multiple artifacts.")

    def update_state(self, state: GraphState) -> None:
        """
        Updates the state with the response information.
        :param state: The state.
        :return: None.
        """
        artifact_ids = get_input_for_context_tool_use(self.artifact_ids, state)
        state["selected_artifact_ids"] = artifact_ids


DEFAULT_FAILURE_RESPONSE = "I don't have any information to relevant to the question."


class RequestAssistance(BaseTool):
    """
    Invoke this tool only when you have exhausted all other strategies for answering the user, including using available context,
    other tools, or your own knowledge.

    This tool will return to the user so that they can improve the question as a last resort.
    To help the user, also provide any relevant knowledge you have learned or related documents
    that they might use as a starting place for getting more information.
    """
    relevant_information_learned: str = Field(description="If you learned anything related to the user's question from the context, "
                                                          "(even if it is not the exact answer), summarize this information.",
                                              default="I don't have any information to relevant to the question.")
    related_doc_ids: List[str] = Field(
        description="If documents from the context are at all related to the question (even if the exact answer is not there), "
                    "provide their ids.",
        default_factory=list)

    def update_state(self, state: GraphState) -> None:
        """
        Updates the state with the response information.
        :param state: The state.
        :return: None.
        """
        state["relevant_information_learned"] = self.relevant_information_learned
        state["related_doc_ids"] = self.related_doc_ids


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
