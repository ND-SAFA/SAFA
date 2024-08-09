from dataclasses import dataclass, field
from typing import List

from common_resources.graph.branches.paths.path import Path
from common_resources.graph.nodes.supported_nodes import SupportedNodes


@dataclass
class PathChoices:
    paths: List[Path] = field(default_factory=list)
    default: SupportedNodes = SupportedNodes.END_COMMAND

    def get_all_paths(self, default: SupportedNodes = None) -> List[Path]:
        """
        Gets a list of all possible paths, including default.
        :param default: Overrides static default if dictated by current state.
        :return: A list of all possible paths, including default.
        """
        if not self.paths:
            return []

        paths = [path for path in self.paths]

        default = self.default if not default else default
        last_path = paths[-1]
        if default is not None and last_path.condition is not None:
            paths += [Path(action=default)]
        return paths
