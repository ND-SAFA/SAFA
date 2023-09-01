import os
from typing import List

from api.server.paths import REPO_PATH
from tgen.common.util.file_util import FileUtil

CHANGELOG = "changelog"
HOMEPAGE_HEADER = "# Welcome to SAFA's generative server"
TGEN_BAR = "-" * 125


class ChangeLog:
    def __init__(self, file_path: str):
        self.version = FileUtil.get_file_base_name(file_path)
        self.description = FileUtil.read_file(file_path)

    def get_content(self) -> str:
        return f"### {self.version}\n{self.description}"


def get_current_version() -> str:
    change_logs = get_change_logs()
    return change_logs[0].version


def get_change_logs() -> List[ChangeLog]:
    change_log_files = os.listdir(os.path.join(REPO_PATH, CHANGELOG))
    change_file_paths = [os.path.join(REPO_PATH, CHANGELOG, c) for c in change_log_files]
    change_logs = [ChangeLog(cp) for cp in change_file_paths]
    change_logs = sorted(change_logs, key=lambda cp: cp.version, reverse=True)
    return change_logs


def get_home_page() -> str:
    change_logs = get_change_logs()
    change_log = "\n".join([cl.get_content() for cl in change_logs])
    home_page = f"{HOMEPAGE_HEADER}\n## Versions\n{change_log}"
    return home_page


def get_api_header() -> str:
    change_logs = get_change_logs()
    api_header = f"{TGEN_BAR}\n{HOMEPAGE_HEADER}\nRunning version {change_logs[0].version}\n{TGEN_BAR}\n"
    return api_header
