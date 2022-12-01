from typing import Dict, Tuple

from data.formats.safa_format import SafaFormat


class RepositoryFormat(SafaFormat):
    ISSUE_FILE_NAME = "issue.csv"
    PULL_FILE_NAME = "pull.csv"
    COMMIT_FILE_NAME = "commit.csv"
    COMMIT2ISSUE_FILE_NAME = "commit2issue.csv"
    PULL2ISSUE_FILE_NAME = "pull2issue.csv"
    ARTIFACT_TOKEN = "content"
    ARTIFACT_ID = "id"
    SOURCE_ID = "source"
    TARGET_ID = "target"
    TRACE_FILE_2_ARTIFACTS = {COMMIT2ISSUE_FILE_NAME: (COMMIT_FILE_NAME, ISSUE_FILE_NAME),
                              PULL2ISSUE_FILE_NAME: (PULL_FILE_NAME, ISSUE_FILE_NAME)}

    def __init__(self, artifact_id_key: str = ARTIFACT_ID, artifact_token_key: str = ARTIFACT_TOKEN,
                 source_id_key: str = SOURCE_ID,
                 target_id_key: str = TARGET_ID, artifacts_key: str = '', traces_key: str = '',
                 trace_files_2_artifacts: Dict[str, Tuple[str, str]] = None):
        super().__init__(artifact_id_key, artifact_token_key, source_id_key, target_id_key, artifacts_key, traces_key,
                         trace_files_2_artifacts=trace_files_2_artifacts if trace_files_2_artifacts else
                         RepositoryFormat.TRACE_FILE_2_ARTIFACTS)
