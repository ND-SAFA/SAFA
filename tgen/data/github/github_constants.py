def to_csv(file_name: str):
    """
    Converts json file extension to CSV.
    :param file_name: File possibly containing JSON extension.
    :return: File with CSV extension.
    """
    return file_name.replace(".json", ".csv")


# Artifact paths
ISSUE_ARTIFACT_FILE = "issue.json"
PULL_ARTIFACT_FILE = "pull.json"
COMMIT_ARTIFACT_FILE = "commit.json"
COMMIT_DIFF_ARTIFACT_FILE = "commit_diff.json"
CODE_ARTIFACT_FILE = "code.json"

ISSUE_EXPORT_FILE = to_csv(ISSUE_ARTIFACT_FILE)
PULL_EXPORT_FILE = to_csv(PULL_ARTIFACT_FILE)
COMMIT_EXPORT_FILE = to_csv(COMMIT_ARTIFACT_FILE)
COMMIT_DIFF_EXPORT_FILE = to_csv(COMMIT_DIFF_ARTIFACT_FILE)
CODE_EXPORT_FILE = to_csv(CODE_ARTIFACT_FILE)

# Trace Paths
COMMIT2ISSUE_ARTIFACT_FILE = "commit2issue.json"
COMMIT2PULL_ARTIFACT_FILE = "commit2pull.json"
PULL2ISSUE_ARTIFACT_FILE = "pull2issue.json"
CODE2CODE_ARTIFACT_FILE = "code2code.json"

COMMIT2ISSUE_EXPORT_FILE = to_csv(COMMIT2ISSUE_ARTIFACT_FILE)
COMMITDIFF2ISSUE_EXPORT_FILE = "commit_diff2issue.csv"
ISSUE2CODE_EXPORT_FILE = "issue2code.csv"
CODE2CODE_EXPORT_FILE = to_csv(CODE2CODE_ARTIFACT_FILE)

# Parsing
