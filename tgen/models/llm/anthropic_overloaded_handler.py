import time

import anthropic
from anthropic import InternalServerError

from tgen.common.constants.environment_constants import ANTHROPIC_KEY
from tgen.common.logging.logger_manager import logger
from tgen.common.threading.threading_state import MultiThreadState

ANTHROPIC_OVERLOADED_SLEEP_TIME = 1000
ANTHROPIC_OVERLOADED_TIMEOUT = 1200


def anthropic_overloaded_handler(state: MultiThreadState, e: Exception) -> bool:
    """
    If anthropic overloaded error is detected, pauses state until anthropic is back up.
    :param state: The multi-threaded state controlling requests to anthropic.
    :param e: The exception happening within anthropic.
    :return: None
    """
    if _is_overloaded_error(e):
        logger.info("Anthropic is currently overloaded. Pausing work and resuming once anthropic comes back online.")
        state.pause_work = True
        _wait_until_online()
        state.pause_work = False
        return True
    return False


def _wait_until_online(timeout: float = ANTHROPIC_OVERLOADED_TIMEOUT) -> None:
    """
    Waits until Anthropogenic is no longer overloaded or until the timeout is reached.

    :param timeout: The maximum time (in seconds) to wait. Default is 1200 seconds (20 minutes).
    :return: None
    """
    start_time = time.time()
    time.sleep(ANTHROPIC_OVERLOADED_SLEEP_TIME)
    while not _is_anthropic_online():
        if time.time() - start_time >= timeout:
            raise TimeoutError("Waited too long for Anthropogenic to be online.")
        time.sleep(ANTHROPIC_OVERLOADED_SLEEP_TIME)


def _is_anthropic_online() -> bool:
    """
    Tests whether anthropic is currently experiencing an overloaded error.
    :return: Whether anthropic is currently online.
    """
    try:
        client = anthropic.Client(api_key=ANTHROPIC_KEY)
        response = client.messages.create(
            model="claude-v1",  # Replace with the correct model if needed
            messages=[{"role": "user", "content": "Hi, what is your name?"}],
            max_tokens_to_sample=50,
        )
    except Exception as e:
        if isinstance(e, InternalServerError):
            return False
        raise e


def _is_overloaded_error(exception: Exception) -> bool:
    """
    Returns whether exception
    :param exception:
    :return:
    """
    if isinstance(exception, InternalServerError):
        try:
            # Check if the status code is 529 and the error type is 'overloaded_error'
            if (exception.status_code == 529 and
                    exception.response.json().get('error', {}).get('type') == 'overloaded_error'):
                return True
        except AttributeError:
            return False

    return False
