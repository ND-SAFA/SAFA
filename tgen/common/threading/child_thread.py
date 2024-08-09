import threading
from typing import Any, Callable

from tgen.common.logging.logger_manager import logger
from tgen.common.threading.threading_state import MultiThreadState


class ChildThread(threading.Thread):
    def __init__(self, state: MultiThreadState, thread_work: Callable):
        """
        Constructs a child thread for the multi-thread state.
        :param state: State containing synchronization information for child threads.
        :param thread_work: The work to be performed by the child thread.
        """
        super().__init__()
        self.state = state
        self.thread_work = thread_work

    def run(self) -> None:
        """
        Performs work on the next available items until no more work is available.
        :return: None
        """
        try:
            work = self.state.get_work()
            while work is not None:
                index, item = work
                work_result = self._perform_work(item, index)
                self.state.on_item_finished(work_result, index)
                work = self.state.get_work()
        except Exception as e:
            # deals with any possible exceptions that may occur outside of performing work.
            self.state.on_exception(e)

    def _perform_work(self, item: Any, index: int, sleep_time: int = None) -> Any:
        """
        Performs work on item.
        :param item: The item to perform work on.
        :param index: The index of the item.
        :param sleep_time: Time to sleep before performing work.
        :return: The result of the work.
        """
        attempts = 0
        has_performed_work = False
        while not has_performed_work and self.state.should_attempt_work(attempts):
            if attempts > 0:
                logger.info(f"Re-trying request...")
            try:
                attempts += 1
                thread_result = self.thread_work(item)
                return thread_result
            except Exception as e:
                self.state.on_exception(e=e, attempts=attempts, index=index)
