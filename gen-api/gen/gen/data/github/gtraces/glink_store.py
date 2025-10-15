from typing import Callable, Dict, List, Union

from gen.data.github.abstract_github_entity import AbstractGithubArtifact
from gen.data.github.gartifacts.gartifact_set import GArtifactSet
from gen.data.github.gartifacts.gartifact_type import GArtifactType
from gen.data.github.gartifacts.gcommit import GCommit
from gen.data.github.gartifacts.gissue import GIssue
from gen.data.github.gartifacts.gpull import GPull
from gen.data.github.gtraces.glink import GLink
from gen.data.github.gtraces.glink_finder import GLinkTarget, LinkFinder

SearchFunction = Callable[[Union[GCommit, GIssue, GPull]], List[GLinkTarget]]


class GLinkStore:
    """
    Responsible for storing links between github artifacts.
    ---
    Uses a nested dictionary to map source type -> target type -> Links between source and target.
    """

    def __init__(self):
        """
        Initializes empty store.
        """
        self.store = {}

    def create_artifact_sets(self) -> Dict[str, GArtifactSet[GLink]]:
        """
        Creates artifacts sets for each trace query in store.
        :return: None
        """
        artifact_sets = {}
        for source_type in self.store.keys():
            for target_type, links in self.store[source_type].items():
                file_name = f"{source_type.name.lower()}2{target_type.name.lower()}.csv"
                artifact_sets[file_name] = self.get_artifact_set(source_type, target_type)
        return artifact_sets

    def has_artifact_set(self, source_type: GArtifactType, target_type: GArtifactType):
        """
        Returns whether trace links exists between given types.
        :param source_type: The source type of artifacts.
        :param target_type: The target type of artifacts.
        :return: Whether trace links exist between source and target type of artifact.
        """
        return source_type in self.store and target_type in self.store[source_type]

    def get_artifact_set(self, source_type: GArtifactType, target_type: GArtifactType):
        """
        Returns artifact set containing links between source and target types.
        :param source_type: The source type of artifacts.
        :param target_type: The target type of artifacts.
        :return: Artifact set containing trace links between source and target types.
        """
        if not self.has_artifact_set(source_type, target_type):
            return GArtifactSet([], GArtifactType.LINK)
        links = self.store[source_type][target_type]
        return GArtifactSet(links, GArtifactType.LINK)

    def add_artifact_links(self,
                           issues: GArtifactSet[GIssue],
                           pulls: GArtifactSet[GIssue],
                           commits: GArtifactSet[GCommit]) -> None:
        """
        Processes artifact's links and adds them to store.
        :param issues: List of issues.
        :param pulls:  List of pull requests.
        :param commits: List of commits.
        :return: None
        """
        self.add_artifacts_links(issues.artifacts, LinkFinder.search_issue_links, GArtifactType.ISSUE)
        self.add_artifacts_links(pulls.artifacts, LinkFinder.search_issue_links, GArtifactType.PULL)
        self.add_commits_to_pr(pulls.artifacts)
        self.add_artifacts_links(commits.artifacts, lambda commit: LinkFinder.search_links(commit.content), GArtifactType.COMMIT)

    def get_source_types(self) -> List[GArtifactType]:
        """
        :return: Returns source artifacts containing links.
        """
        return list(self.store.keys())

    def add_commits_to_pr(self, pulls: List[GPull]) -> None:
        """
        Adds links between commits and pull requests in the right direction (commit -> pull).
        :param pulls: The pull request containing links to commits.
        :return: None
        """
        for pull in pulls:
            for c in pull.commits:
                self.add_link(GArtifactType.COMMIT, GArtifactType.PULL, GLink(c, pull.get_id()))

    def add_artifacts_links(self,
                            artifacts: List[AbstractGithubArtifact],
                            search_function: SearchFunction,
                            source_type: GArtifactType) -> None:
        """
        Searches and adds links found in artifact content to store.
        :param artifacts: The artifacts to search for links in.
        :param search_function: The search function returning links in artifact.
        :param source_type: The artifact type of the artifacts.
        :return: None
        """
        for artifact in artifacts:
            for target_id, target_type in search_function(artifact):
                self.add_link(source_type, target_type, GLink(artifact.get_id(), target_id))

    def add_link(self, source_type, target_type, link: GLink) -> None:
        """
        Adds given link between source and target types.
        :param source_type: The GitHub artifact type of the source id.
        :param target_type: The GitHub artifact type of the target id.
        :param link: The link specifying source and target artifacts ids.
        :return: None
        """
        if source_type not in self.store:
            self.store[source_type] = {}
        if target_type not in self.store[source_type]:
            self.store[source_type][target_type] = []
        self.store[source_type][target_type].append(link)

    def __len__(self) -> int:
        """
        :return: Returns the total number of trace links in the store.
        """
        n_links = 0
        for source_type in self.store.keys():
            for target_type, links in self.store[source_type].items():
                n_links += len(links)
        return n_links

    def __getitem__(self, source_gartifact_type: GArtifactType) -> Dict[GArtifactType, List[GLink]]:
        """
        Returns the set of links associated with given type.
        :param source_gartifact_type: The github artifact type.
        :return: Dictionary of target types and their associated trace links.
        """
        return self.store[source_gartifact_type]

    def __contains__(self, source_gartifact_type: GArtifactType) -> bool:
        """
        Whether source artifact type contains links.
        :param source_gartifact_type: The source artifact type.
        :return: True if source type contains links, false otherwise.
        """
        return source_gartifact_type in self.store
