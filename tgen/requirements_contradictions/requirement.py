from dataclasses import dataclass
from typing import Dict

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
    variable: Dict[RequirementConstituent, str]
    action: Dict[RequirementConstituent, str]

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

    def get_variable(self, constituent: RequirementConstituent) -> str:
        """
        Gets the variable of the constituent in the requirement.
        :param constituent: The constituent in the requirement to get the variable from.
        :return: The variable of the constituent in the requirement.
        """
        return self.variable.get(constituent)

    def get_action(self, constituent: RequirementConstituent) -> str:
        """
        Gets the action of the constituent in the requirement.
        :param constituent: The constituent in the requirement to get the action from.
        :return: The action of the constituent in the requirement.
        """
        return self.action.get(constituent)
