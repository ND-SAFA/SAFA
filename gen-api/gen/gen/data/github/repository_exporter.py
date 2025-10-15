import os
import re
from typing import Dict, Union

from gen_common.data.processing.cleaning.data_cleaner import DataCleaner
from gen_common.data.processing.cleaning.regex_replacement_step import RegexReplacementStep
from gen_common.constants.code_extensions import ALLOWED_CODE_EXTENSIONS
from gen_common.constants.symbol_constants import NEW_LINE, SPACE

from gen.data.github.gartifacts.gartifact_set import GArtifactSet
from gen.data.github.gartifacts.gartifact_type import GArtifactType
from gen.data.github.gartifacts.gcode_file import GCodeFile
from gen.data.github.gartifacts.gcommit import GCommit
from gen.data.github.gartifacts.gissue import GIssue
from gen.data.github.github_constants import CODE2CODE_ARTIFACT_FILE, CODE2CODE_EXPORT_FILE, \
    CODE_ARTIFACT_FILE, \
    CODE_EXPORT_FILE, COMMIT2ISSUE_EXPORT_FILE, COMMITDIFF2ISSUE_EXPORT_FILE, COMMIT_ARTIFACT_FILE, \
    COMMIT_DIFF_EXPORT_FILE, COMMIT_EXPORT_FILE, ISSUE2CODE_EXPORT_FILE, ISSUE_ARTIFACT_FILE, \
    ISSUE_EXPORT_FILE, PULL_ARTIFACT_FILE, PULL_EXPORT_FILE
from gen.data.github.gtraces.glink import GLink
from gen.data.github.gtraces.glink_processor import GLinkProcessor
from gen.data.github.gtraces.glink_store import GLinkStore

GENERIC_COMMIT_HEADERS = ["Merge pull request #.*from.*",
                          "Revert.*of.*",
                          "Merge branch.*into.*",
                          "Merge branch.*of.*"]
MIN_WORD_LENGTH = 5
MIN_CODE_LENGTH = 3

COMMIT_CLEANING_REGEX = {
    "Signed-off-by.+$": "",
    "\s{2}": ". ",
    NEW_LINE: SPACE,
    "<!-.*->": "",
    "```.*```": ""
}
ISSUE_CLEANING_REGEX = {
    "<!-.*->": "",
    "```.*```": ""
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
    DEFAULT_COL_ID = "artifact"
    OBJ = "obj"
    COL_ID = "col_id"

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
        self.commit2issue = None

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
        self.commits = self.__clean_commits(self.commits, RepositoryExporter.__create_regex_data_cleaner(COMMIT_CLEANING_REGEX))
        self.code = self.__clean_code(self.code, RepositoryExporter.__create_regex_data_cleaner(CODE_CLEANING_REGEX))
        self.issues = self.__clean_issues(self.issues, RepositoryExporter.__create_regex_data_cleaner(ISSUE_CLEANING_REGEX))

        self.glink_store.add_artifact_links(self.issues, self.pulls, self.commits)  # Note, code links are already exported.
        linked_issues, linked_pulls, linked_commits = self.glink_store_processor.get_linked_artifact_ids()
        self.issues = self.issues.filter(linked_issues)
        self.pulls = self.pulls.filter(linked_pulls)
        self.commits = self.commits.filter(linked_commits)
        self.commit2issue = self.__create_issue_2_commit()

    def save(self, output_path: str) -> None:
        """
        Saves artifacts and trace links to output path.
        :param output_path: The path to the output directory to save to.
        :return: None
        """
        entity_instructions: Dict[str: Dict] = {
            ISSUE_EXPORT_FILE: {
                self.OBJ: self.issues
            },
            PULL_EXPORT_FILE: {
                self.OBJ: self.pulls
            },
            COMMIT_EXPORT_FILE: {
                self.OBJ: self.commits
            },
            COMMIT_DIFF_EXPORT_FILE: {
                self.OBJ: self.commits,
                "dataset_type": "PL"
            },
            CODE_EXPORT_FILE: {
                self.OBJ: self.code
            },
            CODE2CODE_EXPORT_FILE: {
                self.OBJ: self.code2code,
                self.COL_ID: "trace"
            },
            COMMIT2ISSUE_EXPORT_FILE: {
                self.OBJ: self.commit2issue,
                self.COL_ID: "trace"
            }
        }
        trace_artifact_sets: Dict[str, GArtifactSet[GLink]] = self.glink_store.create_artifact_sets()
        trace_instructions = {file_name: {
            self.OBJ: artifact_set,
            self.COL_ID: "trace"
        } for file_name, artifact_set in trace_artifact_sets.items()}

        if COMMIT2ISSUE_EXPORT_FILE in trace_instructions:
            trace_instructions[COMMITDIFF2ISSUE_EXPORT_FILE] = {
                **entity_instructions[COMMIT2ISSUE_EXPORT_FILE]}  # TODO: Append ids with DIFF

        # appe
        for k, v in trace_instructions.items():
            if k in entity_instructions:
                entity_instructions[k] = {
                    self.OBJ: entity_instructions[k][self.OBJ] + v[self.OBJ],
                    self.COL_ID: "trace"
                }
            else:
                entity_instructions[k] = v

        entity_instructions[ISSUE2CODE_EXPORT_FILE] = {
            self.OBJ: self.__create_issue_2_code(self.commit2issue),
            self.COL_ID: "trace"
        }

        os.makedirs(output_path, exist_ok=True)
        for file_name, instructions in entity_instructions.items():
            if self.COL_ID not in instructions:
                instructions[self.COL_ID] = self.DEFAULT_COL_ID
            export_path = os.path.join(output_path, file_name)
            assert self.OBJ in instructions, f"Expected instructions to contain obj."
            artifact_set: GArtifactSet = instructions.pop(self.OBJ)
            col_id = instructions.pop(self.COL_ID)
            artifact_set.export(export_path, columns=EXPORT_COLUMN_MAP[col_id], **instructions)

    def __read_artifact_set(self, artifact_file_name: str) -> GArtifactSet:
        """
        Reads artifact set in repo with given file name.
        :param artifact_file_name: The file name containing the artifacts to read in repo.
        :return: Artifact set with artifacts loaded.
        """
        artifact_file_path = os.path.join(self.repo_path, artifact_file_name)
        return GArtifactSet.load(artifact_file_path)

    def __create_issue_2_commit(self) -> GArtifactSet[GLink]:
        """
        Creates links between commits and issues using direct and transitive links.
        :return: The links between commits and issues.
        """
        commit2pull = self.glink_store.get_artifact_set(GArtifactType.COMMIT, GArtifactType.PULL)
        pull2issue = self.glink_store.get_artifact_set(GArtifactType.PULL, GArtifactType.ISSUE)
        transitive_commit2_issue = GLinkProcessor.get_transitive_traces(commit2pull, pull2issue)
        commit2issue = self.glink_store.get_artifact_set(GArtifactType.COMMIT, GArtifactType.ISSUE)
        commit2issue = commit2issue + transitive_commit2_issue
        return commit2issue

    def __create_issue_2_code(self, commit2issue: GArtifactSet[GLink]):
        """
        Creates trace links between issues and code through the commits implementing issue.
        :param commit2issue: Map of commits 2 related issues.
        :return: GArtifactSet containing links.
        """
        commit2files = {}
        for c in self.commits.artifacts:
            commit2files[c.get_id()] = c.files

        glinks = []
        for commit2issue_link in commit2issue.artifacts:
            c_id = commit2issue_link.source
            if c_id not in commit2files:
                continue
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
        :param min_code_length: The min length of the code artifacts to keep.
        :return: Commits with equal or greater content length than minimum.
        """
        long_messages = [a for a in commit_artifact_set.artifacts if
                         len(a.content.split(SPACE)) >= min_artifact_length and len(a.diffs) >= min_code_length]
        return GArtifactSet(long_messages, GArtifactType.COMMIT)

    @staticmethod
    def __clean_commits(commit_artifact_set: GArtifactSet[GCommit], data_cleaner: DataCleaner) -> GArtifactSet[GCommit]:
        """
        Removes redundant text and strips content.
        :param commit_artifact_set: The set of artifacts to clean.
        :param data_cleaner: Cleans the artifact content.
        :return: The cleaned artifacts.
        """
        RepositoryExporter.__clean_content(commit_artifact_set, data_cleaner)
        return commit_artifact_set

    @staticmethod
    def __clean_code(code_artifact_set: GArtifactSet[GCodeFile], data_cleaner: DataCleaner) -> GArtifactSet[GCodeFile]:
        """
        Cleans the code bodies.
        :param code_artifact_set: Artifact set of code modules.
        :param data_cleaner: The replacements for cleaning code modules.
        :return: Cleaned code artifact set.
        """
        RepositoryExporter.__clean_content(code_artifact_set, data_cleaner)
        return code_artifact_set

    @staticmethod
    def __clean_issues(issue_artifact_set: GArtifactSet[GIssue], data_cleaner: DataCleaner):
        """
        Cleans the issue title and bodies of given set.
        :param issue_artifact_set: Set of issues to clean.
        :param data_cleaner: Regex cleaning substitutions.
        :return: Cleaned set of issues.
        """
        RepositoryExporter.__clean_content(issue_artifact_set, data_cleaner)
        return issue_artifact_set

    @staticmethod
    def __clean_content(artifact_set: GArtifactSet[Union[GCodeFile, GCommit, GIssue]], data_cleaner: DataCleaner) -> None:
        """
        Cleans the content of artifact set by applying substitutions.
        :param artifact_set: The set of artifact to clean.
        :param data_cleaner: The set of regex replacements.
        :return: None
        """
        for a in artifact_set.artifacts:
            a.clean_content(lambda s: data_cleaner.run([s])[0])

    @staticmethod
    def __create_regex_data_cleaner(regex_replacements: Dict) -> DataCleaner:
        """
        Constructs data cleaner performing regex replacements.
        :param regex_replacements: The regex substitutions.
        :return: The data cleaner.
        """
        return DataCleaner(steps=[RegexReplacementStep(regex_replacements)])
