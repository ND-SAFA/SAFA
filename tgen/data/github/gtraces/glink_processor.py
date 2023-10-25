from typing import Dict, List

from tgen.data.github.gartifacts.gartifact_set import GArtifactSet
from tgen.data.github.gartifacts.gartifact_type import GArtifactType
from tgen.data.github.gtraces.glink import GLink
from tgen.data.github.gtraces.glink_store import GLinkStore


class GLinkProcessor:
    """
    Provides processing functions on the link store.
    """

    def __init__(self, glink_store: GLinkStore):
        """
        Constructor processor for link store.
        :param glink_store: Store containing links to process.
        """
        self.glink_store = glink_store

    def get_linked_artifact_ids(self):
        """
        Calculates list of referenced issues, pulls, and commits.
        :return: List of ids for linked issues, pulls, and commits.
        """
        linked_artifact_ids = {
            GArtifactType.ISSUE: set(),
            GArtifactType.PULL: set(),
            GArtifactType.COMMIT: set()
        }

        for source_type in self.glink_store.get_source_types():
            for target_types, links in self.glink_store[source_type].items():
                for link in links:
                    linked_artifact_ids[source_type].add(link.source)
                    linked_artifact_ids[target_types].add(link.target)
        linked_artifact_ids = {k: list(v) for k, v in linked_artifact_ids.items()}
        linked_issues = linked_artifact_ids[GArtifactType.ISSUE]
        linked_pulls = linked_artifact_ids[GArtifactType.PULL]
        linked_commits = linked_artifact_ids[GArtifactType.COMMIT]
        return linked_issues, linked_pulls, linked_commits

    @staticmethod
    def get_transitive_traces(level_1: GArtifactSet[GLink], level_2: GArtifactSet[GLink]):
        """
        Creates transitive traces between target layer of level 1 and source of level 2.
        :param level_1: Set of trace links in upper level of hierarchy.
        :param level_2: Set of trace links in lower level of hierarchy.
        :return: Set of transitive trace links.
        """

        def save_link(store, link: GLink) -> None:
            """
            Saves links in store.
            :param store: The store of all links
            :param link: The link to store.
            :return: None
            """
            if link.target not in store:
                store[link.target] = []
            store[link.target].append(link)

        level_1_store: Dict[str, List[GLink]] = {}

        for t in level_1:
            save_link(level_1_store, t)

        transitive_traces = []
        for t2 in level_2:
            connecting_traces: List[GLink] = level_1_store.get(t2.source, [])
            for t in connecting_traces:
                transitive_traces.append(GLink(t.source, t2.target))
        return GArtifactSet(transitive_traces, GArtifactType.LINK)

    @staticmethod
    def flip(link_set: GArtifactSet[GLink]):
        """
        Creates artifact set with reverse direction of link.
        :param link_set: Set of links.
        :return: Artifact set of flipped links.
        """
        flipped_set = list(map(lambda t: GLink(t.target, t.source), link_set))
        return GArtifactSet(flipped_set, GArtifactType.LINK)
