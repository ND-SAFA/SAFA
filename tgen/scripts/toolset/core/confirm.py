def confirm(confirm_question: str = None):
    """
    Confirms with the user.
    :param confirm_question: The prompt to show the user.
    """
    if confirm_question is None:
        confirm_question = "Confirm?"
    confirm_prompt = f"{confirm_question} (Yes/No):"
    confirm_response = input(confirm_prompt)
    if "y" in confirm_response.lower():
        return True
    elif "n" in confirm_response.lower():
        return False
    else:
        raise Exception(f"Unable to parse response: {confirm_question}")
