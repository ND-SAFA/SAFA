import re
from typing import Dict, List, Union

from bs4 import BeautifulSoup, Tag

from tgen.util.logging.logger_manager import logger


class LLMResponseUtil:

    @staticmethod
    def parse(res: str, tag_name: str, many: bool = False) -> Union[str, List[Tag]]:
        """
        Parses the LLM response for the given html tags
        :param res: The LLM response
        :param tag_name: The name of the tag to find
        :param many: If True, the response contains sibling and nested tags and  Tag objects are returned. Otherwise, just the single content
        :return: Either a list of tags (if nested) or the content inside the tag (not nested)
        """
        tags = BeautifulSoup(res, features="lxml").findAll(tag_name)

        try:
            assert len(tags) > 0, f"Missing expected tag {tag_name}"
            content = tags[0].contents[0] if not many else tags
        except (AssertionError, IndexError):
            logger.exception(f"Unable to parse {res}")
            content = res if not many else []
        return content

    @staticmethod
    def extract_labels(r: str, labels2props: Dict) -> Dict:
        """
        Extracts XML labels from response.
        :param r: The text response.
        :param labels2props: Dictionary mapping XML property name to export prop name.
        :return: Dictionary of prop names to values.
        """
        props = {}
        for tag, prop in labels2props.items():
            prop_value = LLMResponseUtil.parse(r, tag)
            props[prop] = prop_value
        return props

    @staticmethod
    def strip_non_digits_and_periods(string: str):
        """
        Removes all characters except digits and periods.
        :param string: The str to strip.
        :return: The stripped string.
        """
        pattern = r'[^0-9.]'
        return re.sub(pattern, '', string)
