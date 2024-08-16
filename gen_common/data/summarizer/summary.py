import re
from copy import deepcopy
from enum import Enum
from typing import Dict, List, Union

from gen_common.constants import EMPTY_STRING, NEW_LINE
from gen_common.util import EnumDict, FileUtil, PromptUtil
from gen_common.util.json_util import JsonUtil
from gen_common.util.typed_enum_dict import TypedEnumDict


class SummarySectionKeys(Enum):
    TITLE = "title"
    CHUNKS = "chunks"


class SummarySection(TypedEnumDict, keys=SummarySectionKeys):
    title: str
    chunks: List[str]


class Summary(EnumDict):

    def __init__(self, dict_: Dict[Union[str, Enum], SummarySection] = None, **kwargs):
        """
        Represents a summary with different sections
        :param dict_: Maps id of summary section to the Summary Section obj containing the section title and chunks
        :param kwargs: The dictionary items as kwargs
        """
        super().__init__(dict_, **kwargs)

    def save(self, filepath: str) -> None:
        """
        Saves as json to the desired filepath
        :param filepath: The path to save to
        :return: None
        """
        dirpath = FileUtil.get_directory_path(filepath)
        FileUtil.create_dir_safely(dirpath)
        if filepath.endswith(FileUtil.JSON_EXT):
            JsonUtil.save_to_json_file(self, filepath)
        else:
            FileUtil.write(self.to_string(), filepath)

    @staticmethod
    def load_from_file(filepath: str) -> "Summary":
        """
        Loads from json to the desired filepath
        :param filepath: The path to save to
        :return: The loaded summary
        """
        if filepath.endswith(FileUtil.JSON_EXT):
            json_dict = JsonUtil.read_json_file(filepath)
            summary_dict = {}
            for key, val in json_dict.items():
                JsonUtil.require_properties(val, required_properties=[e.value for e in SummarySectionKeys])
                summary_dict[key] = SummarySection(**val)
            summary = Summary(summary_dict)
        else:
            summary_string = FileUtil.read_file(file_path=filepath, raise_exception=True)
            summary = Summary.from_string(summary_string)
        return summary

    @staticmethod
    def from_string(summary_string: str) -> "Summary":
        """
        Creates a summary object from a string
        :param summary_string: Contains the summary sections
        :return: The summary object
        """
        summary = Summary()
        current_title = None
        sections = re.split(r'\n(#\s.*?)\n', NEW_LINE + summary_string)
        sections.pop(0)
        for i, line in enumerate(sections):
            line = line.strip()
            if not line:
                continue
            match = re.match(r'^(#) (.*)', line)
            if match:
                if len(match.groups()) > 1:
                    current_title = match.group(2)
            elif current_title:
                summary.add_section(section_id=current_title, body=line)
        return summary

    def re_order_sections(self, section_order: List[str] = None,
                          raise_exception_on_not_found: bool = False,
                          remove_unordered_sections: bool = False) -> None:
        """
        Re-orders the sections in the dictionary
        :param section_order: The order that the sections should occur
        :param raise_exception_on_not_found: If True, raises an exception if the section does not exist
        :param remove_unordered_sections: If True, removes any sections that are not in the ordered list
        :return: None
        """
        section_order = deepcopy(section_order)
        section_order.reverse()
        for section_id in section_order:
            if section_id in self:
                self.move_to_end(section_id, last=False)
            else:
                if raise_exception_on_not_found:
                    raise KeyError(f"Header {section_id} is not in summary")
        un_ordered_sections = set(self.keys()).difference(section_order)
        if remove_unordered_sections:
            for section_id in un_ordered_sections:
                self.pop(section_id)

    def to_string(self, section_order: List[str] = None, raise_exception_on_not_found: bool = False) -> str:
        """
        Converts the summary to a string in the order of the headers given.
        :param section_order: The list of section ids in the order they should be viewed
        :param raise_exception_on_not_found: Whether to raise an error if a section does not exist
        :return: String representing the summary.
        """
        section_order = section_order if section_order else list(self.keys())
        summary = EMPTY_STRING
        for section_id in section_order:
            section = self.get(section_id)
            if section:
                title = section[SummarySectionKeys.TITLE]
                body = NEW_LINE.join(section[SummarySectionKeys.CHUNKS])
                formatted_section = f"{PromptUtil.as_markdown_header(title)}{NEW_LINE}{body}"
                if len(summary) > 0:
                    formatted_section = NEW_LINE + formatted_section
                summary += formatted_section
            else:
                if raise_exception_on_not_found:
                    raise KeyError(f"Header {section_id} is not in summary")

        return summary.strip().strip(NEW_LINE)

    def add_section(self, section_id: str, section_title: str = None, body: str = None, chunks: List[str] = None) -> SummarySection:
        """
        Adds a new section to the summary
        :param section_id: The section id
        :param section_title: The section title if different from id
        :param body: The body of the section as a single string
        :param chunks: The chunks making up the body of the section
        :return: The newly created section
        """
        if body:
            chunks = Summary.extract_chunks_from_body(body)
        chunks = chunks if chunks else []
        section_title = section_title if section_title else section_id
        self[section_id] = SummarySection(title=section_title, chunks=chunks)
        return SummarySection(title=section_title, chunks=chunks)

    def add_chunk(self, section_id: str, new_chunk: str) -> None:
        """
        Adds a new chunk to a summary section
        :param section_id: The id of the section
        :param new_chunk: The new chunks to add
        :return: None
        """
        if section_id not in self:
            self.add_section(section_id)
        self[section_id][SummarySectionKeys.CHUNKS].append(new_chunk)

    @staticmethod
    def extract_chunks_from_body(body: str) -> List[str]:
        """
        Breaks the section body into chunks
        :param body: The section body
        :return: A list of chunks making up the section body
        """
        chunks, chunk = [], []
        for line in body.split(NEW_LINE):
            line = line.strip()
            if not line:
                continue
            if re.match(r'^(#*) (.*)', line):
                if chunk:
                    chunks.append(NEW_LINE.join(chunk))
                chunk = [line]
            elif chunk:
                chunk.append(line)
            else:
                chunks.append(line)
        if chunk:
            chunks.append(NEW_LINE.join(chunk))
        return chunks

    def combine_summaries(self, other_summary: "Summary") -> None:
        """
        Adds any sections that are in the other summary but not in this summary
        :param other_summary: The other summary to add from
        :return: None
        """
        for section_id, section in other_summary.items():
            if section_id not in self:
                self[section_id] = section

    def __str__(self) -> str:
        """
        Converts the summary to a string
        :return: The summary as a string
        """
        return self.to_string()
