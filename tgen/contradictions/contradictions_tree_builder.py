from typing import List, Optional, Dict

from tgen.common.util.str_util import StrUtil
from tgen.contradictions.common_choices import CommonChoices
from tgen.contradictions.contradiction_decision_nodes import SupportedContradictionDecisionNodes
from tgen.contradictions.requirement import RequirementConstituent, Requirement
from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.decision_tree.nodes.conditional_node import ConditionalNode
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.tree import Tree


class ContradictionsTreeBuilder:
    N_QUESTIONS = 7

    def __init__(self):
        """
        Builds the decision tree for requirements contradiction detection.
        """
        self.nodes: List[Optional[AbstractNode]] = [None for _ in range(self.N_QUESTIONS)]

    def build_tree(self) -> Tree:
        """
        Builds the tree for requirements contradiction detection.
        :return: The tree for requirements contradiction detection.
        """
        return Tree(starting_node=self.get_question_node(1))

    def get_question_node(self, question_num: int) -> AbstractNode:
        """
        Gets a question node for the tree.
        :param question_num: The number of the question to get.
        :return: The node for that question.
        """
        question_index = question_num - 1
        if self.nodes[question_index] is None:
            self.nodes[question_index] = getattr(self, f"_construct_q{question_num}")()
        return self.nodes[question_index]

    @staticmethod
    def convert_input_to_prompt_vars(requirements: List[Requirement], variable_base_name: str, **kwargs) -> Dict[str, str]:
        """
        Converts the node's input into variables to use in the prompt for the LLM.
        :param requirements: The list of requirements being assessed at the given node.
        :param variable_base_name: The base name of the variable in the prompt.
        :param kwargs: Any additional arguments for getting the variable value from the requirement.
        :return: Format variables for the prompt in a dictionary mapping variable name to its value.
        """
        return {ContradictionsTreeBuilder._create_format_variable_name(variable_base_name, i):
                    getattr(requirements[i], f"get_{variable_base_name}")(**kwargs) for i in range(len(requirements))}

    def _construct_q1(self) -> LLMNode:
        """
        Constructs question 1.
        :return: Question 1.
        """
        q2 = self.get_question_node(2)
        q1 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="Are the words \"{variable1}\" similar to words \"{}\"?",
            branches={CommonChoices.YES: q2, CommonChoices.NO: SupportedContradictionDecisionNodes.NONE.value},
            constituent_addressed=RequirementConstituent.VARIABLE,
            constituent=RequirementConstituent.EFFECT)
        return q1

    def _construct_q2(self) -> LLMNode:
        """
        Constructs question 2.
        :return: Question 2.
        """
        q3 = self.get_question_node(3)
        q5 = self.get_question_node(5)
        q2 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="Are the following sentences similar to each other?:\n- {}\n- {}?",
            branches={CommonChoices.YES: q5, CommonChoices.NO: q3},
            constituent_addressed=RequirementConstituent.ACTION,
            constituent=RequirementConstituent.EFFECT)
        return q2

    def _construct_q3(self) -> LLMNode:
        """
        Constructs question 3.
        :return: Question 3.
        """
        q4 = self.get_question_node(4)
        q5 = self.get_question_node(5)
        q3 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="Are the following sentences similar to each other?:\n- {}\n- {}?",
            branches={CommonChoices.YES: q5, CommonChoices.NO: q4},
            constituent_addressed=RequirementConstituent.ACTION,
            constituent=RequirementConstituent.EFFECT)
        return q3

    def _construct_q4(self) -> LLMNode:
        """
        Constructs question 4.
        :return: Question 4.
        """
        q5 = self.get_question_node(5)
        q4 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="Could the following statements potentially contradict each other?\n- \""
                     "it must {}\"\n- \"it must {}\"",
            branches={CommonChoices.YES: q5, CommonChoices.NO: SupportedContradictionDecisionNodes.NONE.value},
            constituent_addressed=RequirementConstituent.ACTION, constituent=RequirementConstituent.EFFECT)
        return q4

    def _construct_q5(self) -> ConditionalNode:
        """
        Constructs question 5.
        :return: Question 5.
        """
        q6 = self.get_question_node(6)
        q5 = ConditionalNode(description="Does the following sentence contain a condition: {condition}.",
                             branches={CommonChoices.YES: q6,
                                       CommonChoices.NO: SupportedContradictionDecisionNodes.SIMPLEX_CONTRADICTION.value},
                             conditional_statement=lambda requirements: CommonChoices.NO
                             if any([not r.get_condition() for r in requirements]) else CommonChoices.YES)
        return q5

    def _construct_q6(self) -> LLMNode:
        """
        Constructs question 6.
        :return: Question 6.
        """
        q7 = self.get_question_node(7)
        q6 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="Is the condition \"{}\" equivalent to the condition \"{}\"?",
            branches={CommonChoices.YES: q7,
                      CommonChoices.NO: SupportedContradictionDecisionNodes.IDEM_CONTRADICTION.value},
            constituent_addressed=RequirementConstituent.CONDITION)
        return q6

    def _construct_q7(self) -> LLMNode:
        """
        Constructs question 7.
        :return: Question 7.
        """
        q7 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="Can the following states occur at the same time? \n1. {} \n2. {}",
            branches={CommonChoices.YES: SupportedContradictionDecisionNodes.ALIUS_CONTRADICTION.value,
                      CommonChoices.NO: SupportedContradictionDecisionNodes.NONE.value},
            constituent_addressed=RequirementConstituent.CONDITION)
        return q7

    @staticmethod
    def _construct_llm_question_node(question: str, branches: Dict[str, AbstractNode],
                                     constituent_addressed: RequirementConstituent, **converter_kwargs) -> LLMNode:
        """
        Constructs a node for a question to be answered using the LLM.
        :param question: The question being asked.
        :param branches: Maps potential answers to the question to the next node to visit if that answer is chosen.
        :param constituent_addressed: The part of the requirement being examined (e.g. condition, action...).
        :param converter_kwargs: Additional arguments used when converting the input to prompt variables.
        :return: A node for a question to be answered using the LLM.
        """
        constituent_addressed = constituent_addressed.value
        n_variables = question.count(StrUtil.get_format_symbol())
        for i in range(n_variables):
            format_variable_name = ContradictionsTreeBuilder._create_format_variable_name(constituent_addressed, i)
            question = StrUtil.fill_with_format_variable_name(question, format_variable_name, count=1)
        question = LLMNode(description=question,
                           branches=branches,
                           input_variable_converter=lambda input_:
                           ContradictionsTreeBuilder.convert_input_to_prompt_vars(input_, variable_base_name=constituent_addressed,
                                                                                  **converter_kwargs))
        return question

    @staticmethod
    def _create_format_variable_name(variable_base_name: str, variable_num: int) -> str:
        """
        Creates the name of the format using the variable base name and its in index.
        :param variable_base_name: The base variable name without including its number.
        :param variable_num: The variable number starting with 0.
        :return: The name of the format using the variable base name and its in index.
        """
        return f"{variable_base_name}{variable_num}"
