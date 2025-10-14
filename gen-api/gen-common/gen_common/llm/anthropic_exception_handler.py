import time

from anthropic import APIConnectionError, InternalServerError, RateLimitError

from gen_common.infra.t_logging.logger_manager import logger
from gen_common.infra.t_threading.threading_state import MultiThreadState

ANTHROPIC_OVERLOADED_SLEEP_TIME = 1000
ANTHROPIC_OVERLOADED_TIMEOUT = 1200
ANTHROPIC_ERRORS = [InternalServerError, RateLimitError, APIConnectionError]


def anthropic_exception_handler(state: MultiThreadState, e: Exception,
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

    if any([isinstance(e, error_type) for error_type in ANTHROPIC_ERRORS]):
        logger.info(f"Received anthropic error: {e}")
        logger.info("Anthropic is currently overloaded. Resuming once anthropic comes back online.")
        state.add_time(.1)
        _wait_until_online(state, timeout=timeout, sleep_time=sleep_time)
        return True
    return False


def _wait_until_online(state: MultiThreadState, timeout: float, sleep_time: float) -> None:
    """
    Waits until Anthropogenic is no longer overloaded or until the timeout is reached.
    :param state: Synchronizing state between all threads.
    :param timeout: The maximum time (in seconds) to wait. Default is 1200 seconds (20 minutes).
    :param sleep_time: The amount of seconds to sleep between checks to anthropic.
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
    :param state: Synchronizing state between all threads.
    :return: Whether anthropic is currently online.
    """
    try:

        from gen_common.llm.anthropic_manager import AnthropicManager
        from gen_common.constants.default_model_managers import DefaultLLMManager
        manager = DefaultLLMManager.EFFICIENT()
        response = manager.make_completion_request_impl(prompt="Hi, what is your name?")
        logger.info("Anthropic is online.")
        return True
    except Exception as e:
        if isinstance(e, InternalServerError):
            return False
        state.successful = False
        state.exception = e
        raise e
