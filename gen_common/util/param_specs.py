from copy import copy, deepcopy
from dataclasses import dataclass
from inspect import getfullargspec
from typing import Callable, Dict, Set, Type, Union, get_type_hints, List, Any, Tuple


@dataclass
class ParamSpecs:
    param_names: Set[str]
    param_types: Dict[str, Union[Type]]
    has_kwargs: bool
    required_params: Set[str]
    name: str
    args_order: List

    @staticmethod
    def create_from_method(method: Callable) -> "ParamSpecs":
        """
        Returns the param specs for the given method
        :param method: the method to create param specs for
        :return: the param specs
        """
        full_specs = getfullargspec(method)
        expected_param_names = deepcopy(full_specs.args)
        optional_param_names = full_specs.kwonlyargs
        if "self" in expected_param_names:
            expected_param_names.remove("self")

        param_names = set(copy(expected_param_names + optional_param_names))
        type_hints = get_type_hints(method)
        param_types = {param: type_hints[param] if param in type_hints else None for param in param_names}

        expected_param_names.reverse()
        required_params = {param for i, param in enumerate(expected_param_names)
                           if not full_specs.defaults or i >= len(full_specs.defaults)}

        return ParamSpecs(name=str(method), param_names=param_names, param_types=param_types,
                          required_params=required_params, has_kwargs=full_specs.varkw is not None,
                          args_order=full_specs.args)

    def extract_params_from_kwargs(self, **kwargs):
        """
        Gets kwargs that match known param names.
        :return: A dictionary mapping param name to value for all kwargs that are known params.
        """
        constructor_param_names = self.param_names
        params = {name: val for name, val in kwargs.items()
                  if name in constructor_param_names}
        return params

    def assert_definition(self, definition: Dict) -> None:
        """
        Asserts that there are no missing or unexpected params for the method represented by the given param specs
        :param definition: the dictionary of parameter name to value mappings to check
        :return: None (raises an exception if there are missing params)
        """
        missing_params = self.get_any_missing_required_params(definition)
        if len(missing_params) >= 1:
            raise TypeError("%s is missing required arguments: %s" % (self.name, missing_params))
        self.assert_no_unexpected_params(definition)

    def assert_no_unexpected_params(self, definition: Dict) -> None:
        """
        Asserts that there are no unexpected params for the method represented by the given param specs
        :param definition: the dictionary of parameter name to value mappings to check
        :return: None (raises an exception if there are unexpected params)
        """
        extra_params = self.get_any_additional_params(definition)
        if len(extra_params) >= 1 and not self.has_kwargs:
            raise TypeError("%s received unexpected arguments: %s" % (self.name, extra_params))

    def get_any_missing_required_params(self, param_dict: Dict) -> Set[str]:
        """
        Gets any missing params for the given param specs that are not supplied in the parameter dictionary
        :param param_dict: the dictionary of parameter name to value mappings to check
        :return: a set of any missing required parameters
        """
        return set(self.required_params).difference(set(param_dict.keys()))

    def get_accepted_params(self, param_dict: Dict) -> Dict[str, Any]:
        """
        Gets all params that are accepted by the method.
        :param param_dict: the dictionary of parameter name to value mappings to filter.
        :return: A param dict containing only params that are accepted by the method.
        """
        if self.has_kwargs:
            return param_dict
        return {key: value for key, value in param_dict.items() if key in self.param_names}

    def get_any_additional_params(self, param_dict: Dict) -> Set[str]:
        """
        Gets any additional params for the given param specs that are supplied in the parameter dictionary
        :param param_dict: the dictionary of parameter name to value mappings to check
        :return: a set of any additional parameters
        """
        return set(param_dict.keys()).difference(self.param_names)

    def convert_args_to_kwargs(self, arg_values: Tuple) -> Dict[str, Any]:
        """
        Converts args to the equivalent kwargs.
        :param arg_values: List of arg values.
        :return: A dictionary mapping arg name to value for kwargs.
        """
        kwargs = {}
        for i, val in enumerate(arg_values):
            assert len(self.args_order) > i, "Unknown arg"
            arg_name = self.args_order[i]
            kwargs[arg_name] = val
        return kwargs
