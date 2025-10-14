from dataclasses import dataclass
from dataclasses import dataclass
from typing import Callable, Dict, Iterable

from gen_common.graph.branches.supported_branches import SupportedBranches
from gen_common.graph.nodes.supported_nodes import SupportedNodes

PathMapType = Iterable[SupportedNodes] | Dict[str | SupportedNodes, str | SupportedNodes]


@dataclass
class Edge:
    start: SupportedNodes
    end: SupportedNodes | str | Callable | SupportedBranches
    path_map: PathMapType = None

    def is_conditional_edge(self) -> bool:
        """
        Returns True if the edge is conditional (branching behavior).
        :return: True if the edge is conditional (branching behavior).
        """
        return isinstance(self.end, SupportedBranches) or self.path_map is not None
