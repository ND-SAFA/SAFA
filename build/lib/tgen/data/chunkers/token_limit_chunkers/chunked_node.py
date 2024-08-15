import ast
from dataclasses import dataclass, field
from typing import List, Union, Any

from common_resources.tools.util.dict_util import DictUtil


@dataclass
class ChunkedNode:
    lineno: int
    end_lineno: int
    type: str
    body: List = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        After initialization, ensures that al items in the body are of the node type
        :return: None
        """
        self.body = [ChunkedNode.from_python_ast(child) if not isinstance(child, ChunkedNode) else child for child in self.body] \
            if self.body is not None else []

    @staticmethod
    def from_python_ast(ast_node: Union[ast.AST, ast.stmt]) -> "ChunkedNode":
        """
        Creates a node from python ast
        :param ast_node: The node from python ast
        :return: The python ast as a Node
        """
        params = {}
        for attr_name in ChunkedNode.__annotations__.keys():
            params[attr_name] = getattr(ast_node, attr_name, None)
        DictUtil.update_kwarg_values(params, type=ChunkedNode.get_type_name(ast_node))
        return ChunkedNode(**params)

    @staticmethod
    def get_type_name(obj: Any) -> str:
        """
        Gets the class name of the obj
        :param obj: The obj to get the type name of
        :return: The type name
        """
        return obj.__class__.__name__
