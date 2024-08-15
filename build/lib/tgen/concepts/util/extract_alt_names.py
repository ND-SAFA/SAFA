from typing import List

from common_resources.tools.constants.symbol_constants import CLOSE_PAREN, EMPTY_STRING, OPEN_PAREN, SPACE


def extract_alternate_names(string_list: List[str]) -> List[List[str]]:
    """
    For each string, extract alternate names defined in parenthesis. For example:
    Advanced Baseline Imager (ABI)
    :param string_list: List of string to parse alternate names for.
    :return: List of tuples where each tuple contains the main name followed by the alternate names.
    """
    result = []

    # Iterate over each string in the list
    for string in string_list:
        main_name = []
        alternate_names = []
        is_in_parenthesis = False
        current_name = []

        # Iterate over each character in the string
        for char in string:
            if char == OPEN_PAREN:
                if not is_in_parenthesis:
                    is_in_parenthesis = True
                    if current_name:
                        # Join the main name and clear the buffer
                        main_name.append("".join(current_name).strip())
                        current_name = []
            elif char == CLOSE_PAREN:
                if is_in_parenthesis:
                    alternate_names.append(EMPTY_STRING.join(current_name).strip())
                    current_name = []
                    is_in_parenthesis = False
            else:
                # Collect characters for the current name
                current_name.append(char)

        # If there's a current name remaining, add it to the main name
        if current_name:
            if is_in_parenthesis:
                alternate_names.append(EMPTY_STRING.join(current_name).strip())
            else:
                main_name.append(EMPTY_STRING.join(current_name).strip())

        # Join main names into a single name and append alternate names
        extracted_names = [SPACE.join(main_name)] + alternate_names
        result.append(extracted_names)

    return result
