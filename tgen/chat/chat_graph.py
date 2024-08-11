from typing import Optional, Dict

from common_resources.graph.branches.supported_branches import SupportedBranches
from common_resources.graph.edge import Edge
from common_resources.graph.graph_definition import GraphDefinition
from common_resources.graph.graph_runner import GraphRunner
from common_resources.graph.io.graph_args import GraphArgs
from common_resources.graph.io.graph_state import GraphState
from common_resources.graph.llm_tools.tool_models import RequestAssistance
from common_resources.graph.nodes.generate_node import AnswerUser
from common_resources.graph.nodes.supported_nodes import SupportedNodes
from common_resources.tools.constants.cli_constants import EXIT_COMMAND


class ChatGraph:
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
        state_type=GraphState)

    @staticmethod
    def get_runner() -> GraphRunner:
        """
        Creates the runner for creating the chat graph.
        :return: The runner for the chat graph.
        """
        runner = GraphRunner(ChatGraph.DEFINITION)
        return runner

    @staticmethod
    def run_cli(args: GraphArgs, verbose: bool = False,
                run_continuous: bool = False) -> Dict[str, AnswerUser | RequestAssistance | None]:
        """
        Runs the chat graph based on the user's input.
        :param args: Args to the graph.
        :param verbose: If True, prints the state at each time step.
        :param run_continuous: If True, automatically prompts for next question after completion.
        :return: Dictionary mapping question to answer.
        """
        answer_map = {}
        runner = ChatGraph.get_runner()
        if not args.user_question:
            args.user_question = ChatGraph._get_user_input()
        while args.user_question:
            answer_obj = runner.run(args, verbose)
            if isinstance(answer_obj, AnswerUser):
                print(f"\nAnswer: {answer_obj.answer}\nReferences: {answer_obj.reference_ids}")
            elif isinstance(answer_obj, RequestAssistance):
                print(f"\nUnable to answer question but determined the following:\n {answer_obj.relevant_information_learned}"
                      f"\nRelated: {answer_obj.related_doc_ids}")
            answer_map[args.user_question] = answer_obj
            if run_continuous:
                args.user_question = ChatGraph._get_user_input()
            else:
                args.user_question = None
        return answer_map

    @staticmethod
    def _get_user_input() -> Optional[str]:
        """
        Gets input from the user - either new question or exit command.
        :return: The user's input or None if the user wants to exit.
        """
        message = "Enter a question or type 'exit' to quit."
        user_input = input(message)
        if user_input.lower() == EXIT_COMMAND:
            return
        return user_input
