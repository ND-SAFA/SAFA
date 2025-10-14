import psutil

from api.endpoints.handler.endpoint_decorator import endpoint_get


@endpoint_get
def health_metrics():
    """
    :return: Return health metrics of current machine.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent  # Adjust path as necessary

    metrics = {
        'cpu_usage_percent': cpu_usage,
        'memory_usage_percent': memory_usage,
        'disk_usage_percent': disk_usage
    }
    return metrics
