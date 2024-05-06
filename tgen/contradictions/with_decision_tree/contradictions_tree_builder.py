from typing import List, Optional, Dict, Callable

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.list_util import ListUtil
from tgen.common.util.str_util import StrUtil
from tgen.contradictions.common_choices import CommonChoices
from tgen.contradictions.with_decision_tree.contradiction_decision_nodes import SupportedContradictionDecisionNodes
from tgen.contradictions.with_decision_tree.requirement import RequirementConstituent, Requirement
from tgen.decision_tree.nodes.abstract_node import AbstractNode
from tgen.decision_tree.nodes.conditional_node import ConditionalNode
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.tree import Tree


class ContradictionsTreeBuilder:

    def __init__(self):
        """
        Builds the decision tree for requirements contradiction detection.
        """
        self.question_constructors: List[Callable] = [self._compare_vars,
                                                      self._compare_action_effect,
                                                      self._assert_action_contradiction,
                                                      self._assert_condition_exists,
                                                      self._compare_conditions,
                                                      self._compare_states]
        self.nodes: List[Optional[AbstractNode]] = [None for _ in range(len(self.question_constructors))]

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
            self.nodes[question_index] = self.question_constructors[question_index](question_num=question_num)
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
        prompt_vars = {ContradictionsTreeBuilder._create_format_variable_name(variable_base_name, i):
                           getattr(requirements[i], f"get_{variable_base_name}")(**kwargs) for i in range(len(requirements))}
        prompt_vars = {k: (v if v else EMPTY_STRING) for k, v in prompt_vars.items()}
        return prompt_vars

    def _compare_vars(self, question_num: int) -> LLMNode:
        """
        Constructs question 1.
        :param question_num: The current question number.
        :return: Question 1.
        """
        q1 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="Are the words \"{}\" similar to words \"{}\"?",
            branches={CommonChoices.YES: self.get_question_node(question_num + 1),
                      CommonChoices.NO: SupportedContradictionDecisionNodes.NONE.value},
            constituent_addressed=RequirementConstituent.VARIABLE,
            constituent=RequirementConstituent.EFFECT,
            pre_check_constituent=True)
        return q1

    def _compare_action_effect(self, question_num: int) -> LLMNode:
        """
        Constructs question 3.
        :param question_num: The current question number.
        :return: Question 3.
        """
        q3 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="Are the following sentences similar to each other?:\n- {}\n- {}?",
            branches={CommonChoices.YES: self.get_question_node(question_num + 2),
                      CommonChoices.NO: self.get_question_node(question_num + 1)},
            constituent_addressed=RequirementConstituent.ACTION,
            constituent=RequirementConstituent.EFFECT,
            pre_check_constituent=True)
        return q3

    def _assert_action_contradiction(self, question_num: int) -> LLMNode:
        """
        Constructs question 4.
        :param question_num: The current question number.
        :return: Question 4.
        """
        q4 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="If the two statements were effects of two different formal requirements, "
                     "could they potentially contradict one another?\n- \""
                     "it must {}\"\n- \"it must {}\"",
            branches={CommonChoices.YES: self.get_question_node(question_num + 1),
                      CommonChoices.NO: SupportedContradictionDecisionNodes.NONE.value},
            constituent_addressed=RequirementConstituent.ACTION, constituent=RequirementConstituent.EFFECT)
        return q4

    def _assert_condition_exists(self, question_num: int) -> ConditionalNode:
        """
        Constructs question 5.
        :param question_num: The current question number.
        :return: Question 5.
        """
        q5 = ConditionalNode(description="Do the requirements contain a condition?",
                             branches={CommonChoices.YES: self.get_question_node(question_num + 1),
                                       CommonChoices.NO: SupportedContradictionDecisionNodes.SIMPLEX_CONTRADICTION.value},
                             conditional_statement=lambda requirements: CommonChoices.NO
                             if any([not r.get_condition() for r in requirements]) else CommonChoices.YES)
        return q5

    def _compare_conditions(self, question_num: int) -> LLMNode:
        """
        Constructs question 6.
        :param question_num: The current question number.
        :return: Question 6.
        """
        q6 = ContradictionsTreeBuilder._construct_llm_question_node(
            question="Is the condition \"{}\" equivalent to the condition \"{}\"?",
            branches={CommonChoices.YES: SupportedContradictionDecisionNodes.IDEM_CONTRADICTION.value,
                      CommonChoices.NO: self.get_question_node(question_num + 1)},
            constituent_addressed=RequirementConstituent.CONDITION,
            pre_check_constituent=True)
        return q6

    def _compare_states(self, question_num: int) -> LLMNode:
        """
        Constructs question 7.
        :param question_num: The current question number.
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
                                     constituent_addressed: RequirementConstituent,
                                     pre_check_constituent: bool = False,
                                     **converter_kwargs) -> LLMNode:
        """
        Constructs a node for a question to be answered using the LLM.
        :param question: The question being asked.
        :param branches: Maps potential answers to the question to the next node to visit if that answer is chosen.
        :param constituent_addressed: The part of the requirement being examined (e.g. condition, action...).
        :param converter_kwargs: Additional arguments used when converting the input to prompt variables.
        :param pre_check_constituent: If True, checks if all requirements have the same constituent before continuing.
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
        if pre_check_constituent:
            question = ConditionalNode(f"Check if the {constituent_addressed} are exactly the same",
                                       branches={CommonChoices.YES: question.branches[CommonChoices.YES],
                                                 CommonChoices.NO: question},
                                       conditional_statement=lambda input_: CommonChoices.YES if ListUtil.are_all_items_the_same(
                                           [StrUtil.remove_stop_words(r.lower())
                                            for r in ContradictionsTreeBuilder.convert_input_to_prompt_vars(
                                               input_, variable_base_name=constituent_addressed, **converter_kwargs).values()])
                                       else CommonChoices.NO)
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
