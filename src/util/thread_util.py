import threading
from typing import Callable, List

from tqdm import tqdm

from util.general_util import ListUtil


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
        :param thread_work: The callable performing the work on item.
        :param n_threads: The number of threads to use to perform work.
        :return: None
        """
        batches = ListUtil.batch(iterable, n_threads)
        for batch in tqdm(batches, desc=title):
            threads = []
            for item in batch:
                t1 = threading.Thread(target=thread_work, args=[item])
                threads.append(t1)
                t1.start()

            for t in threads:
                t.join()
