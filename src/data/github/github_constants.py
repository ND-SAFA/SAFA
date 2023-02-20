import os

# Run
PROJECTS = ["ND-SAFA/fend",
            "Autonomous-Racing-PG/ar-tu-do",
            "ApolloAuto/apollo",
            "autorope/donkeycar",
            "automotive-grade-linux/docs-agl",
            "automotive-grade-linux/docs-sources",
            "pylessard/python-udsoncan",
            "iDoka/awesome-canbus",
            "Marcin214/awesome-automotive",
            "linklayer/pyvit",
            "autoas/as",
            "edmcouncil/auto",
            "eclipse-iceoryx/iceoryx"]

# Artifact paths
COMMIT_ARTIFACT_FILE = "commit.json"
ISSUE_ARTIFACT_FILE = "issue.json"
PULL_ARTIFACT_FILE = "pull.json"
COMMIT2ISSUE_ARTIFACT_FILE = "commit2issue.json"
COMMIT2PULL_ARTIFACT_FILE = "commit2pull.json"
PULL2ISSUE_ARTIFACT_FILE = "pull2issue.json"

# Parsing
EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
GENERIC_COMMIT_HEADERS = ["Merge pull request #.*from.*",
                          "Revert.*of.*",
                          "Merge branch.*of.*"]

# Safa Paths

COMMIT_SAFA_FILE = "commit_file.csv"
ISSUE_SAFA_FILE = "issue_file.csv"
LINK_SAFA_FILE = "link_file.csv"
TRAINING_STAGES = ["test", "train", "valid"]

# Paths
PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
CLONE_PATH = os.path.join(PROJECT_PATH, "clones")
ARTIFACT_PATH = os.path.join(PROJECT_PATH, "artifacts")
SAFA_PATH = os.path.join(PROJECT_PATH, "safa")

# Code Paths
SRC_PATH = os.path.join(PROJECT_PATH, "src")

# Post-processing
MIN_ARTIFACT_LENGTH = 10
