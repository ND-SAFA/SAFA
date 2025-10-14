from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlInit

from gen_common.infra.t_logging.logger_manager import logger


class MemoryUtil:
    """
    Contains utility functionality related to managing memory.
    """

    @staticmethod
    def print_gpu_utilization():
        """
        Prints the gpu memory used.
        """
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        info = nvmlDeviceGetMemoryInfo(handle)
        logger.info(f"GPU memory occupied: {info.used // 1024 ** 2} MB.")
