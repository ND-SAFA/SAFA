from abc import abstractmethod
from enum import Enum, IntEnum, auto
from typing import Any, Callable, Dict, Type

from langchain_core.tools import BaseTool
from pydantic.v1.fields import FieldInfo
from pydantic.v1.main import BaseModel

from gen_common.constants.symbol_constants import BRACKET_CLOSE, BRACKET_OPEN, DASH, SQ_BRACKET_CLOSE, SQ_BRACKET_OPEN
from gen_common.graph.io.graph_state import GraphState
from gen_common.util.dict_util import DictUtil
from gen_common.util.str_util import StrUtil

ToolType = Dict[str, Any] | Type[BaseModel] | Callable | BaseTool


class Default(IntEnum):
    ALL = auto()
    NONE = auto()
    NO_DEFAULT = auto()


class DynamicEnumFieldInfo(FieldInfo):
    state_var: str
    default_selection: Default = Default.NO_DEFAULT

    def __init__(self, state_var: str, default_selection: Default = Default.NO_DEFAULT, **field_info):
        """
        Represents a field that will be dynamically updated with state values.
        :param state_var: The corresponding state value used to update field.
        :param default_selection: Default option.
        :param field_info: Any additional values for the field info.
        """
        self.state_var = state_var
        self.default_selection = default_selection
        super().__init__(**field_info)


def DynamicEnumField(state_var: str, default_selection: Default = Default.NO_DEFAULT, **field_info):
    """
    Represents a field that will be dynamically updated based on state.
    :param state_var: The corresponding state value used to update field.
    :param default_selection: Default option.
    :param field_info: Additional field info.
    :return: The FieldInfo to be used in creating the schema.
    """
    field_info_kwargs = DictUtil.update_kwarg_values(field_info, **{"state_var": state_var,
                                                                    "default_selection": default_selection})
    field_info = DynamicEnumFieldInfo(**field_info_kwargs)
    field_info._validate()
    return field_info


class BaseTool(BaseModel):

    @classmethod
    def to_schema(cls, state: GraphState) -> Dict:
        """
        Converts the tool to the schema, updating dynamic fields as needed.
        :param state: The current state of the graph.
        :return: The schema of the tool.
        """
        schema = cls.schema()
        for name, val in cls.__fields__.items():
            if isinstance(val.field_info, DynamicEnumFieldInfo):
                field_info = val.field_info
                assert field_info.state_var in state, f"Cannot update field because state does not contain {field_info.state_var}"
                state_value = state.get(field_info.state_var)
                enum_id = DASH.join(state_value)
                NewEnum = Enum(f"{name.upper()}_{enum_id}", {val: val for val in state_value})
                schema["$defs"] = {
                    NewEnum.__name__: {
                        'enum': state_value,
                        'title': NewEnum.__name__,
                        'type': cls.get_type(state_value[0])
                    }
                }
                new_property = {'allOf': [{'$ref': f'#/$defs/{NewEnum.__name__}'}]}
                if field_info.default_selection == Default.ALL:
                    new_property["default"] = state_value
                elif field_info.default_selection == Default.NONE:
                    new_property["default"] = None

                orig_property = {k: v for k, v in schema["properties"][name].items() if k in {"title", "description"}}
                new_property.update(orig_property)
                schema["properties"][name] = new_property
        return schema

    @abstractmethod
    def update_state(self, state: GraphState) -> None:
        """
        Updates the state with the response information.
        :param state: The state.
        """

    @classmethod
    def get_description(cls) -> str:
        """
        Gets the description of the tool.
        :return: The description of the tool.
        """
        return cls.__doc__

    @staticmethod
    def get_type(o: Any):
        """
        :param o: The object to get type of.
        :returns: The pydantic type of the given object.
        """
        if o is None:
            return "null"
        elif isinstance(o, list):
            return "array"
        elif isinstance(o, dict):
            return "object"
        elif isinstance(o, int):
            return "integer"
        elif isinstance(o, float):
            return "number"
        elif isinstance(o, str):
            return "string"
        elif isinstance(o, bool):
            return "boolean"
        else:
            raise Exception(f"Unsupported json type:{type(o)}: {o}")

    def __repr__(self) -> str:
        """
        Creates a string representation of the tool.
        :return: A string representation of the tool.
        """
        representation = super().__repr__()
        representation = StrUtil.word_replacement([representation], {
            BRACKET_OPEN: SQ_BRACKET_OPEN,
            BRACKET_CLOSE: SQ_BRACKET_CLOSE,
        }, full_match_only=False)[0]
        return representation
