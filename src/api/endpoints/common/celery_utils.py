from api.server.celery import celery
from tgen.common.logging.logger_manager import logger


def find_task_position(task_id: str) -> int:
    """
    Returns the queue position of task.
    :param task_id: ID of task whose position is to be found.
    :return: The position in queue.
    """
    i = celery.control.inspect()
    active_task_map = i.active()
    reserved_task_map = i.reserved()
    logger.info(f"active:{active_task_map}")  # TODO: Remove this after debug
    logger.info(f"reserved:{reserved_task_map}")  # TODO: Remove this after debug

    active_ids = [task["id"] for queue, queue_tasks in active_task_map.items() for task in queue_tasks]
    if task_id in active_ids:
        return 0
    for queue, queue_tasks in reserved_task_map.items():
        for pos, task in enumerate(queue_tasks):
            if task["id"] == task_id:
                return pos + 1
    return -1  # Indicates task not found in the queue
