from typing import Callable, List, Set

from common_resources.tools.constants.threading_constants import THREAD_SLEEP
from common_resources.tools.t_threading.threading_state import MultiThreadState


class ThreadUtil:
    """
    Performs distributed work using threads.
    """

    @staticmethod
    def multi_thread_process(title: str, iterable: List, thread_work: Callable, n_threads: int, max_attempts: int = 1,
                             collect_results: bool = False, sleep_time: float = THREAD_SLEEP,
                             retries: Set = None, raise_exception: bool = True, rpm: int = None, **kwargs) -> MultiThreadState:
        """
        Performs distributed work over threads.
        :param title: The title of the work being done, used for logging.
        :param iterable: The iterable containing the items to batch and perform work over.
        :param thread_work: The callable performing the work on item_index.
        :param n_threads: The number of threads to use to perform work.
        :param max_attempts: The maximum number of attempts before stopping thread entirely.
        :param collect_results: Whether to collect the output of each thread
        :param sleep_time: The amount of time to sleep after an error occurs.
        :param retries: List of indices to retry if they failed initially.
        :param raise_exception: Throws an exception if one of the threads fails.
        :param rpm: Maximum requests per minutes allowed.
        :param kwargs: Keyword arguments passed to thread state.
        :return: None
        """

        global_state: MultiThreadState = MultiThreadState(iterable,
                                                          title=title,
                                                          retries=retries,
                                                          max_attempts=max_attempts,
                                                          collect_results=collect_results,
                                                          sleep_time=sleep_time,
                                                          rpm=rpm,
                                                          **kwargs)

        threads = []
        for i in range(n_threads):
            t1 = ChildThread(global_state, thread_work)
            threads.append(t1)
            t1.start()

        for t in threads:
            t.join()

        if not global_state.successful:
            if raise_exception:
                raise global_state.exception
        if collect_results:
            global_state.results = global_state.result_list
        return global_state
