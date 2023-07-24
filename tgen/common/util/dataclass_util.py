import inspect
from dataclasses import dataclass
from typing import Dict


class DataclassUtil:

    @staticmethod
    def convert_to_dict(dataclass_: dataclass, **val2replace) -> Dict:
        """
        Converts the dataclass to a dictionary
        :param dataclass_: The dataclass to convert
        :param val2replace: Dictionary mapping attr to the new value for it
        :return: the dataclass as a dictionary
        """
        args = {k: v for k, v in vars(dataclass_).items() if k not in val2replace.keys()}
        args.update(val2replace)
        return args


    @staticmethod
    def set_unique_args(child_dataclass: dataclass, parent_dataclass: dataclass, **kwargs) -> Dict:
        """
        Sets arguments that are unique to this class and returns those belonging to super class.
        :param child_dataclass: The dataclass to set unique args for
        :param parent_dataclass: The super class of the dataclass
        :param kwargs: Keyword arguments for class.
        :return: Keyword arguments belonging to parent class.
        """
        super_args = {}
        for arg_name, arg_value in kwargs.items():
            if arg_name in inspect.signature(parent_dataclass.__init__).parameters:
                super_args[arg_name] = arg_value
            elif hasattr(child_dataclass, arg_name):
                setattr(child_dataclass, arg_name, arg_value)
            else:
                raise Exception("Unrecognized training arg: " + arg_name)
        return super_args
