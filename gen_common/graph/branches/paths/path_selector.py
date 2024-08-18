from enum import Enum
from typing import Tuple, Callable, Awaitable, List, Dict, Any, Mapping

from langchain_core.runnables.base import Runnable, RunnableLike
from langchain_core.runnables.branch import RunnableBranch
from langchain_core.runnables.utils import Input

from gen_common.graph.branches.conditions.return_value_runnable import ReturnValueRunnable
from gen_common.graph.branches.paths.path import Path

LangchainBranchType = Tuple[
    Runnable[Input, bool] |
    Callable[[Input], bool] |
    Callable[[Input], Awaitable[bool]],
    RunnableLike |
    RunnableLike,  # To accommodate the default branch
]


class PathSelector:

    def __init__(self, *paths: Path):
        """
        Selects which node to visit next based on a condition.
        :param paths: a list of (condition, node) pairs and a default branch.
        """
        paths = self._convert_branches_to_langchain_type(paths)
        self.branch = RunnableBranch(*paths)

    def select(self, state: Dict) -> Any:
        """
        Selects a node to visit next based on the state.
        :param state: The current state.
        :return: The name of the next node to visit.
        """
        return self.branch.invoke(state)

    @staticmethod
    def _convert_branches_to_langchain_type(branches: Tuple[Path]) -> List[LangchainBranchType]:
        """
        Converts the branches to the expected type for langchain runnable branch.
        :param branches: a list of (condition, node) pairs and a default branch.
        :return: the expected branch type for langchain runnable branch.
        """
        converted = []
        for branch in branches:
            path = branch
            if isinstance(branch, Path):
                path = branch.action
                if isinstance(path, Enum):
                    path = branch.action.name
                if not isinstance(path, (Runnable, Callable, Mapping)):
                    path = ReturnValueRunnable(path)
                if branch.condition:
                    path = (branch.condition, path)
            converted.append(path)
        return converted
