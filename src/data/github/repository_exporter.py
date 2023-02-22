import os
import re
from typing import Dict, Union

from data.github.gartifacts.gartifact_set import GArtifactSet
from data.github.gartifacts.gartifact_type import GArtifactType
from data.github.gartifacts.gcode_file import GCodeFile
from data.github.gartifacts.gcommit import GCommit
from data.github.github_constants import ALLOWED_CODE_EXTENSIONS, CODE2CODE_ARTIFACT_FILE, CODE_ARTIFACT_FILE, COMMIT_ARTIFACT_FILE, \
    COMMIT_DIFF_ARTIFACT_FILE, ISSUE_ARTIFACT_FILE, \
    PULL_ARTIFACT_FILE
from data.github.gtraces.glink import GLink
from data.github.gtraces.glink_processor import GLinkProcessor
from data.github.gtraces.glink_store import GLinkStore

GENERIC_COMMIT_HEADERS = ["Merge pull request #.*from.*",
                          "Revert.*of.*",
                          "Merge branch.*of.*"]
MIN_WORD_LENGTH = 10
MIN_CODE_LENGTH = 5

COMMIT_CLEANING_REGEX = {
    "Signed-off-by.+$": "",
    "\s{2}": ". ",
    "\n": " "
}
CODE_CLEANING_REGEX = {
    "// Copyright((.|\n)*)Apache-2\.0": ""
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
        self.code = self.__clean_code(self.code, CODE_CLEANING_REGEX)

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
        if "commit2issue.csv" in entity_instructions:  # copy commit2issue for commit_diff2issue
            trace_instructions["commit_diff2issue.csv"] = {**trace_instructions["commit2issue.csv"]}
        entity_instructions.update(trace_instructions)
        entity_instructions["issue2code.csv"] = {
            "obj": self.__create_issue_2_code(),
            "col_id": "trace"
        }

        for file_name, instructions in entity_instructions.items():
            export_path = os.path.join(output_path, file_name)
            assert "obj" in instructions, f"Expected instructions to contain obj."
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

    def __create_issue_2_code(self):
        """
        Creates trace links between issues and code through the commits implementing issue.
        :return: GArtifactSet containing links.
        """
        commit2issue = self.glink_store.get_artifact_set(GArtifactType.COMMIT, GArtifactType.ISSUE)
        commit2files = {}
        for c in self.commits.artifacts:
            commit2files[c.get_id()] = c.files

        glinks = []
        for commit2issue_link in commit2issue.artifacts:
            c_id = commit2issue_link.source
            files = commit2files[c_id]
            for f in files:
                for extension in ALLOWED_CODE_EXTENSIONS:
                    if f.endswith(extension):
                        f = self.__calculate_file_path(f)
                        glinks.append(GLink(commit2issue_link.target, f))
        return GArtifactSet(glinks, GArtifactType.LINK)

    @staticmethod
    def __calculate_file_path(file_path: str):
        """
        Will calculate the file path if the path defines moving a file.
        :param file_path: The file path possibly containing move of file command.
        :return: Path to the latest movement of the path.
        """
        if "=>" in file_path:
            if "{" not in file_path:
                return file_path.split("=>")[1]
            else:
                prefix, other = file_path.split("{")
                change, suffix = other.split("}")
                before, after = change.split(" => ")
                file_path = prefix + after + suffix
        return file_path

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
        RepositoryExporter.__clean_content(commit_artifact_set, regex_replacements)
        return commit_artifact_set

    @staticmethod
    def __clean_code(code_artifact_set: GArtifactSet[GCodeFile], regex_replacement: Dict) -> GArtifactSet[GCodeFile]:
        """
        Cleans the code bodies.
        :param code_artifact_set: Artifact set of code modules.
        :param regex_replacement: The replacements for cleaning code modules.
        :return: Cleaned code artifact set.
        """
        RepositoryExporter.__clean_content(code_artifact_set, regex_replacement)
        return code_artifact_set

    @staticmethod
    def __clean_content(artifact_set: GArtifactSet[Union[GCodeFile, GCommit]], regex_replacements: Dict):
        for regex, replacement in regex_replacements.items():
            for a in artifact_set.artifacts:
                a.clean_content(lambda s: re.sub(regex, replacement, s).strip())
