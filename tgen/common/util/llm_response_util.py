import html
import re
from typing import Dict, List, Union

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString

from tgen.common.util.logging.logger_manager import logger


class LLMResponseUtil:

    @staticmethod
    def parse(res: str, tag_name: str, is_nested: bool = False, raise_exception: bool = False, return_res_on_failure: bool = False) -> \
            List[Union[str, Dict]]:
        """
        Parses the LLM response for the given html tags
        :param res: The LLM response
        :param tag_name: The name of the tag to find
        :param is_nested: If True, the response contains nested tags so all Tag objects are returned, else just the single content
        :param raise_exception: if True, raises an exception if parsing fails
        :param return_res_on_failure: Whether to return original response on failure.
        :return: Either a list of tags (if nested) or the content inside the tag (not nested)
        """
        soup = BeautifulSoup(res, features="lxml")

        try:
            assert tag_name in res, f"Missing expected tag {tag_name}"
            tags = soup.findAll(tag_name)
            if is_nested:
                content = [LLMResponseUtil._parse_children(tag) for tag in tags]
            else:
                content = [tag.contents[0] for tag in tags if len(tag.contents) > 0]
            assert len(content) > 0, f"Found no tags ({tag_name}) in:\n{res}"
        except Exception:
            error = f"Unable to parse {tag_name}"
            logger.exception(error)
            if raise_exception:
                raise Exception(error)
            content = [res] if return_res_on_failure else []
        return [html.unescape(c) for c in content]

    @staticmethod
    def _parse_children(tag: Tag) -> Dict[str, List]:
        """
        Parses all children tags in the given tag
        :param tag: The parent tag
        :return: The children of the tag
        """
        children = {}
        if isinstance(tag, str):
            return tag
        for child in tag.children:
            if isinstance(child, Tag) and child.contents is not None and len(child.contents) > 0:
                tag_name = child.name
                content = child.contents[0]
            elif isinstance(child, NavigableString):
                tag_name = tag.name
                content = child
            else:
                continue
            if tag_name not in children:
                children[tag_name] = []
            children[tag_name].append(content)
        return children

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
