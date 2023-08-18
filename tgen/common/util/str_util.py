import re
import uuid

from tgen.constants.deliminator_constants import EMPTY_STRING, UNDERSCORE


class StrUtil:

    @staticmethod
    def format_selective(string, *args: object, **kwargs: object) -> str:
        """
        A replacement for the string format to allow the formatting of only selective fields
        :param string: The string to format
        :param args: Ordered params to format the prompt with
        :param kwargs: Key, value pairs to format the prompt with
        :return: The formatted str
        """
        if not args and not kwargs:
            return string
        formatting_fields = re.findall(r'\{(\w*)\}', string)
        updated_args = [arg for arg in args]
        for i, field in enumerate(formatting_fields):
            if kwargs and field not in kwargs:
                kwargs[field] = '{%s}' % field
            if args and i >= len(args):
                updated_args.append('{%s}' % field)
        return string.format(*updated_args, **kwargs)

    @staticmethod
    def is_uuid(input_string: str) -> bool:
        """
        Returns true if given string is uuid. False otherwise.
        :param input_string: The string to analyze.
        :return: True if uuid, false otherwise.
        """
        try:
            uuid_obj = uuid.UUID(input_string)
            return str(uuid_obj) == input_string
        except ValueError:
            return False

    @staticmethod
    def snake_case_to_pascal_case(snake_case: str) -> str:
        """
        Converts a snake case string to pascal
        :param snake_case: String as snake case
        :return: The string as pascal case
        """
        return EMPTY_STRING.join([word.capitalize() for word in snake_case.split(UNDERSCORE)])
