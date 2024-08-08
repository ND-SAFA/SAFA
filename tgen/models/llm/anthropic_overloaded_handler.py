import time

from anthropic import InternalServerError

from tgen.common.logging.logger_manager import logger
from tgen.common.threading.threading_state import MultiThreadState
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder

ANTHROPIC_OVERLOADED_SLEEP_TIME = 1000
ANTHROPIC_OVERLOADED_TIMEOUT = 1200


def anthropic_overloaded_handler(state: MultiThreadState, e: Exception,
                                 timeout: float = ANTHROPIC_OVERLOADED_TIMEOUT,
                                 sleep_time: float = ANTHROPIC_OVERLOADED_SLEEP_TIME) -> bool:
    """
    If anthropic overloaded error is detected, pauses state until anthropic is back up.
    :param state: The multi-threaded state controlling requests to anthropic.
    :param e: The exception happening within anthropic.
    :param timeout: The amount of time to wait before giving up.
    :param sleep_time: The amount of time to sleep before checking for anthropic's status.
    :return: None
    """
    if _is_overloaded_error(e):
        logger.info("Anthropic is currently overloaded. Pausing work and resuming once anthropic comes back online.")
        state.pause_work = True
        _wait_until_online(state, timeout=timeout, sleep_time=sleep_time)
        state.pause_work = False
        return True
    return False


def _wait_until_online(state: MultiThreadState, timeout: float, sleep_time: float) -> None:
    """
    Waits until Anthropogenic is no longer overloaded or until the timeout is reached.

    :param timeout: The maximum time (in seconds) to wait. Default is 1200 seconds (20 minutes).
    :return: None
    """
    start_time = time.time()
    time.sleep(sleep_time)
    while not _is_anthropic_online(state):
        if time.time() - start_time >= timeout:
            raise TimeoutError("Waited too long for Anthropic to be online.")
        time.sleep(sleep_time)


def _is_anthropic_online(state: MultiThreadState) -> bool:
    """
    Tests whether anthropic is currently experiencing an overloaded error.
    :return: Whether anthropic is currently online.
    """
    try:
        from tgen.models.llm.anthropic_manager import AnthropicManager
        from tgen.core.trainers.llm_trainer import LLMTrainer
        manager = AnthropicManager()
        builders = [PromptBuilder([Prompt("Hi, what is your name?")])]
        response = LLMTrainer.predict_from_prompts(llm_manager=manager, prompt_builders=builders)
        return True
    except Exception as e:
        if isinstance(e, InternalServerError):
            return False
        state.successful = False
        state.exception = e
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
