import os
from copy import deepcopy
from typing import List, Dict, Generator

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.common.constants.project_summary_constants import DEFAULT_PROJECT_SUMMARY_SECTIONS, DEFAULT_PROJECT_SUMMARY_SECTIONS_DISPLAY_ORDER, \
    PS_DEFAULT_SAVE_PROGRESS, PS_FILE_NAME, PS_STATE_FILE_NAME
from tgen.common.util.file_util import FileUtil
from tgen.common.util.json_util import JsonUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.project_summary_prompts import PROJECT_SUMMARY_MAP
from tgen.summarizer.summarizer_args import SummarizerArgs


class ProjectSummary:
    def __init__(self, summary_args: SummarizerArgs, export_dir: str = None, save_progress: bool = PS_DEFAULT_SAVE_PROGRESS,
                 project_summary_file_name: str = PS_FILE_NAME, state_file_name: str = PS_STATE_FILE_NAME):
        """
        Constructs project summary to save at export path.
        :param summary_args: The args for the summary
        :param export_dir: The path to the directory to export to.
        :param project_summary_file_name: The name of the file to save summary to.
        :param save_progress: Whether to save anytime there are changes to the project summary.
        """
        self.ps_state = {}
        self.export_dir = export_dir
        self.save_progress = save_progress
        self.ps_file_name = project_summary_file_name
        self.state_file_name = state_file_name
        self.args = summary_args

    def get_generation_iterator(self) -> Generator:
        """
        Creates iterator for section titles and questions.
        :return: Iterator for each title and prompt.
        """
        for section_title in self.args.project_summary_sections:
            section_prompt = self.get_section_prompt_by_title(section_title)
            yield section_title, section_prompt

    def get_section_prompt_by_title(self, title: str) -> QuestionnairePrompt:
        """
        Gets the prompt for creating the section by its title
        :param title: The title of the section
        :return: The prompt for creating the section
        """
        section_prompt = PROJECT_SUMMARY_MAP.get(title, None)
        if not section_prompt:
            assert title in self.args.new_sections, f"Must provide the prompt to use for creating the section: {title}"
            section_prompt = self.args.new_sections[title]
        return section_prompt

    def set_section_body(self, section_id: str, title: str, body: str) -> None:
        """
        Sets the body of a project section.
        :param section_id: The id for the section (generally the same as the title)
        :param title: The title of a section.
        :param body: The body of the section.
        :return: None
        """
        self.ps_state[section_id] = (title, body)
        if self.save_progress:
            self.save()

    def get_summary(self, raise_exception_on_not_found: bool = False) -> str:
        """
        Creates summary in the order of the headers given.
        :param raise_exception_on_not_found: Whether to raise an error if a header if not in the map.
        :return: String representing project summary.
        """
        summary = EMPTY_STRING
        ordered_sections = set(self.args.section_order)
        unorder_sections = [section for section in self.args.project_summary_sections if section not in ordered_sections]
        section_order = self.args.section_order + unorder_sections
        for section_id in section_order:
            if section_id in self.ps_state:
                section_title, section_body = self.ps_state[section_id]
                section = f"{PromptUtil.as_markdown_header(section_title)}{NEW_LINE}{section_body}"
                if len(summary) > 0:
                    section = NEW_LINE + section
                summary += section
            else:
                if raise_exception_on_not_found and section_id in self.args.project_summary_sections:
                    raise Exception(f"Header {section_id} is not in: {self.ps_state}")

        return summary.strip().strip(NEW_LINE)

    def has_summary(self) -> bool:
        """
        :return: Returns whether summary has any content.
        """
        return len(self.ps_state) > 0

    def save(self) -> None:
        """
        Saves the project summary and state to the export directory.
        :return: None
        """
        if self.export_dir:
            summary = self.get_summary()
            ps_file_path = os.path.join(self.export_dir, self.ps_file_name)
            ps_state_path = os.path.join(self.export_dir, self.state_file_name)

            FileUtil.write(summary, ps_file_path)
            FileUtil.write(self.ps_state, ps_state_path)

    def load(self, load_dir: str = None) -> None:
        """
        Loads project summary from the directory.
        :param load_dir: Path to directory containing project summary.
        :return: None
        """
        if load_dir is None:
            load_dir = self.export_dir
        ps_state_path = os.path.join(load_dir, self.state_file_name)
        self.ps_state = JsonUtil.read_json_file(ps_state_path)
