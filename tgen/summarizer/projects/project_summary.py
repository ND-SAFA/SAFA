import os
from typing import List

from tgen.common.constants.project_summary_constants import PROJECT_SUMMARY_FILE_NAME, PS_DEFAULT_SAVE_PROGRESS
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.supported_prompts.project_summary_prompts import PROJECT_SUMMARY_MAP, \
    PROJECT_SUMMARY_SECTIONS, PROJECT_SUMMARY_SECTIONS_DISPLAY_ORDER


class ProjectSummary:
    def __init__(self, export_dir: str = None, project_summary_file_name: str = PROJECT_SUMMARY_FILE_NAME,
                 save_progress: bool = PS_DEFAULT_SAVE_PROGRESS):
        """
        Constructs project summary to save at export path.
        :param export_dir: The path to the directory to export to.
        :param project_summary_file_name: The name of the file to save summary to.
        :param save_progress: Whether to save anytime there are changes to the project summary.
        """
        self.header_map = {}
        self.export_dir = export_dir
        self.artifact_file_name = project_summary_file_name
        self.save_progress = save_progress

    @staticmethod
    def get_generation_iterator():
        """
        Creates iterator for section titles and questions.
        :return: Iterator for each title and prompt.
        """
        for section_title in PROJECT_SUMMARY_SECTIONS:
            section_prompt = PROJECT_SUMMARY_MAP[section_title]
            yield section_title, section_prompt

    def set_section_body(self, title: str, body: str):
        """
        Sets the body of a project section.
        :param title: The title of a section.
        :param body: The body of the section.
        :return: None
        """
        self.header_map[title] = body
        if self.save_progress:
            self.save()

    def get_summary(self, headers: List[str] = PROJECT_SUMMARY_SECTIONS_DISPLAY_ORDER,
                    raise_exception_on_not_found: bool = False):
        """
        Creates summary in the order of the headers given.
        :param headers: The headers in the order they should appear.
        :param raise_exception_on_not_found: Whether to raise an error if a header if not in the map.
        :return: String representing project summary.
        """
        summary = ""
        for header in headers:
            if header in self.header_map:
                header_body = self.header_map[header]
                summary += f"{PromptUtil.as_markdown_header(header)}\n{header_body}"
            else:
                if raise_exception_on_not_found:
                    raise Exception(f"Header {header} is not in: {self.header_map}")

        return summary.strip()

        summary_export_path = os.path.join(self.export_dir, PROJECT_SUMMARY_FILE_NAME)
        FileUtil.write(summary, summary_export_path)

    def has_summary(self) -> bool:
        """
        :return: Returns whether summary has any content.
        """
        return len(self.header_map) > 0

    def save(self) -> None:
        """
        Saves the project summary to its export path.
        :return: None
        """
        if self.export_dir:
            summary = self.get_summary()
            summary_export_path = os.path.join(self.export_dir, PROJECT_SUMMARY_FILE_NAME)
            FileUtil.write(summary, summary_export_path)
