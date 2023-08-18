import threading
import time
from queue import Queue
from typing import Any, Callable, List, Union

from tqdm import tqdm

from tgen.common.util.logging.logger_manager import logger
from tgen.constants.threading_constants import THREAD_SLEEP


class ThreadUtil:
    """
    Performs distributed work using threads.
    """

    @staticmethod
    def multi_thread_process(title: str, iterable: List, thread_work: Callable, n_threads: int, max_attempts: int = 1,
                             collect_results: bool = False, thread_sleep: float = THREAD_SLEEP) -> Union[None, List[Any]]:
        """
        Performs distributed work over threads.
        :param title: The title of the work being done, used for logging.
        :param iterable: The iterable containing the items to batch and perform work over.
        :param thread_work: The callable performing the work on item_index.
        :param n_threads: The number of threads to use to perform work.
        :param max_attempts: The maximum number of attempts before stopping thread entirely.
        :param collect_results: Whether to collect the output of each thread
        :param thread_sleep: The amount of time to sleep after an error occurs.
        :return: None
        """
        if collect_results:
            iterable = list(enumerate(iterable))

        result_list = [None] * len(iterable)

        item_queue = Queue()
        for i in iterable:
            item_queue.put(i)

        progress_bar = tqdm(total=len(iterable), desc=title)
        global_state = {"successful": True}

        def thread_body() -> None:
            """
            Performs the next work payload from the item queue. If fails, then thread will sleed and retry until the max attempts
            has been reached.
            """
            while not item_queue.empty() and global_state["successful"]:
                item = item_queue.get()
                if collect_results:
                    index, item = item
                    
                attempts = 0
                successful_local = False
                while not successful_local and attempts < max_attempts and global_state["successful"]:
                    if attempts > 0:
                        logger.info(f"Re-trying request...")
                    try:
                        thread_result = thread_work(item)
                        successful_local = True
                        if collect_results:
                            result_list[index] = thread_result
                    except Exception as e:
                        logger.exception(e)
                        logger.info(f"Request failed, retrying in {thread_sleep} seconds.")
                        time.sleep(thread_sleep)

                    attempts += 1
                if attempts >= max_attempts and not successful_local:
                    global_state["successful"] = False
                    raise ValueError(f"A thread executed {attempts} out of {max_attempts}.")
                progress_bar.update()

        threads = []
        for i in range(n_threads):
            t1 = threading.Thread(target=thread_body, args=[])
            threads.append(t1)
            t1.start()
        for t in threads:
            t.join()

        if not global_state["successful"]:
            raise ValueError("At least one thread reached the maximum re-tries.")
        if collect_results:
            return result_list
