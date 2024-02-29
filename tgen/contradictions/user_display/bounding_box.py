import math
from dataclasses import dataclass
from typing import Tuple

from tgen.common.constants.deliminator_constants import NEW_LINE


@dataclass
class BoundingBox:
    x_mid: float
    y_mid: float = None
    y0: float = None
    text: str = None
    x0: float = None
    x1: float = None
    y1: float = None
    letter_width: float = 7
    line_height: float = 15
    x_padding: float = 5
    y_padding: float = 15
    max_width: int = math.inf

    def __post_init__(self):
        """
        Calculates coordinates if not provided.
        :return: None.
        """
        assert self.y_mid or self.y0, "Must provide the y center or starting y position."
        if not self.x0 or not self.x1 or not self.y1:
            self._create_coordinates_from_initial_points()
        if not self.y_mid:
            self.y_mid = self.calculate_center_position(self.y0, self.y1)

    @staticmethod
    def from_border(x0: float, x1: float, y0: float, y1: float) -> "BoundingBox":
        """
        Creates a bounding box by providing all the border points.
        :param x0: The leftmost x coordinate.
        :param x1: The rightmost x coordinate.
        :param y0: The top y coordinate.
        :param y1: The bottom y coordinate.
        :return: The bounding box.
        """
        x_mid = BoundingBox.calculate_center_position(x0, x1)
        y_mid = BoundingBox.calculate_center_position(y0, y1)
        return BoundingBox(x_mid, y_mid)

    @staticmethod
    def calculate_center_position(p0: float, p1: float) -> float:
        """
        Calculates the center of two points.
        :param p0: First point (left/top).
        :param p1: Second point (right/bottom).
        :return: The center of the two points.
        """
        return (p0 + p1) / 2

    def get_height_and_width(self) -> Tuple[float, float]:
        """
        Gets the height and width of the box.
        :return: The height and width.
        """
        return self.y1 - self.y0, self.x1 - self.x0

    def get_coordinates(self) -> Tuple[float, float, float, float]:
        """
        Gets the coordinates needed to create a tkinter box.
        :return: The coordinates needed to create a tkinter box.
        """
        return self.x0, self.y0, self.x1, self.y1

    @staticmethod
    def calculate_height_of_text(text2display: str, line_height: float = None) -> float:
        """
        Calculates how much height to use for lines of the text.
        :param text2display: The text to use to judge y.
        :param line_height: The approx height of each line.
        :return: How much height to use for lines of the text.
        """
        line_height = BoundingBox.line_height if not line_height else line_height
        return (text2display.count(NEW_LINE) + 1) * line_height + 15

    @staticmethod
    def calculate_width_of_text(text2display: str, letter_width: float = None, max_width: int = math.inf) -> float:
        """
        Calculates how much width to use for length of the text.
        :param text2display: The text to use to judge x.
        :param letter_width: The approx width of each letter.
        :param max_width: The maximum width for the text.
        :return: How much width to use for length of the text.
        """
        letter_width = BoundingBox.letter_width if not letter_width else letter_width
        len_text = max([len(text) for text in text2display.splitlines()])
        return min(len_text * letter_width, max_width)

    def _create_coordinates_from_initial_points(self) -> None:
        """
        Creates the coordinates for the corners of a bounding box.
        :return: None
        """
        width = self.calculate_width_of_text(self.text, self.letter_width, self.max_width) if self.text else self.x_padding * 2
        height = self.calculate_height_of_text(self.text, self.line_height) if self.text else self.y_padding * 2
        x_offset = (width / 2) + self.x_padding
        y_offset = height + self.y_padding
        self.x0, self.x1 = self.x_mid - x_offset, self.x_mid + x_offset
        if not self.y0:
            self.y0 = self.y_mid - y_offset / 2
        self.y1 = self.y0 + y_offset
