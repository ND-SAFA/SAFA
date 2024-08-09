import operator
from typing import Any, Tuple

from common_resources.graph.branches.conditions.operators import OPERATORS
from common_resources.graph.io.graph_state import GraphState
from common_resources.tools.constants.symbol_constants import SPACE


class Condition:

    def __init__(self, terms: Tuple[Any, ...], default: bool = None):
        """
        Compares state value with comparison value based on a relational operator.
        :param terms: Contains the variables and operator for comparison, including names of the state var to compare.
        :param default: If comparison fails, default will be returned.
        """
        self.terms = terms
        self.default = default

    def check(self, state: GraphState = None) -> bool:
        """
        Checks if the condition is True or False based on current state.
        :param state: Current state dictionary.
        :return: True if condition is True, else False.
        """
        try:
            match self.terms:
                case (operator, x) if operator in OPERATORS:
                    return self._evaluate(x=x, operator=operator, state=state)
                case _:
                    return self._evaluate(*self.terms, state=state)

        except Exception as e:
            if self.default is not None:
                return self.default
            raise e

    @staticmethod
    def _evaluate(x: Any, operator: str, y: Any = None, state: GraphState = None) -> bool:
        """
        Evaluates the result of x operator y.
        :param x: First term.
        :param operator: Second term.
        :param y: Second term.
        :param state:
        :return:
        """
        assert operator in OPERATORS, f"Unknown operator {operator}"
        x = Condition._evaluate_term(x, state)
        if not Condition._eval_second_term(operator, x):
            return x
        y = Condition._evaluate_term(y, state)
        result = OPERATORS.get(operator)(x, y)
        return result

    @staticmethod
    def _eval_second_term(operator: str, first_term: bool) -> bool:
        """
        If the operator is "and" or "or", then the second term does not necessarily need to be evaluated depending on the first.
        :param operator: The operator name.
        :param first_term: The value of the first term.
        :return: True if the second term needs to be evaluated, else False.
        """
        match operator:
            case "or":
                return first_term is False
            case "and":
                return first_term is True
            case _:
                return True

    @staticmethod
    def _evaluate_term(term: Any, state: GraphState) -> Any:
        """
        Gets the value of the state var if it exists.
        :param term: The name of hte variable.
        :param state: The state.
        :return: The value of the state var if it exists else var name.
        """
        from common_resources.graph.io.state_var import StateVar
        if isinstance(term, Condition):
            return term.check(state)
        if isinstance(term, StateVar):
            return term.get_value(state)
        return term

    def __call__(self, *args, **kwargs):
        """
        Checks conditional.
        :param args: Arguments to the condition.
        :param kwargs: Arguments to the condition.
        :return: Result of condition based on args.
        """
        try:
            return self.check(*args, **kwargs)
        except Exception as e:
            if self.default is None:
                raise e
            return self.default

    def __or__(self, b: "Condition") -> "Condition":
        """
        Determines if either condition a OR b is True.
        :param b: The second condition.
        :return: True if either condition a or b is True.
        """
        return Condition((self, "or", b))

    def __xor__(self, a: "Condition") -> "Condition":
        """
        Determines if either condition a OR b is True.
        :param a: The first condition.
        :return: True if either condition a or b is True.
        """
        return Condition((a, operator.or_, self))

    def __and__(self, b: "Condition") -> "Condition":
        """
        Determines if both condition a AND b is True.
        :param b: The second condition.
        :return: True if both condition a and b is True.
        """
        return Condition((self, "and", b))

    def __invert__(self) -> "Condition":
        """
        Determines if both condition a AND b is True.
        :return: True if both condition a and b is True.
        """
        return Condition(("not", self))

    def __repr__(self) -> str:
        """
        Represents the condition.
        :return: Representation of the condition.
        """
        return f"({SPACE.join([str(x) for x in self.terms])})"
