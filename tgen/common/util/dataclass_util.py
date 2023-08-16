import inspect
from dataclasses import dataclass, field, MISSING, Field
from typing import Dict


def required_field(*, field_name: str, init=True, repr=True, hash=None, compare=True, metadata=None):
    """
    Return an object to identify required dataclass fields.

    field_name should correspond to the attribute name of the dataclass
    If init is True, the field will be a parameter to the class's __init__()
    function.  If repr is True, the field will be included in the
    object's repr().  If hash is True, the field will be included in
    the object's hash().  If compare is True, the field will be used
    in comparison functions.  metadata, if specified, must be a
    mapping which is stored but not otherwise examined by dataclass.

    It is an error to specify both default and default_factory.
    """
    return Field(MISSING, lambda: RequiredField(field_name), init, repr, hash, compare, metadata)


class RequiredField:
    """
    Represents a field that is required in a dataclss
    """
    def __init__(self, field_name: str):
        raise TypeError(f"{field_name} is required.")


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
