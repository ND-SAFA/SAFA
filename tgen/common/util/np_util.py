from typing import List, Tuple

import numpy as np


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
        n_rows = similarity_matrix.shape[0]
        n_cols = similarity_matrix.shape[1]
        use_all_indices = n_rows != n_cols
        unique_indices = NpUtil.get_all_indices(n_rows=n_rows, n_cols=n_cols) if use_all_indices else NpUtil.get_unique_indices(
            n_rows=n_rows, n_cols=n_cols)
        unique_scores = NpUtil.get_values(similarity_matrix, unique_indices)
        quantile_score = np.quantile(unique_scores, quantile)
        return quantile_score

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
