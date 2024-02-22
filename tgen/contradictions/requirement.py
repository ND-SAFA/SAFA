from dataclasses import dataclass
from typing import Dict, List, Union

from tgen.common.util.supported_enum import SupportedEnum


class RequirementConstituent(SupportedEnum):
    CONDITION = "condition"
    EFFECT = "effect"
    ACTION = "action"
    VARIABLE = "variable"


@dataclass
class Requirement:
    id: str
    condition: str
    effect: str
    variable: Dict[RequirementConstituent, List[str]]
    action: Dict[RequirementConstituent, List[str]]

    def get_condition(self) -> str:
        """
        Gets the condition in the requirement.
        :return: The condition in the requirement.
        """
        return self.condition

    def get_effect(self) -> str:
        """
        Gets the effect in the requirement.
        :return: The effect in the requirement.
        """
        return self.effect

    def get_variable(self, constituent: RequirementConstituent, return_first: bool = True) -> Union[str, List]:
        """
        Gets the variable of the constituent in the requirement.
        :param constituent: The constituent in the requirement to get the variable from.
        :param return_first: If True, returns the first action if there is multiple for a given constituent.
        :return: The variable of the constituent in the requirement.
        """
        return self._get_component_of_constituent(self.variable, constituent, return_first)

    def get_action(self, constituent: RequirementConstituent, return_first: bool = True) -> Union[str, List]:
        """
        Gets the action of the constituent in the requirement.
        :param constituent: The constituent in the requirement to get the action from.
        :param return_first: If True, returns the first action if there is multiple for a given constituent.
        :return: The action of the constituent in the  requirement.
        """
        return self._get_component_of_constituent(self.action, constituent, return_first)

    @staticmethod
    def _get_component_of_constituent(component_dict: Dict[RequirementConstituent, List], constituent: RequirementConstituent,
                                      return_first: bool = True) -> Union[str, List[str], None]:
        """
        Gets the component of the constituent in the requirement.
        :param component_dict: Contains the component for all constituents.
        :param constituent: he constituent in the requirement to get the component from.
        :param return_first: If True, returns the first action if there is multiple for a given constituent.
        :return: The component of the constituent in the requirement.
        """
        component = component_dict.get(constituent)
        if not component:
            return
        return component[0] if return_first else component
