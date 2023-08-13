from typing import Any

from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE, SPACE


class PromptUtil:
    """
    Contains utility methods for creating prompts.
    """

    @staticmethod
    def create_xml(tag_name: str, tag_content: str = EMPTY_STRING) -> str:
        """
        Creates xml as follows: <[tag_name]>tag_content</[tag_name]>
        :param tag_name: The name of the tag
        :param tag_content: The content inside of the tag
        :return: The formatted xml
        """
        return f"<{tag_name}>{tag_content}</{tag_name}>"

    @staticmethod
    def format_as_markdown_italics(original_string: str) -> str:
        """
        Formats the string as markdown italics
        :param original_string: The string to format
        :return: The string formatted as markdown
        """
        return f"*{original_string}*"

    @staticmethod
    def format_as_markdown(original_string: str, level: int = 1) -> str:
        """
        Formats the string as markdown header
        :param original_string: The string to format
        :param level: The level of the header
        :return: The string formatted as markdown
        """
        return f"{'#' * level} {original_string}"

    @staticmethod
    def strip_new_lines_and_extra_space(original_string) -> str:
        """
        Removes new lines and extra leading or trailing spaces from the string
        :param original_string: The original string
        :return: The string without new lines or leading or trailing spaces
        """
        return original_string.replace(NEW_LINE, SPACE).strip()
