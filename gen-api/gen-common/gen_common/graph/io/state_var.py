from collections.abc import Sized
from typing import Any, Callable, Dict

from gen_common.graph.branches.conditions.condition import Condition
from gen_common.graph.io.state_var_prompt_config import StateVarPromptConfig
from gen_common.util.dict_util import DictUtil
from gen_common.util.reflection_util import ReflectionUtil
from gen_common.util.str_util import StrUtil


class StateVar:

    def __init__(self, var_name: str, attribute: Callable = None, prompt_config: StateVarPromptConfig = None):
        """
        Represents a variable expected to be in the state.
        :param var_name: Name of the variable.
        :param attribute: If provided, method to call on the state variable to get final value.
        :param prompt_config: If provided, specifies how the state var should be displayed in a prompt to the LLM.
        """
        self.var_name = var_name
        self.prompt_config = prompt_config if prompt_config else StateVarPromptConfig()
        if not self.prompt_config.title:
            self.prompt_config.title = StrUtil.separate_joined_words(self.var_name).title()
        self.__attribute = attribute

    def get_value(self, state: Dict) -> Any:
        """
        Gets that value of the variable in state.
        :param state: The state.
        :return: The value of the variable in state.
        """
        value = state.get(self.var_name)
        if self.__attribute:
            value = self.__attribute(value)
        return value

    def _create_condition(self, operator: str, other: Any = None, self_is_first_term: bool = True) -> Condition:
        """
        Creates a condition to compare state value with another object.
        :param operator: The operator to use to evaluate with other.
        :param other: The comparison value.
        :param self_is_first_term: If True, self is first term, otherwise other will come before operator.
        :return: A condition comparing value of and other.
        """

        if self_is_first_term:
            terms = (self, operator, other)
        elif other is None:
            terms = (operator, self)
        else:
            terms = (other, operator, self)
        return Condition(terms)

    def contains(self, item: Any) -> Condition:
        """
        Item in State value.
        :param item: Item to check if it exists in the state value.
        :return: Item in State value.
        """
        return self._create_condition("in", item, self_is_first_term=False)

    def is_(self, other: Any) -> Condition:
        """
        State value is other.
        :param other: The comparison value.
        :return: State value is other.
        """
        return self._create_condition("is", other)

    def is_instance(self, other: Any) -> Condition:
        """
        State value is instance of other.
        :param other: The comparison value.
        :return: State value is instance of other.
        """
        return self._create_condition("isinstance", other)

    def exists(self) -> Condition:
        """
        True if the object is not None or empty.
        :return:  True if the object is not None or empty.
        """
        is_none = self.is_(None)
        is_sized = self.is_instance(Sized)
        is_empty = self.length() == 0
        return ~ (is_none | (is_sized & is_empty))

    def length(self) -> "StateVar":
        """
        Adds length as the attribute to obtain from state value.
        :return: Updated state var with length as the attribute to obtain from state value.
        """
        var_name = ReflectionUtil.extract_name_of_variable(f"{self.__attribute=}", is_self_property=True)
        var_name = f"_{self.__class__.__name__}{var_name}"
        params = {var: value for var, value in self.__dict__.items() if var != var_name}
        params = DictUtil.update_kwarg_values(params, attribute=len)
        return StateVar(**params)

    def __hash__(self) -> int:
        """
        Hashes the state var based on name of variable.
        :return: Hash of the state var based on name of variable.
        """
        return hash(self.var_name)

    def __eq__(self, other: Any) -> Condition:
        """
        State value == other.
        :param other: Comparison value.
        :return: State value == other.
        """
        return self._create_condition("==", other)

    def __ne__(self, other: Any) -> Condition:
        """
        State value != other.
        :param other: Comparison value.
        :return: State value != other.
        """
        return self._create_condition("!=", other)

    def __lt__(self, other: Any) -> Condition:
        """
        State value < other.
        :param other: Comparison value.
        :return: State value < other.
        """
        return self._create_condition("<", other)

    def __gt__(self, other: Any) -> Condition:
        """
        State value > other.
        :param other: Comparison value.
        :return: State value > other.
        """
        return self._create_condition(">", other)

    def __le__(self, other: Any) -> Condition:
        """
        State value <= other.
        :param other: Comparison value.
        :return: State value < other.
        """
        return self._create_condition("<=", other)

    def __ge__(self, other: Any) -> Condition:
        """
        State value >= other.
        :param other: Comparison value.
        :return: State value > other.
        """
        return self._create_condition(">=", other)

    def __invert__(self) -> Condition:
        """
        Not state value.
        :return:  Not state value.
        """
        return self._create_condition("not", self_is_first_term=False)

    def __repr__(self) -> str:
        """
        Creates a representation of the state variable.
        :return: String representation of the state variable.
        """
        if self.__attribute:
            return f"{self.__attribute.__name__}({self.var_name})"
        return self.var_name
