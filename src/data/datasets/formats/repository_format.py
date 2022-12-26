from typing import Dict, Tuple

from data.datasets.formats.safa_format import SafaFormat


class RepositoryFormat(SafaFormat):
    ISSUE_FILE_NAME = "issue.csv"
    PULL_FILE_NAME = "pull.csv"
    COMMIT_FILE_NAME = "commit.csv"
    COMMIT2ISSUE_FILE_NAME = "commit2issue.csv"
    PULL2ISSUE_FILE_NAME = "pull2issue.csv"
    SAFA_CVS_ARTIFACT_TOKEN = "content"
    ARTIFACT_ID = "id"
    SOURCE_ID = "source"
    TARGET_ID = "target"
    TRACE_FILE_2_ARTIFACTS = {COMMIT2ISSUE_FILE_NAME: (COMMIT_FILE_NAME, ISSUE_FILE_NAME),
                              PULL2ISSUE_FILE_NAME: (PULL_FILE_NAME, ISSUE_FILE_NAME)}

    def __init__(self, artifact_id_key: str = ARTIFACT_ID,
                 source_id_key: str = SOURCE_ID,
                 target_id_key: str = TARGET_ID, artifacts_key: str = '', traces_key: str = '',
                 trace_files_2_artifacts: Dict[str, Tuple[str, str]] = None):
        """
        Represents the format for repositories
        :param artifact_id_key: the key to access artifact key
        :param source_id_key: the key to access source id
        :param target_id_key: the key to access target id
        :param artifacts_key: the key to access the artifacts
        :param traces_key: the key to access the trace links
        :param trace_files_2_artifacts: the files mapping artifacts to links
        """
        super().__init__(artifact_id_key, source_id_key, target_id_key, artifacts_key, traces_key,
                         trace_files_2_artifacts=trace_files_2_artifacts if trace_files_2_artifacts else
                         RepositoryFormat.TRACE_FILE_2_ARTIFACTS)
