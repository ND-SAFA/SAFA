import queue
import threading
import time
from typing import Generic, TypeVar

ItemType = TypeVar("ItemType")
SEC_PER_MIN = 60.0


class RateLimitedQueue(Generic[ItemType]):
    def __init__(self, items_per_minute: int):
        """
        Synchronized queue with limited rate per limit.
        :param items_per_minute: How many items per minute are allowed.
        """
        self.queue = queue.Queue()
        self.items_per_minute = items_per_minute
        self.lock = threading.Lock()
        self.last_access_time = None
        self.time_between_requests = SEC_PER_MIN / items_per_minute if items_per_minute else None
        self.pause_event = threading.Event()
        self.pause_event.set()  # Start with the queue unpaused

    def __len__(self) -> int:
        """
        :return: Returns the length of the queue.
        """
        return self.queue.unfinished_tasks

    def put(self, item: ItemType) -> None:
        """
        Adds item to queue.
        :param item: The item to add.
        :return: None
        """
        self.queue.put(item)

    def get(self) -> ItemType:
        """
        Gets the next item in the queue.
        :return: Returns next item in the queue.
        """
        self.pause_event.wait()  # Wait until unpaused

        if self.time_between_requests is None:
            return None if self.queue.qsize() == 0 else self.queue.get()

        with self.lock:
            if self.queue.qsize() == 0:
                return None

            elapsed_time = time.time() - self.last_access_time if self.last_access_time else self.time_between_requests

            if elapsed_time < self.time_between_requests:
                sleep_time = self.time_between_requests - elapsed_time
                time.sleep(sleep_time)

            if self.queue.qsize() == 0:
                return None

            self.last_access_time = time.time()
            item = self.queue.get()
            return item

    def change_time_per_request(self, delta: float) -> None:
        """
        Increments the expected seconds per request.
        :param delta: The delta to increase interval by.
        :return: None
        """
        if self.time_between_requests is None:
            raise Exception("RPM is not set, therefore, cannot change time between requests.")
        self.time_between_requests += delta

    def pause(self) -> None:
        """
        Pauses the queue, preventing items from being retrieved.
        :return: None
        """
        self.pause_event.clear()

    def unpause(self) -> None:
        """
        Unpauses the queue, allowing items to be retrieved again.
        :return: None
        """
        self.pause_event.set()
