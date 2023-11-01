import inspect
from dataclasses import Field, MISSING, dataclass
from typing import Dict

from tgen.common.util.reflection_util import ReflectionUtil
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.tdatasets.idataset import iDataset


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

    def __init__(self, field_name: str):
        """
        Represents a field that is required in a dataclass.
        :param field_name: The name of the field.
        """
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
        args = {k: v for k, v in vars(dataclass_).items() if k not in val2replace.keys()
                and not ReflectionUtil.is_function(v) and not k.startswith("__")}
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

    @staticmethod
    def post_initialize_datasets(dataset: iDataset = None, dataset_creator: AbstractDatasetCreator = None) -> iDataset:
        """
        Ensures that a dataset is either supplied or created
        :param dataset: The dataset
        :param dataset_creator: The creator to make the dataset
        :return: The created dataset
        """
        if not dataset:
            assert dataset_creator, "Must supply either a dataset or a creator to make one."
            dataset = dataset_creator.create()
        else:
            assert not dataset_creator, "Must provide only a dataset OR a dataset creator"
        return dataset
