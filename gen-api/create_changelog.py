import os
import subprocess
import sys

from packaging import version

sys.path.append("../tgen")

from tgen.common.logging.logger_manager import logger
from tgen.common.util.file_util import FileUtil


def get_latest_version_from_changelog(directory):
    """
    Determines the latest version number based on files in the specified directory.
    :param directory: The path to directory to search within.
    Returns the next patch version.
    """
    versions = []
    for file in os.listdir(directory):
        if file.endswith(".md"):
            try:
                file_version = file.replace('changelog_', '').replace('.md', '')
                versions.append(version.parse(file_version))
            except ValueError:
                continue
    if not versions:
        raise Exception(f"Found no versions in {directory}")

    latest_version = str(max(versions))
    major, minor, patch = [int(x) for x in latest_version.split('.')]
    previous_version = f"{major}.{minor}.{patch}"
    new_version = f"{major}.{minor}.{patch + 1}"
    return previous_version, new_version


def get_last_changelog_commit(file_pattern) -> str:
    """
    Get the last commit hash for changes to files matching the file_pattern.
    :param file_pattern: File pattern used to match commits whose files where affected.
    :return: The lastest commit ID whose affected files match pattern.
    """
    last_commit = subprocess.check_output(
        ["git", "log", "-1", "--format=%H", "--", file_pattern],
        stderr=subprocess.STDOUT
    ).decode('utf-8').strip()
    return last_commit


def get_commit_messages_since(last_commit: str):
    """
    Get all commit messages since the specified commit hash.
    :param last_commit: ID of last commit.
    :return: List of commits since last commit.
    """
    commits = subprocess.check_output(
        ["git", "log", f"{last_commit}..HEAD", "--pretty=format:%s"],
        stderr=subprocess.STDOUT
    ).decode('utf-8').split('\n')
    commits = [c for c in commits if len(c.strip()) > 0]
    return commits


def create_commit_message() -> None:
    """
    Create a commit message file for the given version, including all commit messages since the last version.
    :param version_str: The version of the file to create.
    :return: None
    """
    previous_version, new_version = get_latest_version_from_changelog("changelog")
    new_file_name = f"changelog/{new_version}.md"  # Adjust the path as necessary.
    previous_file_name = f"changelog/{previous_version}.md"

    last_commit = get_last_changelog_commit(previous_file_name)
    messages = get_commit_messages_since(last_commit)

    if len(messages) > 0:
        file_content = "\n".join([f"- {m}" for m in messages])
        FileUtil.write(file_content, new_file_name)
        logger.info(f"Created new changelog: {new_file_name}")
    else:
        print("No new commits found.")


if __name__ == "__main__":
    create_commit_message()
