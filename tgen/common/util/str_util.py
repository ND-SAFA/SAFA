import re
import string
import uuid
from typing import List, Union, Set, Dict, Tuple

from nltk.corpus import stopwords

from tgen.common.constants.deliminator_constants import EMPTY_STRING, UNDERSCORE, PERIOD, SPACE, DASH
from tgen.common.logging.logger_manager import logger


class StrUtil:
    FIND_FLOAT_PATTERN = r"\s+\d+\.\d+\s*$|^\s+\d+\.\d+\s+|(?<=\s)\d+\.\d+(?=\s)"
    STOP_WORDS = set(stopwords.words('english'))

    @staticmethod
    def get_letter_from_number(number: int, lower_case: bool = False) -> str:
        """
        Gets the letter in the alphabet in the given number position.
        :param number: Position of letter in alphabet.
        :param lower_case: If True, returns the lower case letter.
        :return:  The letter in the alphabet in the given number position.
        """
        alpha = string.ascii_lowercase if lower_case else string.ascii_uppercase
        return alpha[number % len(alpha)]

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
        if not formatting_fields:
            return string
        updated_args = [arg for arg in args]
        updated_kwargs = {}
        for i, field in enumerate(formatting_fields):
            replacement = StrUtil.get_format_symbol(field)
            if field:
                if field in kwargs:
                    updated_kwargs[field] = kwargs[field]
                else:
                    updated_kwargs[field] = replacement
            if not field and i >= len(updated_args):
                updated_args.append(replacement)
        try:
            string = string.format(*updated_args, **updated_kwargs)
        except Exception:
            logger.exception(f"Unable to format {string} with args={updated_args} and kwargs={updated_kwargs}")
        return string

    @staticmethod
    def fill_with_format_variable_name(string_: str, variable_name: str, count: int = -1) -> str:
        """
        Updates the format symbol in the string to include the variable name for use with the format map.
        :param string_: The string to update.
        :param variable_name: The name of the format variable.
        :param count: Number of replacements to make (-1 is all).
        :return: The string with the format symbol and variable name for use with the format map.
        """
        return string_.replace(StrUtil.get_format_symbol(), StrUtil.get_format_symbol(variable_name), count)

    @staticmethod
    def get_format_symbol(var_name: str = EMPTY_STRING) -> str:
        """
        Gets the symbol for formatting strings '{}'.
        :param var_name: If provided, places the variable name in the brackets for use with the format map.
        :return: The symbol for formatting strings.
        """
        return '{%s}' % var_name

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

    @staticmethod
    def split_sentences_by_punctuation(string: str, punctuation: str = PERIOD) -> List[str]:
        """
        Splits sentences by end of sentence punctuation
        :param string: The string to split
        :param punctuation: The type of punctuation to split on
        :return: The string split into sentences
        """
        regex = fr"(?<={re.escape(punctuation)}) "
        sentences = re.split(regex, string)
        return [sentence.strip(punctuation) for sentence in sentences]

    @staticmethod
    def remove_floats(string: str) -> str:
        """
        Remove all floats in a string if they are by themselves (not inside of a substring)
        :param string: The string to find floats
        :return: The string without floats that were found
        """
        return re.compile(StrUtil.FIND_FLOAT_PATTERN).sub(EMPTY_STRING, string)

    @staticmethod
    def find_floats(string: str) -> List[str]:
        """
        Finds all floats in a string if they are by themselves (not inside of a substring)
        :param string: The string to find floats
        :return: The floats that were found
        """
        return re.findall(StrUtil.FIND_FLOAT_PATTERN, string)

    @staticmethod
    def remove_substrings(input_string: str, sub_string2remove: Union[List[str], str]) -> str:
        """
        Removes all characters from the string
        :param input_string: The string to remove characters from
        :param sub_string2remove: The characters to remove
        :return: The string without the characters
        """
        if not isinstance(sub_string2remove, list):
            sub_string2remove = [sub_string2remove]
        for char in sub_string2remove:
            input_string = input_string.replace(char, EMPTY_STRING)
        return input_string

    @staticmethod
    def remove_decimal_points_from_floats(string: str) -> str:
        """
        Removes all decimal points from each float in the string
        :param string: The input string
        :return: The string without decimal points
        """
        # Define a regular expression pattern to match floating-point numbers
        return re.sub(r'\d+\.\d+', lambda x: x.group().split(PERIOD)[0], string)

    @staticmethod
    def convert_all_items_to_string(iterable: Union[List, Set, Dict], keys_only: bool = False) -> Union[List, Set, Dict]:
        """
        Converts all values to string.
        :param iterable: An iterable containing values to convert.
        :param keys_only: If True, only converts the keys in the dictionary, else values too.
        :return: The iterable with converted values.
        """
        if isinstance(iterable, list) or isinstance(iterable, set):
            converted = [str(item) for item in iterable]
            converted = type(iterable)(converted) if not isinstance(converted, type(iterable)) else converted
        elif isinstance(iterable, dict):
            converted = {str(k): (v if keys_only else str(v)) for k, v in iterable.items()}
        else:
            raise NotImplemented(f"Cannot perform conversion for {type(iterable)}")
        return converted

    @staticmethod
    def remove_substring(input_string: str, str2remove: str, only_if_startswith: bool = False,
                         only_if_endswith: bool = False) -> str:
        """
        Removes a substring from a string.
        :param input_string: The string to remove substring from.
        :param str2remove: The sub-string to remove.
        :param only_if_startswith: If True, only removes from start of string.
        :param only_if_endswith: If True, only removes from end of string.
        :return: The string without the substring.
        """
        assert not (only_if_startswith and only_if_endswith), "Cannot be only if startswith and only if endswith."
        pattern = f"{re.escape(str2remove)}"
        if only_if_startswith:
            pattern = f"^{pattern}"
        elif only_if_endswith:
            pattern = f"{pattern}$"
        pattern = re.compile(pattern)
        result = pattern.sub(EMPTY_STRING, input_string)
        return result

    @staticmethod
    def separate_camel_case(input_string: str):
        """
        Finds words written in camel casing and separates them into individual words.
        :param input_string: The string to split camel case words.
        :return: Processed string.
        """
        split_doc = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", input_string)).split()
        return SPACE.join(split_doc)

    @staticmethod
    def separate_joined_words(input_string: str, deliminators: List = None):
        """
        Splits camel case, snake case, and pascal case words.
        :param input_string: The string to split.
        :param deliminators: Deliminators to split on.
        :return: Processed string.
        """
        if deliminators is None:
            deliminators = [DASH, UNDERSCORE]
        processed_string = StrUtil.separate_camel_case(input_string)
        for d in deliminators:
            processed_string = SPACE.join(processed_string.split(d))
        return processed_string

    @staticmethod
    def remove_stop_words(input_string: str) -> str:
        """
        Removes the stop words in the string.
        :param input_string: The string to remove stopwords from.
        :return: The string without stop words.
        """
        return SPACE.join([word for word in input_string.split() if word.lower() not in StrUtil.STOP_WORDS])

    @staticmethod
    def split_by_punctuation(input_string: str) -> List[str]:
        """
        Splits a string by punctuation.
        :param input_string: The string to split.
        :return: List of substrings, divided using the punctuation.
        """
        input_string += SPACE
        pattern = re.compile(r'[.!?;]+ ')
        return [line.strip() for line in re.split(pattern, input_string) if line.strip()]

    @staticmethod
    def find_start_and_end_loc(main_string: str, string2find: str,
                               ignore_case: bool = False,
                               start: int = 0, end: int = None) -> Tuple[int, int]:
        """
        Finds the start and end location of the concept.
        :param main_string: The artifact content to find concept in.
        :param string2find: The concept to find.
        :param ignore_case: If True, makes everything lower case.
        :param start: The index to start at.
        :param end: The index to end at.
        :return: The start and end location of the concept.
        """
        if ignore_case:
            main_string = main_string.lower()
            string2find = string2find.lower()
        end = len(main_string) if end is None else end
        start_index = main_string.find(string2find, start, end)
        end_index = start_index
        if start_index > -1:
            end_index += len(string2find)
        return start_index, end_index
