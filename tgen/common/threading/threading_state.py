import time
from typing import Any, Callable, Iterable, List, Optional, Set

from tqdm import tqdm

from tgen.common.constants.logging_constants import TQDM_NCOLS
from tgen.common.constants.threading_constants import THREAD_SLEEP
from tgen.common.logging.logger_manager import logger
from tgen.common.threading.rate_limited_queue import RateLimitedQueue

ExceptionHandler = Callable[["MultiThreadState", Exception], bool]


class MultiThreadState:
    def __init__(self, iterable: Iterable, title: str, retries: Set, collect_results: bool = False, max_attempts: int = 3,
                 sleep_time_on_error: float = THREAD_SLEEP, rpm: int = None, exception_handlers: List[ExceptionHandler] = None):
        """
        Creates the state to synchronize a multi-threaded job.
        :param iterable: List of items to perform work on.
        :param title: The title of the progress bar.
        :param retries: The indices of the iterable to retry.
        :param collect_results: Whether to collect the results of the jobs.
        :param max_attempts: The maximum number of retries after exception is thrown.
        :param sleep_time_on_error: The time to sleep after an exception has been thrown.
        :param rpm: Maximum rate of items per minute.
        """
        self.title = title
        self.iterable = list(enumerate(iterable))
        self.result_list = [None] * len(iterable)
        self.item_queue = RateLimitedQueue(rpm)
        self.progress_bar = None
        self.successful: bool = True
        self.exception: Optional[Exception] = None
        self.pause_work: bool = False
        self.failed_responses: Set[int] = set()
        self.results: Optional[List[Any]] = None
        self.collect_results = collect_results
        self.sleep_time_on_error = sleep_time_on_error
        self.max_attempts = max_attempts
        self.exception_handlers = exception_handlers if exception_handlers else []
        self._init_retries(retries)
        self._init_progress_bar()

    def get_work(self) -> Any:
        """
        :return: Whether there is work to be performed and its still valid to do so.
        """
        return self.item_queue.get()

    def should_attempt_work(self, attempts: int) -> bool:
        """
        Decides whether a child thread should attempt to perform work.
        :param attempts: The number of attempts at performing the work.
        :return: Whether to try to perform work again.
        """
        return self.below_attempt_threshold(attempts) and self.successful

    def below_attempt_threshold(self, attempts: int) -> bool:
        """
        Whether the number of attempts is below the max threshold.
        :param attempts: The number of attempts at performing work.
        :return: Whether the threshold is exceeded.
        """
        return attempts < self.max_attempts

    def get_item(self) -> Any:
        """
        :return: Returns the next work item.
        """
        return self.item_queue.get()

    def on_item_finished(self, result: Any, index: int) -> None:
        """
        Process the result performed by a job.
        :param result: The result of a job.
        :param index: The index of the item that was processed.
        :return: None
        """
        if self.collect_results:
            assert index is not None, "Expected index to be provided when collect results is activated."
            if result:
                self.result_list[index] = result
        self.progress_bar.update()

    def on_exception(self, e: Exception, attempts: int, index: int):
        """
        Handles exception happening in child thread.
        :param e: The exception occurring.
        :param attempts: The number of attempts the child has attempted.
        :param index: The child index (also a unique identifier).
        :return: None
        """
        for exception_handler in self.exception_handlers:
            is_handled = exception_handler(self, e)
            if is_handled:
                return
            
        if self.below_attempt_threshold(attempts):
            self.pause_work = True
            logger.exception(e)
            logger.info(f"Request failed, retrying in {self.sleep_time_on_error} seconds.")
            time.sleep(self.sleep_time_on_error)
        else:
            self.successful = False
            self.exception = e
            self.failed_responses.add(index)
            if self.collect_results:
                self.result_list[index] = e

    def increase_interval(self) -> None:
        """
        Increases the interval to wait between items in queue.
        :return: None
        """
        self.item_queue.increment_interval(.1)

    def _init_progress_bar(self) -> None:
        """
        Initializes the progress bar for the job.
        :return: None
        """
        self.progress_bar = tqdm(total=len(self.item_queue), desc=self.title, ncols=TQDM_NCOLS)

    def _init_retries(self, retries: Set) -> None:
        """
        Initializes the indices to retry.
        :param retries: The indices to retry.
        :return: None
        """
        for i, item in self.iterable:
            if not retries or i in retries:
                self.item_queue.put((i, item))
