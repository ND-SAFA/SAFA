import os
import subprocess

from packaging import version


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
    if versions:
        latest_version = str(max(versions))
        major, minor, patch = [int(x) for x in latest_version.split('.')]
        return f"{major}.{minor}.{patch + 1}"
    else:
        return "0.0.1"  # Default to start versions if no files are found


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


def create_changelog_file(version, messages, file_path):
    """
    Create a changelog file from a list of commit messages.
    """
    with open(file_path, 'w') as file:
        file.write(f"# Changelog for Version {version}\n\n")
        for msg in messages:
            file.write(f"- {msg}\n")


def create_commit_message(version_str: str) -> None:
    """
    Create a commit message file for the given version, including all commit messages since the last version.
    :param version_str: The version of the file to create.
    :return: None
    """
    file_pattern = "changelog/*.md"  # Adjust this pattern to match your changelog files if needed.
    file_name = f"changelog/{version_str}.md"  # Adjust the path as necessary.

    last_commit = get_last_changelog_commit(file_pattern)
    messages = get_commit_messages_since(last_commit)

    if len(messages) > 0:
        create_changelog_file(version_str, messages, file_name)
        print(f"Changelog file created for version {version_str}: {file_name}")
    else:
        print("No new commits found.")


if __name__ == "__main__":
    version = get_latest_version_from_changelog("changelog")
    create_commit_message(version)
