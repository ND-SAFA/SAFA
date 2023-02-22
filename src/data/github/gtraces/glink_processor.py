from data.github.gartifacts.gartifact_type import GArtifactType
from data.github.gtraces.glink_store import GLinkStore


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
