from typing import Tuple


class MathUtil:

    @staticmethod
    def normalize_val(val: float, max_val: float, min_val: float = 0) -> float:
        """
        Normalizes the value to be between 0 and 1
        :param val: The value to normalize
        :param max_val: The max value in range
        :param min_val: The min value in range
        :return: The normalized value
        """
        return (val - min_val) / (max_val - min_val)

    @staticmethod
    def convert_to_new_range(val: float, orig_min_max: Tuple[float, float], new_min_max: Tuple[float, float]) -> float:
        """
        Normalizes the value to be between 0 and 1
        :param val: The value to normalize
        :param orig_min_max: The original (min, max)
        :param new_min_max: The new (min, max)
        :return: The normalized value
        """
        orig_min, orig_max = orig_min_max
        new_min, new_max = new_min_max
        orig_range = orig_max - orig_min
        new_range = new_max - new_min
        return (((val - orig_min) * new_range) / orig_range) + new_min
