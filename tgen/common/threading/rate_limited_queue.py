import queue
import threading
import time
from typing import Generic, TypeVar

ItemType = TypeVar("ItemType")


class RateLimitedQueue(Generic[ItemType]):
    def __init__(self, items_per_minute):
        """
        Syncronized queue with limited rate per limit.
        :param items_per_minute: How many items per minute are allowed.
        """
        self.queue = queue.Queue()
        self.items_per_minute = items_per_minute
        self.lock = threading.Lock()
        self.last_access_time = time.time()
        self.interval = 60.0 / items_per_minute

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
        while True:
            with self.lock:
                current_time = time.time()
                elapsed_time = current_time - self.last_access_time

                if elapsed_time < self.interval:
                    time.sleep(self.interval - elapsed_time)

                self.last_access_time = time.time()

            if not self.queue.empty():
                return self.queue.get()
            else:
                return None
