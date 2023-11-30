import time
from dataclasses import field
from queue import Queue
from typing import Any, Iterable, List, Optional, Set

from tqdm import tqdm

from tgen.common.constants.logging_constants import TQDM_NCOLS
from tgen.common.constants.threading_constants import THREAD_SLEEP
from tgen.common.logging.logger_manager import logger


class MultiThreadState:
    def __init__(self, iterable: Iterable, title: str, retries: Set, collect_results: bool = False, max_attempts: int = 3,
                 sleep_time: float = THREAD_SLEEP):
        """
        Creates the state to syncronize a multi-threaded job.
        :param iterable: List of items to perform work on.
        :param title: The title of the progress bar.
        :param retries: The indices of the iterable to retry.
        :param collect_results: Whether to collect the resutls of the jobs.
        :param max_attempts: The maximum number of retries after exception is thrown.
        :param sleep_time: The time to sleep after an exception has been thrown.
        """
        self.title = title
        self.iterable = list(enumerate(iterable))
        self.result_list = [None] * len(iterable)
        self.item_queue = Queue()
        self.progress_bar = None
        self.successful: bool = True
        self.exception: Optional[Exception] = None
        self.failed_responses: Set[int] = field(default_factory=set)
        self.results: Optional[List[Any]] = None
        self.collect_results = collect_results
        self.sleep_time = sleep_time
        self.max_attempts = max_attempts
        self._init_retries(retries)
        self._init_progress_bar()

    def has_work(self) -> bool:
        """
        :return: Returns whether there is work to be performed and its still valid to do so.
        """
        return not self.item_queue.empty() and self.successful

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

    def on_item_finished(self, result: Any, index: int = None) -> None:
        """
        Process the result performed by a job.
        :param result: The result of a job.
        :param index: The index of the item that was processed.
        :return: None
        """
        if self.collect_results:
            assert index is not None, "Expected index to be provided when collect results is activated."
            self.result_list[index] = result
        self.progress_bar.update()

    def on_item_fail(self, e: Exception, index: int) -> None:
        """
        Handler for when a child-thread has completely failed, reaching its max attempts.
        :param e: The final exception thrown.
        :param index: The index of the work being processed.
        :return: None
        """
        self.successful = False
        self.exception = e
        self.failed_responses.add(index)
        if self.collect_results:
            self.result_list[index] = e

    def on_valid_exception(self, e: Exception) -> None:
        """
        Handler for when a thread caught an exception and is still within its threshold of max attempts.
        :param e: The exception thrown.
        :return: None
        """
        logger.exception(e)
        logger.info(f"Request failed, retrying in {self.sleep_time} seconds.")
        time.sleep(self.sleep_time)

    def _init_progress_bar(self) -> None:
        """
        Initializes the progress bar for the job.
        :return: None
        """
        self.progress_bar = tqdm(total=self.item_queue.unfinished_tasks, desc=self.title, ncols=TQDM_NCOLS)

    def _init_retries(self, retries: Set) -> None:
        """
        Initializes the indices to retry.
        :param retries: The indices to retry.
        :return: None
        """
        for i, item in self.iterable:
            if not retries or i in retries:
                self.item_queue.put((i, item))
