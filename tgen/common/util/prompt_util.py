from typing import List, Any

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE, SPACE, TAB
from tgen.common.util.str_util import StrUtil


class PromptUtil:
    """
    Contains utility methods for creating prompts.
    """

    @staticmethod
    def create_xml_opening(tag_name: str):
        """
        Creates an opening xml tag.
        :param tag_name: The name of the tag.
        :return: The opening tag.
        """
        return f"<{tag_name}>"

    @staticmethod
    def create_xml_closing(tag_name: str):
        """
        Creates an opening xml tag.
        :param tag_name: The name of the tag.
        :return: The opening tag.
        """
        return f"</{tag_name}>"

    @staticmethod
    def create_xml(tag_name: str, tag_content: str = EMPTY_STRING, prefix: str = None, suffix: str = None) -> str:
        """
        Creates xml as follows: <[tag_name]>tag_content</[tag_name]>
        :param tag_name: The name of the tag
        :param tag_content: The content inside of the tag
        :param prefix: The prefix to add to the final string.
        :param suffix: The suffix to append to the final string.
        :return: The formatted xml
        """
        prefix = prefix if prefix else EMPTY_STRING
        suffix = suffix if suffix else EMPTY_STRING
        opening_tag = PromptUtil.create_xml_opening(tag_name)
        closing_tag = PromptUtil.create_xml_closing(tag_name)
        return f"{prefix}{opening_tag}{tag_content}{closing_tag}{suffix}"

    @staticmethod
    def as_markdown_italics(original_string: str) -> str:
        """
        Formats the string as markdown italics
        :param original_string: The string to format
        :return: The string formatted as markdown
        """
        return f"*{original_string}*"

    @staticmethod
    def as_markdown_bold(original_string: str) -> str:
        """
        Formats the string as markdown bold
        :param original_string: The string to format
        :return: The string formatted as markdown
        """
        return f"**{original_string}**"

    @staticmethod
    def as_blockquote(original_string: str) -> str:
        """
        Formats the string as markdown blockquote
        :param original_string: The string to format
        :return: The string formatted as markdown
        """
        return f">{original_string}"

    @staticmethod
    def as_markdown_header(original_string: str, level: int = 1) -> str:
        """
        Formats the string as markdown header
        :param original_string: The string to format
        :param level: The level of the header
        :return: The string formatted as markdown
        """
        return f"{'#' * level} {original_string}"

    @staticmethod
    def as_bullet_point(original_string: str, level: int = 1) -> str:
        """
        Formats the string as markdown bullet
        :param original_string: The string to format
        :param level: The level of the bullet point
        :return: The string formatted as markdown
        """
        bullets = ['*', '-', '+']
        level -= 1
        return f"{TAB * level}{bullets[level % 3]} {original_string}"

    @staticmethod
    def indent_for_markdown(original_string: str, level: int = 1) -> str:
        """
        Formats the string as indented in markdown
        :param original_string: The string to format
        :param level: The indentation level.
        :return: The string indented as markdown
        """
        markdown_tab = "    "
        return f"{level * markdown_tab}{original_string}"

    @staticmethod
    def markdown_divider() -> str:
        """
        Creates a markdown divider
        :return: The markdown divider
        """
        return "---------------"

    @staticmethod
    def strip_new_lines_and_extra_space(original_string: str, remove_all_new_lines: bool = False) -> str:
        """
        Removes new lines and extra leading or trailing spaces from the string
        :param original_string: The original string
        :param remove_all_new_lines: If True, removes new lines even if they are in the middle of the string
        :return: The string without new lines or leading or trailing spaces
        """
        formatted_string = original_string.strip(NEW_LINE).strip()
        if remove_all_new_lines:
            formatted_string = formatted_string.replace(NEW_LINE, SPACE)
        return formatted_string

    @staticmethod
    def format_options(options: List[Any], conjunction: str = "or"):
        """
        Formats the options so the LLM can understand.
        :param options: The list of options
        :param conjunction: Joins the last option e.g. and, or and/or.
        :return: The options as a readable string.
        """
        format_symbol = StrUtil.get_format_symbol()
        options_format = f"{format_symbol}, " * (len(options) - 1)
        options_format += f"{conjunction} {format_symbol}"
        formatted_categories = options_format.format(*options)
        return formatted_categories
