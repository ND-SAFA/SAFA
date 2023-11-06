from tgen.scripts.constants import CONFIRM_MESSAGE_DEFAULT, CONFIRM_NEG, CONFIRM_OPTIONS, CONFIRM_PARSE_ERROR, CONFIRM_POS


def confirm(confirm_question: str = CONFIRM_MESSAGE_DEFAULT):
    """
    Confirms with the user.
    :param confirm_question: The prompt to show the user.
    """
    confirm_prompt = f"{confirm_question} {CONFIRM_OPTIONS}:"
    confirm_response = input(confirm_prompt)
    if CONFIRM_POS in confirm_response.lower():
        return True
    elif CONFIRM_NEG in confirm_response.lower():
        return False
    else:
        raise Exception(CONFIRM_PARSE_ERROR.format(confirm_question))
