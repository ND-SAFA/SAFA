from dataclasses import dataclass
from typing import Dict, List, Union, Any

from gen_common.util.supported_enum import SupportedEnum


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

    def get_constituent(self, constituent2get: RequirementConstituent, **kwargs) -> Any:
        """
        Gets the constituent of the requirement.
        :param constituent2get: The constituent to get.
        :param kwargs: Additional arguments to the getter.
        :return: The constituent.
        """
        return getattr(self, f"get_{constituent2get.value}")(**kwargs)

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

    def get_variable(self, constituent: RequirementConstituent = None, default: Any = None) -> Union[str, List]:
        """
        Gets the variable of the constituent in the requirement.
        :param constituent: The constituent in the requirement to get the variable from.
        :param default: Default value if does not exist.
        :return: The variable of the constituent in the requirement.
        """
        return self._get_component_of_constituent(self.variable, constituent, default)

    def get_action(self, constituent: RequirementConstituent = None,
                   default: Any = None) -> Union[str, List]:
        """
        Gets the action of the constituent in the requirement.
        :param constituent: The constituent in the requirement to get the action from.
        :param default: Default value if does not exist.
        :return: The action of the constituent in the  requirement.
        """
        return self._get_component_of_constituent(self.action, constituent, default)

    def is_empty(self) -> bool:
        """
        Returns True if the requirement does not contain a condition or an effect.
        :return: True if the requirement does not contain a condition or an effect.
        """
        return not self.get_condition() and not self.get_effect()

    @staticmethod
    def _get_component_of_constituent(component_dict: Dict[RequirementConstituent, str],
                                      constituent: RequirementConstituent = None,
                                      default: Any = None) -> Union[str, List[str], None]:
        """
        Gets the component of the constituent in the requirement.
        :param component_dict: Contains the component for all constituents.
        :param constituent: he constituent in the requirement to get the component from.
        :param default: Default value if does not exist.
        :return: The component of the constituent in the requirement.
        """
        if not constituent:
            components = [Requirement._get_component_of_constituent(component_dict, RequirementConstituent.CONDITION),
                          Requirement._get_component_of_constituent(component_dict, RequirementConstituent.EFFECT)]
            return [c if c is not None else default for c in components]
        return component_dict.get(constituent, default)
