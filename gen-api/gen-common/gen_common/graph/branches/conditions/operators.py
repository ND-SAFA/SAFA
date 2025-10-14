import operator
from typing import Callable

OPERATORS = {
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "is": operator.is_,
    "is not": operator.is_not,
    "in": lambda a, b: a in b,
    "not in": lambda a, b: a not in b,
    "isinstance": lambda a, b: isinstance(a, b),
    "hasattr": lambda a, b: hasattr(a, b),

    "and": operator.and_,
    "or": operator.or_,
    "not": lambda a, _: not a,
}
