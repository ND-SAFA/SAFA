import os
from typing import Callable, List, Union

from data.github.abstract_github_entity import AbstractGithubArtifact
from data.github.gartifacts.gartifact_set import GArtifactSet
from data.github.gartifacts.gartifact_type import GArtifactType
from data.github.gartifacts.gcommit import GCommit
from data.github.gartifacts.gissue import GIssue
from data.github.gartifacts.gpull import GPull
from data.github.gtraces.glink import GLink
from data.github.gtraces.glink_finder import GLinkTarget, LinkFinder
from data.github.repository_downloader import logger

SearchFunction = Callable[[Union[GCommit, GIssue, GPull]], List[GLinkTarget]]


class GTraceStore:
    """
    Responsible for storing links github artifacts.
    """

    def __init__(self):
        self.trace_store = {}

    def get_linked_artifact_ids(self):
        linked_artifact_ids = {
            GArtifactType.ISSUE: set(),
            GArtifactType.PULL: set(),
            GArtifactType.COMMIT: set()
        }

        for source_type in self.trace_store.keys():
            for target_types, links in self.trace_store[source_type].items():
                for link in links:
                    linked_artifact_ids[source_type].add(link.source)
                    linked_artifact_ids[target_types].add(link.target)
        linked_artifact_ids = {k: list(v) for k, v in linked_artifact_ids.items()}
        linked_issues = linked_artifact_ids[GArtifactType.ISSUE]
        linked_pulls = linked_artifact_ids[GArtifactType.PULL]
        linked_commits = linked_artifact_ids[GArtifactType.COMMIT]
        return linked_issues, linked_pulls, linked_commits

    def keys(self) -> List[str]:
        return list(self.trace_store.keys())

    def save(self, output_path: str, **kwargs):
        logger.info("Exporting trace links...")
        for source_type in self.trace_store.keys():
            for target_type, links in self.trace_store[source_type].items():
                file_name = f"{source_type.name.lower()}2{target_type.name.lower()}.csv"
                artifact_set = GArtifactSet(links, GArtifactType.LINK)
                export_path = os.path.join(output_path, file_name)
                artifact_set.save(export_path, columns=["source", "target"], **kwargs)
                logger.info(f"Exported {file_name} ({len(artifact_set)}).")

    def parse_links(self,
                    issues: GArtifactSet[GIssue],
                    pulls: GArtifactSet[GIssue],
                    commits: GArtifactSet[GCommit]) -> None:

        self._add_links(issues.artifacts, LinkFinder.search_issue_links, GArtifactType.ISSUE)
        self._add_links(pulls.artifacts, LinkFinder.search_issue_links, GArtifactType.PULL)
        self._add_commits_to_pr(pulls.artifacts)
        self._add_links(commits.artifacts, lambda commit: LinkFinder.search_links(commit.content), GArtifactType.COMMIT)

    def _add_commits_to_pr(self, pulls: List[GPull]):
        for pull in pulls:
            for c in pull.commits:
                self._add_link(GArtifactType.COMMIT, GArtifactType.PULL, GLink(c, pull.get_id()))

    def _add_links(self,
                   artifacts: List[AbstractGithubArtifact],
                   search_function: SearchFunction,
                   source_type: GArtifactType):
        for artifact in artifacts:
            for target_id, target_type in search_function(artifact):
                self._add_link(source_type, target_type, GLink(artifact.get_id(), target_id))

    def _add_link(self, source_type, target_type, link: GLink):
        if source_type not in self.trace_store:
            self.trace_store[source_type] = {}
        if target_type not in self.trace_store[source_type]:
            self.trace_store[source_type][target_type] = []
        self.trace_store[source_type][target_type].append(link)

    def __len__(self) -> int:
        n_links = 0
        for source_type in self.trace_store.keys():
            for target_type, links in self.trace_store[source_type].items():
                n_links += len(links)
        return n_links
