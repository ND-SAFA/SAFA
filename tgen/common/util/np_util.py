from typing import List, Tuple

import numpy as np
import pandas as pd
from scipy.stats import hmean

from tgen.common.util.list_util import ListUtil


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
    def get_similarity_matrix_outliers(similarity_matrix: np.array) -> Tuple[float, float]:
        """
        Returns the indices in the matrix whose values are outliers in the matrix.
        :param similarity_matrix: The matrix whose similarities are analyzed.
        :return: The lower and upper threshold scores for filtering out outliers.
        """
        unique_values = NpUtil.get_unique_values(similarity_matrix)
        unique_scores = ListUtil.unzip(unique_values, -1)
        lower_threshold, upper_threshold = NpUtil.detect_outlier_scores(unique_scores)
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
    def detect_outlier_scores(scores: List[float], sigma: int = 1.5, epsilon=0.01) -> Tuple[float, float]:
        """
        Detects the list of outlier scores within sigma.
        :param scores: List of scores to detect outliers from.
        :param sigma: Number of Std Deviations to include in valid boundary.
        :return: The lower and upper threshold scores for filtering out outliers.
        """
        scores = pd.Series(scores)
        scores[scores < 0] = epsilon
        harmonic_mean = hmean(scores)
        lower_limit = harmonic_mean - sigma * scores.std()
        upper_limit = harmonic_mean + sigma * scores.std()

        return lower_limit, upper_limit

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
