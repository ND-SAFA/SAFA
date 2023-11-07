from typing import List, Tuple

import numpy as np


class NpUtil:
    """
    Contains utility methods relating to dealing with numpy.
    """

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
