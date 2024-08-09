from typing import Dict

from common_resources.graph.io.graph_state_vars import GraphStateVars
from common_resources.llm.prompts.binary_score_prompt import BinaryScorePrompt
from common_resources.llm.prompts.prompt_args import PromptArgs

from common_resources.graph.agents.base_agent import BaseAgent
from common_resources.graph.branches.llm_branch import LLMBranch
from common_resources.graph.nodes.supported_nodes import SupportedNodes


class GradeGenerationBranch(LLMBranch):
    RESPONSE_MAP = {BinaryScorePrompt.YES: SupportedNodes.END_COMMAND,
                    BinaryScorePrompt.NO: SupportedNodes.GENERATE}

    @property
    def response_map(self) -> Dict[str, SupportedNodes]:
        """
        Maps LLM response to node to visit if that response is given.
        :return: Dictionary mapping LLM response to node to visit if that response is given.
        """
        return self.RESPONSE_MAP

    def create_agent(self) -> BaseAgent:
        """
        Gets the agent used to determine whether the generation is grounded in the document and answers question.
        :return: The agent.
        """
        system_prompt = BinaryScorePrompt(yes_descr="means the answer addresses the question AND is grounded in / "
                                                    "supported by the set of facts",
                                          question="You are a grader assessing an LLM generation. "
                                                   "First access if the generation answers the question. "
                                                   "If it does, assess whether it is grounded in "
                                                   "/ supported by a set of retrieved facts.",
                                          response_descr="Answer is grounded in the facts",
                                          prompt_args=PromptArgs(system_prompt=True))
        agent = BaseAgent(system_prompt=system_prompt, state_vars_for_context=[GraphStateVars.DOCUMENTS,
                                                                               GraphStateVars.USER_QUESTION,
                                                                               GraphStateVars.GENERATION],
                          allowed_missing_state_vars={GraphStateVars.DOCUMENTS})
        return agent
