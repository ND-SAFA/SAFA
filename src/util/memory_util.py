from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlInit


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
        print(f"GPU memory occupied: {info.used // 1024 ** 2} MB.")
