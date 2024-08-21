from typing import List, Optional

from gen_common.graph.branches.supported_branches import SupportedBranches
from gen_common.graph.edge import Edge
from gen_common.graph.graph_definition import GraphDefinition
from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.llm_tools.tool import BaseTool
from gen_common.graph.nodes.supported_nodes import SupportedNodes
from pydantic.v1.fields import Field

from gen.health.contradiction.contradiction_result import ContradictionResult

NO_CONTRADICTIONS_RESPONSE = "No contradictions were found."


class IdentifyContradictions(BaseTool):
    """
    Respond with whether a contradiction was found. If a contradiction was found,
    (1) provide an explanation of why you believe it is a contradiction and (2) provide the ids of the conflicting artifacts.
    """
    contradiction_found: bool = Field(description="True if contradiction(s) were found, else False. "
                                                  "If TRUE, all other fields MUST be filled in.")
    explanation: str = Field(description="Explanation of the contradiction found (why is it a contradiction?)",
                             default=None)
    contradicting_ids: List[str] = Field(description="Provide ids of all conflicting IDs.", default_factory=list)

    def update_state(self, state: GraphState) -> None:
        """
        Updates the state with the response information.
        :param state: The state.
        """
        state["generation"] = self.explanation if self.contradiction_found else NO_CONTRADICTIONS_RESPONSE
        state["reference_ids"] = self.contradicting_ids


def convert_output(final_state: GraphState) -> Optional[ContradictionResult]:
    """
    Converts final state to ContradictionsResult.
    :param final_state: Final state of the graph.
    :return: Result of contradiction detection including explanation and all conflicting ids.
    """
    explanation = final_state.get("generation")
    conflicting_ids = final_state.get("reference_ids")
    if not explanation or (explanation != NO_CONTRADICTIONS_RESPONSE and not conflicting_ids):
        return None  # detection failed
    result = ContradictionResult(explanation=explanation, conflicting_ids=conflicting_ids)
    return result


class ContradictionsGraph:
    DEFINITION = GraphDefinition(
        nodes=[
            SupportedNodes.GENERATE,
            SupportedNodes.RETRIEVE,
            SupportedNodes.CONTINUE,
            SupportedNodes.EXPLORE_NEIGHBORS
        ],
        edges=[
            Edge(SupportedNodes.GENERATE, SupportedBranches.DECIDE_NEXT),
            Edge(SupportedNodes.CONTINUE, SupportedNodes.END_COMMAND),
            Edge(SupportedNodes.RETRIEVE, SupportedNodes.GENERATE),
            Edge(SupportedNodes.EXPLORE_NEIGHBORS, SupportedNodes.GENERATE)],
        state_type=GraphState,
        output_converter=convert_output,
        node_args=dict(response_model=IdentifyContradictions, allow_request_assistance=False)
    )
