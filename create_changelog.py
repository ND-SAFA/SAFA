import os
import subprocess

from packaging import version


def get_latest_version_from_changelog(directory):
    """
    Determines the latest version number based on files in the specified directory.
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


def get_last_changelog_commit(file_pattern):
    """
    Get the last commit hash for changes to files matching the file_pattern.
    """
    try:
        last_commit = subprocess.check_output(
            ["git", "log", "-1", "--format=%H", "--", file_pattern],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip()
        return last_commit
    except subprocess.CalledProcessError as e:
        print("Error getting last changelog commit:", e.output.decode())
        return None


def get_commit_messages_since(last_commit):
    """
    Get all commit messages since the specified commit hash.
    """
    try:
        commits = subprocess.check_output(
            ["git", "log", f"{last_commit}..HEAD", "--pretty=format:%s"],
            stderr=subprocess.STDOUT
        ).decode('utf-8').split('\n')
        return commits
    except subprocess.CalledProcessError as e:
        print("Error getting commit messages:", e.output.decode())
        return []


def create_changelog_file(version, messages, file_path):
    """
    Create a changelog file from a list of commit messages.
    """
    with open(file_path, 'w') as file:
        file.write(f"# Changelog for Version {version}\n\n")
        for msg in messages:
            file.write(f"- {msg}\n")


def create_commit_message(version):
    """
    Create a commit message file for the given version, including all commit messages since the last version.
    """
    file_pattern = "*.md"  # Adjust this pattern to match your changelog files if needed.
    file_name = f"changelog/{version}.md"  # Adjust the path as necessary.

    last_commit = get_last_changelog_commit(file_pattern)
    if last_commit:
        messages = get_commit_messages_since(last_commit)
        create_changelog_file(version, messages, file_name)
        print(f"Changelog file created for version {version}: {file_name}")
    else:
        print("No new commits found.")


if __name__ == "__main__":
    version = get_latest_version_from_changelog("changelog")
    create_commit_message(version)
