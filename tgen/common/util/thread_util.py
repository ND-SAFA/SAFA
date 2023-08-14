import threading
import time
from queue import Queue
from typing import Callable, List

from tqdm import tqdm

from tgen.common.util.logging.logger_manager import logger

THREAD_SLEEP = 5


class ThreadUtil:
    """
    Performs distributed work using threads.
    """

    @staticmethod
    def multi_thread_process(title: str, iterable: List, thread_work: Callable, n_threads: int, max_attempts: int = 1,
                             collect_as_list: bool = False) -> None:
        """
        Performs distributed work over threads.
        :param title: The title of the work being done, used for logging.
        :param iterable: The iterable containing the items to batch and perform work over.
        :param thread_work: The callable performing the work on item_index.
        :param n_threads: The number of threads to use to perform work.
        :return: None
        """
        if collect_as_list:
            iterable = list(enumerate(iterable))

        result_list = [None] * len(iterable)

        item_queue = Queue()
        for i in iterable:
            item_queue.put(i)

        progress_bar = tqdm(total=len(iterable), desc=title)

        def thread_body() -> None:
            """
            Performs work on each item_index in the queue.
            :return: None
            """
            while not item_queue.empty():
                item = item_queue.get()
                if collect_as_list:
                    index, item = item
                attempts = 0
                successful = False
                while not successful and attempts < max_attempts:
                    if attempts > 0:
                        logger.info(f"Re-trying request...")
                    try:
                        thread_result = thread_work(item)
                        successful = True
                        if collect_as_list:
                            result_list[index] = thread_result
                    except Exception as e:
                        logger.exception(e)
                        logger.info(f"Request failed, retrying in {THREAD_SLEEP} seconds.")
                        time.sleep(THREAD_SLEEP)

                    attempts += 1
                if attempts >= max_attempts and not successful:
                    raise ValueError(f"A thread executed {attempts} out of {max_attempts}.")
                progress_bar.update()

        threads = []
        for i in range(n_threads):
            t1 = threading.Thread(target=thread_body, args=[])
            threads.append(t1)
            t1.start()
        for t in threads:
            t.join()
        if collect_as_list:
            return result_list
