from typing import List, Tuple

import numpy as np
import pandas as pd
from numpy import mean

from gen_common.util.list_util import ListUtil
from gen_common.util.math_util import MathUtil


class NpUtil:
    """
    Contains utility methods relating to dealing with numpy.
    """

    @staticmethod
    def get_similarity_matrix_percentile(similarity_matrix: np.array, quantile: float):
        """
        Returns the threshold required for given percentile of similarity matrix scores.
        :param similarity_matrix: The matrix whose percentile (quantile) score is returned.
        :param quantile: The quantile at which to retrieve the threshold for.
        :return: Threshold to achieve percentile within the similarity matrix.
        """
        unique_scores = [s[-1] for s in NpUtil.get_unique_values(similarity_matrix)]
        quantile_score = np.quantile(unique_scores, quantile)
        return quantile_score

    @staticmethod
    def get_similarity_matrix_outliers(similarity_matrix: np.array, sigma: float = None) -> Tuple[float, float]:
        """
        Returns the indices in the matrix whose values are outliers in the matrix.
        :param similarity_matrix: The matrix whose similarities are analyzed.
        :param sigma: How many stds from the mean are allowed.
        :return: The lower and upper threshold scores for filtering out outliers.
        """
        unique_values = NpUtil.get_unique_values(similarity_matrix)
        unique_scores = ListUtil.unzip(unique_values, -1)
        lower_threshold, upper_threshold = NpUtil.detect_outlier_scores(unique_scores, sigma=sigma)
        return lower_threshold, upper_threshold

    @staticmethod
    def get_unique_values(similarity_matrix: np.array) -> List[Tuple[int, int, float]]:
        """
        Returns the values of the unique comparisons in similarity matrix.
        :param similarity_matrix: Matrix of similarity scores containing the same artifacts as rows and cols.
        :return:
        """
        n_rows = similarity_matrix.shape[0]
        n_cols = similarity_matrix.shape[1]
        use_all_indices = n_rows != n_cols
        unique_indices = NpUtil.get_all_indices(n_rows=n_rows, n_cols=n_cols) if use_all_indices else NpUtil.get_unique_indices(
            n_rows=n_rows, n_cols=n_cols)
        unique_scores = NpUtil.get_values(similarity_matrix, unique_indices)
        result = [(i[0], i[1], s) for i, s in zip(unique_indices, unique_scores)]
        return result

    @staticmethod
    def detect_outlier_scores(scores: List[float], epsilon: float = 0.01, sigma: float = None,
                              ensure_at_least_one_detection: bool = False) -> Tuple[float, float]:
        """
        Detects the list of outlier scores within sigma.
        :param scores: List of scores to detect outliers from.
        :param sigma: Number of Std Deviations to include in valid boundary.
        :param epsilon: The small number to use instead of negative or zero values.
        :param sigma: How many stds from the mean are allowed.
        :param ensure_at_least_one_detection: If True, makes sure that at least one score will be detected as low or high.
        :return: The lower and upper threshold scores for filtering out outliers.
        """
        if sigma is None:
            sigma = 2.5 if len(scores) > 20 else 1.5
        scores = pd.Series(sorted(scores, reverse=True))
        scores[scores < 0] = epsilon
        harmonic_mean = mean(scores)

        upper_sigma, lower_sigma = sigma, sigma
        if ensure_at_least_one_detection:
            max_sigmas = (max(scores) - harmonic_mean) / scores.std()
            max_sigma_allowed = MathUtil.round_to_nearest_half(max_sigmas, floor=True)
            upper_sigma = min(sigma, max_sigma_allowed)

            min_sigmas = (harmonic_mean - min(scores)) / scores.std()
            min_sigmas_allowed = MathUtil.round_to_nearest_half(min_sigmas, floor=True)
            lower_sigma = min(sigma, min_sigmas_allowed)

        lower_limit = harmonic_mean - lower_sigma * scores.std()
        upper_limit = harmonic_mean + upper_sigma * scores.std()

        index = min([i for i, score in enumerate(scores) if score < upper_limit])
        closest = scores[index]
        if (upper_limit - closest) <= 0.02:
            upper_limit = closest
        return lower_limit + epsilon, upper_limit - epsilon

    @staticmethod
    def get_unique_indices(n_rows: int, n_cols: int = None) -> List[Tuple[int, int]]:
        """
        Gets the unique set of indices for a matrix of given size.
        :param n_rows: The number of rows in the matrix.
        :param n_cols: The number of cols in the matrix.
        :return: List of unique pairs of indices in the matrix.
        """
        if n_cols is None:
            n_cols = n_rows
        indices = [(i, j) for i in range(n_rows) for j in range(i + 1, n_cols) if i != j]
        return indices

    @staticmethod
    def get_all_indices(n_rows: int, n_cols: int) -> List[Tuple[int, int]]:
        """
        Creates list of all indices spanning matrix with given size.
        :param n_rows: The number of rows in the matrix.
        :param n_cols: The number of cols of the matrix.
        :return: List of indices.
        """
        indices = [(r, c) for r in range(n_rows) for c in range(n_cols)]
        return indices

    @staticmethod
    def get_indices_above_threshold(matrix: np.array, threshold: float):
        """
        Returns list of indices above a threshold. Ensures uniqueness of indices.
        :param matrix: The matrix to extrapolate.
        :param threshold: The threshold to apply.
        :return: List of indices in matrix.
        """

        above_threshold_indices = np.where(matrix > threshold)  # Find the indices where the values are above the threshold
        # Combine row and column indices into a single array of (row, col) tuples
        indices_tuples = np.column_stack((above_threshold_indices[0], above_threshold_indices[1]))
        sorted_indices = np.sort(indices_tuples, axis=1)  # Sort the tuples to ensure uniqueness
        unique_indices = set(map(tuple, sorted_indices))  # Get unique indices by converting the tuples back to a set

        return [(i, j) for i, j in unique_indices if i != j]  # remove references comparing an artifact to itself

    @staticmethod
    def get_values(matrix: np.array, indices: List[Tuple[int, int]]):
        """
        Gets the values in the matrix. TODO: Replace with actual numpy notation.
        :param matrix: The matrix to index.
        :param indices: The index in the matrix to retrieve. Expected to be 2D.
        :return: List of values in the matrix.
        """
        values = [matrix[i][j] for i, j in indices]
        return values

    @staticmethod
    def convert_to_np_matrix(lists: List) -> np.ndarray:
        """
        Converts a list or list of lists to numpy array/matrix
        :param lists: Python list or list of lists
        :return: A numpy array/matrix.
        """
        outer_list = []
        for item in lists:
            if isinstance(item, list):
                item = NpUtil.convert_to_np_matrix(item)
            outer_list.append(item)
        return np.asarray(outer_list)
