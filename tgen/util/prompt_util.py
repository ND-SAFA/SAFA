from tgen.constants.deliminator_constants import EMPTY_STRING


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