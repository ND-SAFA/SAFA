import os
from typing import Dict, Tuple

from util.file_util import FileUtil


class SafaFormat:
    TIM_FILE = "tim.json"
    DATAFILES_KEY = "datafiles"
    ARTIFACT_ID = "id"
    SAFA_CVS_ARTIFACT_TOKEN = "content"
    SAFA_JSON_ARTIFACT_TOKEN = "body"
    SOURCE_ID = "source"
    TARGET_ID = "target"
    ARTIFACTS = "artifacts"
    TRACES = "traces"
    SUPPORTED_EXTENSIONS = [".json", ".csv"]

    def __init__(self, project_path: str, artifact_token_key: str = SAFA_CVS_ARTIFACT_TOKEN,
                 source_id_key: str = SOURCE_ID,
                 target_id_key: str = TARGET_ID, artifacts_key: str = ARTIFACTS, traces_key: str = TRACES,
                 trace_files_2_artifacts=None):
        self.project_path = project_path
        self.artifact_token_key = artifact_token_key
        self.source_id_key = source_id_key
        self.target_id_key = target_id_key
        self.artifacts_key = artifacts_key
        self.traces_key = traces_key
        self.trace_files_2_artifacts = self.read_project_definition() if not trace_files_2_artifacts else trace_files_2_artifacts

    def read_project_definition(self):
        tim_file_path = os.path.join(self.project_path, self.TIM_FILE)
        project_definition = FileUtil.read_json_file(tim_file_path)
        name2artifact = self.read_data_files(project_definition.pop("DataFiles"))
        trace2artifacts: Dict[str, Tuple[str, str]] = {}
        for key, definition in project_definition.items():
            if key.lower() == self.DATAFILES_KEY:
                continue
            source = definition["Source"]
            target = definition["Target"]
            file = definition["File"]
            trace2artifacts[file] = (name2artifact[source], name2artifact[target])
        return trace2artifacts

    @staticmethod
    def read_data_files(data_files: Dict) -> Dict[str, str]:
        """
        Creates mapping between artifact names and their files.
        :param data_files: Definition for all data files.
        :return: Mapping between artifact names and their definition file names.
        """
        name2artifact = {}
        for artifact_name, artifact_definition in data_files.items():
            name2artifact[artifact_name] = artifact_definition["File"]
        return name2artifact

    def get_artifact_token(self, data_file_name: str):
        supported_formats = [(self.SAFA_CVS_ARTIFACT_TOKEN, ".csv"), (self.SAFA_JSON_ARTIFACT_TOKEN, ".json")]
        for token, identifier in supported_formats:
            if identifier in data_file_name:
                return token
        supported_format_names = list(map(lambda f: f[1], supported_formats))
        raise Exception(data_file_name, "does not have a supported file type: ", supported_format_names)

    def get_artifact_id(self, data_file_name: str):
        supported_ids = [(".json", "name"), (".csv", "id")]
        for extension, key in supported_ids:
            if extension in data_file_name:
                return key
        supported_format_names = [ext for ext, key in supported_ids]
        raise Exception(data_file_name, "does not have a supported file type: ", supported_format_names)
