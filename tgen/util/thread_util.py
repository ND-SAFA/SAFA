import threading
from queue import Queue
from typing import Callable, List

from tgen.util.logging.tgen_tqdm import tgen_tqdm


class ThreadUtil:
    """
    Performs distributed work using threads.
    """

    @staticmethod
    def multi_thread_process(title: str, iterable: List, thread_work: Callable, n_threads: int) -> None:
        """
        Performs distributed work over threads.
        :param title: The title of the work being done, used for logging.
        :param iterable: The iterable containing the items to batch and perform work over.
        :param thread_work: The callable performing the work on item_index.
        :param n_threads: The number of threads to use to perform work.
        :return: None
        """

        item_queue = Queue()
        for item in iterable:
            item_queue.put(item)

        progress_bar = tgen_tqdm(total=len(iterable), desc=title)

        def thread_body() -> None:
            """
            Performs work on each item_index in the queue.
            :return: None
            """
            while not item_queue.empty():
                item = item_queue.get()
                thread_work(item)
                progress_bar.update()

        threads = []
        for i in range(n_threads):
            t1 = threading.Thread(target=thread_body, args=[])
            threads.append(t1)
            t1.start()
        for t in threads:
            t.join()
