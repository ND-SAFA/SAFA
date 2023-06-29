import re
from typing import Dict, List, Union

from bs4 import BeautifulSoup, Tag

from tgen.util.logging.logger_manager import logger


class LLMResponseUtil:

    @staticmethod
    def parse(res: str, tag_name: str, is_nested: bool = False, raise_exception: bool = False) -> Union[List[str], List[Tag]]:
        """
        Parses the LLM response for the given html tags
        :param res: The LLM response
        :param tag_name: The name of the tag to find
        :param is_nested: If True, the response contains nested tags so all Tag objects are returned, else just the single content
        :param raise_exception: if True, raises an exception if parsing fails
        :return: Either a list of tags (if nested) or the content inside the tag (not nested)
        """
        tags = BeautifulSoup(res, features="lxml").findAll(tag_name)

        try:
            assert len(tags) > 0, f"Missing expected tag {tag_name}"
            content = [tag.contents[0] for tag in tags] if not is_nested else tags
        except (AssertionError, IndexError):
            error = f"Unable to parse {res}"
            logger.exception(error)
            if raise_exception:
                raise Exception(error)
            content = res if not is_nested else []
        return content

    @staticmethod
    def extract_labels(r: str, labels2props: Union[Dict, List]) -> Dict:
        """
        Extracts XML labels from response.
        :param r: The text response.
        :param labels2props: Dictionary mapping XML property name to export prop name.
        :return: Dictionary of prop names to values.
        """
        if isinstance(labels2props, list):
            labels2props = {label: label for label in labels2props}
        props = {}
        for tag, prop in labels2props.items():
            try:
                prop_value = LLMResponseUtil.parse(r, tag, raise_exception=True)
            except Exception:
                prop_value = []
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
