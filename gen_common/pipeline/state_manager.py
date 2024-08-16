from copy import deepcopy
from typing import Any, Generic, Optional, TypeVar

from gen_common.tools.util.base_object import BaseObject
from gen_common.tools.util.dataclass_util import DataclassUtil
from gen_common.tools.state_management.state import State

StateType = TypeVar("StateType", bound=State)


class StateManager(BaseObject, Generic[StateType]):
    """
    Manages all states
    """

    def __init__(self, state: StateType):
        """
        Initialize with current state
        :param state: The current state
        """
        self._current_state = state
        self.history = []

    def update_state(self, **state_props) -> None:
        """
        Updates the current state to the given one
        :param state_props: The properties of state to update
        :return: None
        """
        previous_state_props = DataclassUtil.convert_to_dict(self._current_state)
        previous_state_props.update(state_props)
        new_state = self._current_state.__class__(**state_props)
        self.set_current_state(new_state)

    def set_current_state(self, state: StateType) -> None:
        """
        Updates the current state to the given one
        :param state: The new current state
        :return: None
        """
        self.history.append(deepcopy(self._current_state))
        self._current_state = state

    def reset_state_to_last(self) -> StateType:
        """
        Resets the current state to be the last state
        :return: The current state (reset to be the last)
        """
        self._current_state = self.history.pop()
        return self._current_state

    def get_previous_state(self, n_before: int = 1) -> Optional[StateType]:
        """
        Gets a previous state
        :param n_before: The number of states before the current to get (i.e. the current state would be 0 before,
                                                                                the previous state is 1 before, etc...)
        :return: The state n_before the current
        """
        n_before = n_before * -1 if n_before > 0 else n_before
        if n_before == 0:
            return self._current_state
        if n_before * -1 > len(self.history):
            return None
        return self.history[-1]

    def get(self, prop_name: str) -> Any:
        """
        Gets a property from the state
        :param prop_name: The name of the property
        :return: The property from the current state
        """
        return getattr(self._current_state, prop_name)
