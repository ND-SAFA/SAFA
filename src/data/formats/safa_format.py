import os
from typing import Dict, Tuple

from util.file_util import FileUtil


class SafaFormat:
    TIM_FILE = "tim.json"
    DATAFILES_KEY = "datafiles"
    ARTIFACT_ID = "id"
    ARTIFACT_TOKEN = "content"
    SOURCE_ID = "source"
    TARGET_ID = "target"
    ARTIFACTS = "artifacts"
    TRACES = "traces"

    def __init__(self, project_path: str,
                 artifact_id_key: str = ARTIFACT_ID, artifact_token_key: str = ARTIFACT_TOKEN,
                 source_id_key: str = SOURCE_ID,
                 target_id_key: str = TARGET_ID, artifacts_key: str = ARTIFACTS, traces_key: str = TRACES):
        self.project_path = project_path
        self.artifact_id_key = artifact_id_key
        self.artifact_token_key = artifact_token_key
        self.source_id_key = source_id_key
        self.target_id_key = target_id_key
        self.artifacts_key = artifacts_key
        self.traces_key = traces_key
        self.trace_files_2_artifacts = self.read_project_definition()

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
