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
        return (val - min_val)/(max_val - min_val)