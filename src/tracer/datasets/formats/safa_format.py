from typing import Dict, Tuple


class SafaFormat:
    SAFETY_GOALS_FILE = "sg.json"
    SYSTEM_REQUIREMENTS_FILE = "SYS.json"
    FUNCTIONAL_REQUIREMENTS_FILE = "fsr.json"
    SOFTWARE_REQUIREMENTS_FILE = "swr.json"
    HARDWARE_REQUIREMENTS_FILE = "hwr.json"
    FR2SG_FILE = "fsr2sg.json"
    SR2FR_FILE = "SYS2fsr.json"
    SWR2SR_FILE = "swr2SYS.json"
    HWR2SR_FILE = "hwr2SYS.json"

    ARTIFACT_ID = "name"
    ARTIFACT_TOKEN = "body"
    SOURCE_ID = "sourceName"
    TARGET_ID = "targetName"
    ARTIFACTS = "artifacts"
    TRACES = "traces"

    TRACE_FILES_2_ARTIFACTS = {FR2SG_FILE: (FUNCTIONAL_REQUIREMENTS_FILE, SAFETY_GOALS_FILE),
                               SR2FR_FILE: (
                                   SYSTEM_REQUIREMENTS_FILE, FUNCTIONAL_REQUIREMENTS_FILE),
                               SWR2SR_FILE: (
                                   SOFTWARE_REQUIREMENTS_FILE, SYSTEM_REQUIREMENTS_FILE),
                               HWR2SR_FILE: (
                                   HARDWARE_REQUIREMENTS_FILE, SYSTEM_REQUIREMENTS_FILE)}

    def __init__(self, artifact_id_key: str = ARTIFACT_ID, artifact_token_key: str = ARTIFACT_TOKEN,
                 source_id_key: str = SOURCE_ID,
                 target_id_key: str = TARGET_ID, artifacts_key: str = ARTIFACTS, traces_key: str = TRACES,
                 trace_files_2_artifacts: Dict[str, Tuple[str, str]] = None):
        self.artifact_id_key = artifact_id_key
        self.artifact_token_key = artifact_token_key
        self.source_id_key = source_id_key
        self.target_id_key = target_id_key
        self.artifacts_key = artifacts_key
        self.traces_key = traces_key
        self.trace_files_2_artifacts = trace_files_2_artifacts if trace_files_2_artifacts else SafaFormat.TRACE_FILES_2_ARTIFACTS
