import math

from typing import Tuple, Union


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
        conversion = (((val - orig_min) * new_range) / orig_range) if orig_range > 0 else 0
        return conversion + new_min

    @staticmethod
    def calculate_weighted_score(scoreA: float, scoreB: float, weight_of_scoreA: float) -> float:
        """
        Calculates a weighted score
        :param scoreA: The original score
        :param scoreB: The new score to combine with the original
        :param weight_of_scoreA: The amount to weight the new score
        :return: The weighted score of the combined scores
        """
        return scoreA * weight_of_scoreA + scoreB * (1 - weight_of_scoreA)

    @staticmethod
    def difference_between(set1: Union[set, list], set2: Union[set, list]) -> set:
        """
        Finds all elements that are different between set1 and set2
        :param set1: The first set or list
        :param set2: The second set or list
        :return: A set of all different elements
        """
        differences = set(set1).difference(set2)
        differences.update(set(set2).difference(set1))
        return differences

    @staticmethod
    def is_odd(num: int) -> bool:
        """
        Returns True if the number is odd, else False.
        :param num: The number to determine if it is odd.
        :return: True if the number is odd, else False.
        """
        return num % 2 == 1

    @staticmethod
    def round_to_nearest_half(num: float, floor: bool = False, ceil: bool = False) -> float:
        """
        Rounds the number to the nearest 0.5 (e.g. 1.6 -> 1.5, 1.4 -> 1.5)
        :param num: The number to round.
        :param floor: If True, floors the number.
        :param ceil: If True, ceils the number.
        :return: The nearest 0.5 to the number.
        """
        assert not (floor and ceil), "Can only floor OR ceil the number, not both."
        if floor:
            func = math.floor
        elif ceil:
            func = math.ceil
        else:
            func = round
        return func(num * 2) / 2
