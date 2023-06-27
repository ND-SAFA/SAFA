from typing import List, Union

from bs4 import BeautifulSoup, Tag

from tgen.util.logging.logger_manager import logger


class LLMResponseUtil:

    @staticmethod
    def parse(res: str, tag_name: str, is_nested: bool = False) -> Union[str, List[Tag]]:
        """
        Parses the LLM response for the given html tags
        :param res: The LLM response
        :param tag_name: The name of the tag to find
        :param is_nested: If True, the response contains nested tags so all Tag objects are returned, else just the single content
        :return: Either a list of tags (if nested) or the content inside the tag (not nested)
        """
        tags = BeautifulSoup(res, features="lxml").findAll(tag_name)

        try:
            assert len(tags) > 0, f"Missing expected tag {tag_name}"
            content = tags[0].contents[0] if not is_nested else tags
        except (AssertionError, IndexError):
            logger.exception(f"Unable to parse {res}")
            content = res if not is_nested else []
        return content
