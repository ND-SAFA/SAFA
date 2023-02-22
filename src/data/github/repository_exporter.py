import os
import re
from typing import Dict

from data.github.gartifacts.gartifact_set import GArtifactSet
from data.github.gartifacts.gartifact_type import GArtifactType
from data.github.gartifacts.gcode_file import GCodeFile
from data.github.gartifacts.gcommit import GCommit
from data.github.github_constants import CODE2CODE_ARTIFACT_FILE, CODE_ARTIFACT_FILE, COMMIT_ARTIFACT_FILE, \
    COMMIT_DIFF_ARTIFACT_FILE, ISSUE_ARTIFACT_FILE, \
    PULL_ARTIFACT_FILE
from data.github.gtraces.glink_processor import GLinkProcessor
from data.github.gtraces.glink_store import GLinkStore

GENERIC_COMMIT_HEADERS = ["Merge pull request #.*from.*",
                          "Revert.*of.*",
                          "Merge branch.*of.*"]
MIN_WORD_LENGTH = 15
MIN_CODE_LENGTH = 5

COMMIT_CLEANING_REGEX = {
    "Signed-off-by.+$": "",
    "\s{2}": ". ",
    "\n": " "
}
EXPORT_COLUMN_MAP = {
    "trace": ["source", "target"],
    "artifact": ["id", "content"]
}


class RepositoryExporter:
    """
    Reads parsed artifacts and cleans them for export.
    """
    SOURCE_FILE = "sources.csv"
    TARGET_FILE = "targets.csv"
    LINK_FILE = "links.csv"

    def __init__(self, repo_path: str):
        """
        Initializes extracter for given repo and
        :param repo_path: Path to the local repository.
        """
        self.repo_path = repo_path
        self.issues = self.__read_artifact_set(ISSUE_ARTIFACT_FILE)
        self.pulls = self.__read_artifact_set(PULL_ARTIFACT_FILE)
        self.commits = self.__read_artifact_set(COMMIT_ARTIFACT_FILE)
        self.code = self.__read_artifact_set(CODE_ARTIFACT_FILE)
        self.code2code = self.__read_artifact_set(CODE2CODE_ARTIFACT_FILE)
        self.glink_store = GLinkStore()
        self.glink_store_processor = GLinkProcessor(self.glink_store)

    def extract(self, output_path: str) -> None:
        """
        Reads and extracts dataset from repo, saving entities to output path.
        :param output_path: Path to output directory to save entities to.
        :return:  None
        """
        self.process_repo()
        self.save(output_path=output_path)

    def process_repo(self) -> None:
        """
        Cleans commits, reads trace links, and filters orphans.
        :return:  None
        """
        self.commits = self.__remove_default_commits(self.commits)
        self.commits = self.__remove_short_commits(self.commits, MIN_WORD_LENGTH, MIN_CODE_LENGTH)
        self.commits = self.__clean_commits(self.commits, COMMIT_CLEANING_REGEX)
        self.code = self.__clean_code(self.code)

        self.glink_store.add_artifact_links(self.issues, self.pulls, self.commits)  # Note, code links are already exported.
        linked_issues, linked_pulls, linked_commits = self.glink_store_processor.get_linked_artifact_ids()
        self.issues = self.issues.filter(linked_issues)
        self.pulls = self.pulls.filter(linked_pulls)
        self.commits = self.commits.filter(linked_commits)

    def save(self, output_path: str) -> None:
        """
        Saves artifacts and trace links to output path.
        :param output_path: The path to the output directory to save to.
        :return: None
        """
        entity_instructions: Dict[str: Dict] = {
            ISSUE_ARTIFACT_FILE.replace(".json", ".csv"): {
                "obj": self.issues,
                "col_id": "artifact"
            },
            PULL_ARTIFACT_FILE.replace(".json", ".csv"): {
                "obj": self.pulls,
                "col_id": "artifact"
            },
            COMMIT_ARTIFACT_FILE.replace(".json", ".csv"): {
                "obj": self.commits,
                "col_id": "artifact"
            },
            COMMIT_DIFF_ARTIFACT_FILE.replace(".json", ".csv"): {
                "obj": self.commits,
                "col_id": "artifact",
                "dataset_type": "PL"
            },
            CODE_ARTIFACT_FILE.replace(".json", ".csv"): {
                "obj": self.code,
                "col_id": "artifact"
            },
            CODE2CODE_ARTIFACT_FILE.replace(".json", ".csv"): {
                "obj": self.code2code,
                "col_id": "trace"
            }
        }
        trace_artifact_sets = self.glink_store.create_artifact_sets()
        trace_instructions = {file_name: {
            "obj": artifact_set,
            "col_id": "trace"
        } for file_name, artifact_set in trace_artifact_sets.items()}
        trace_instructions["commit_diff2issue.csv"] = {
            **trace_instructions["commit2issue.csv"]}  # copy commit2issue for commit_diff2issue
        entity_instructions.update(trace_instructions)

        for file_name, instructions in entity_instructions.items():
            export_path = os.path.join(output_path, file_name)
            artifact_set = instructions.pop("obj")
            col_id = instructions.pop("col_id")
            artifact_set.export(export_path, columns=EXPORT_COLUMN_MAP[col_id], **instructions)

    def __read_artifact_set(self, artifact_file_name: str) -> GArtifactSet:
        """
        Reads artifact set in repo with given file name.
        :param artifact_file_name: The file name containing the artifacts to read in repo.
        :return: Artifact set with artifacts loaded.
        """
        artifact_file_path = os.path.join(self.repo_path, artifact_file_name)
        return GArtifactSet.load(artifact_file_path)

    @staticmethod
    def __remove_default_commits(commit_artifact_set: GArtifactSet[GCommit]) -> GArtifactSet[GCommit]:
        """
        Removes GitHub generated commits including pull requests merge and reverts.
        :param commit_artifact_set: The artifact set containing commits.
        :return: User created-commits.
        """
        commits = []
        for commit in commit_artifact_set.artifacts:
            hits = [re.search(generic_header, commit.content) for generic_header in GENERIC_COMMIT_HEADERS]
            hits = [h for h in hits if h is not None]
            if len(hits) == 0:
                commits.append(commit)
        return GArtifactSet(commits, GArtifactType.COMMIT)

    @staticmethod
    def __remove_short_commits(commit_artifact_set: GArtifactSet[GCommit], min_artifact_length: int, min_code_length: int) -> \
            GArtifactSet[GCommit]:
        """
        Removes commits whose body is less than minimum artifact length defined in constants.
        :param commit_artifact_set: The set of commits in repository.
        :param min_artifact_length: The minimum length of the artifacts to keep.
        :return: Commits with equal or greater content length than minimum.
        """
        long_messages = [a for a in commit_artifact_set.artifacts if
                         len(a.content.split(" ")) >= min_artifact_length and len(a.diffs) >= min_code_length]
        return GArtifactSet(long_messages, GArtifactType.COMMIT)

    @staticmethod
    def __clean_commits(commit_artifact_set: GArtifactSet[GCommit], regex_replacements: Dict) -> GArtifactSet[GCommit]:
        """
        Removes redundant text and strips content.
        :param commit_artifact_set: The set of artifacts to clean.
        :return: The cleaned artifacts.
        """
        for regex, replacement in regex_replacements.items():
            for a in commit_artifact_set.artifacts:
                a.clean_content(lambda s: re.sub(regex, replacement, s).strip())
        return commit_artifact_set

    @staticmethod
    def __clean_code(code_artifact_set: GArtifactSet[GCodeFile]) -> GArtifactSet[GCodeFile]:
        LICENSE_REGEX = "^//Copyright((.|\\n)*)Apache-2\.0"
        for a in code_artifact_set.artifacts:
            a.clean_content(lambda s: re.sub(LICENSE_REGEX, "", s).strip())
        return code_artifact_set
