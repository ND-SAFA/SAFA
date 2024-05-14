import threading
import tkinter as tk
from tkinter import font, scrolledtext
from typing import Tuple, Dict, List

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE, SPACE
from tgen.common.logging.logger_manager import logger
from tgen.common.objects.artifact import Artifact
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.str_util import StrUtil
from tgen.contradictions.user_display.bounding_box import BoundingBox
from tgen.contradictions.with_decision_tree.contradictions_detector_with_tree import ContradictionsDetectorWithTree
from tgen.contradictions.with_decision_tree.requirement import Requirement, RequirementConstituent
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.decision_tree.path import Path


class ContradictionsUserDisplay:
    BACKGROUND_COLOR = "#f3f4f6"
    ACCENT_COLOR = "#4e8d7c"
    EDGES_COLOR = "#5C4033"
    N_REQUIREMENTS = 2

    root = None
    font = None
    requirements_entries = []
    result_text = None

    REQUIREMENT_CONSTITUENT_COLORS = {RequirementConstituent.CONDITION: "#000080",
                                      RequirementConstituent.VARIABLE: "#E600BF",
                                      RequirementConstituent.ACTION: "#00CCCC",
                                      RequirementConstituent.EFFECT: "#222222",
                                      }

    def run(self) -> None:
        """
        Runs the display.
        :return: None
        """
        if not self.root:
            self.create()
        self.root.mainloop()

    def create(self) -> None:
        """
        Creates the display.
        :return: None
        """
        self.root = tk.Tk()
        self.root.title("Contradiction Checker")

        self.root.geometry("400x400")

        possible_fonts = list(font.families())
        self.font = font.Font(family=possible_fonts[0], size=12)
        self.root.configure(bg=self.BACKGROUND_COLOR)
        self.root.minsize(800, 600)  # Adjust the width and height as needed

        self.requirements_entries = [self._create_requirement_entry(req_num=i) for i in range(self.N_REQUIREMENTS)]

        self._create_checker_button()

        # Area to show the result with some styling
        self.result_text = self._create_results_label()

    @staticmethod
    def create_and_run() -> None:
        """
        Creates the display and runs it.
        :return: None
        """
        ContradictionsUserDisplay().run()

    def start_contradiction_check(self) -> None:
        """
        Starts the process of contradiction detection when button is pressed.
        :return: None.
        """
        self.result_text.set("Checking for contradictions...")
        threading.Thread(target=self.check_for_contradictions).start()

    def check_for_contradictions(self) -> None:
        """
        Runs logic for checking contradictions.
        :return: None
        """
        requirements = self._get_requirements_from_input()
        if any([not r for r in requirements]):
            self.result_text.set("Must provide two requirements to check.")
        else:
            artifacts = [Artifact(id=f"R{i}", content=req, layer_id="Requirement") for i, req in enumerate(requirements)]
            try:
                decision_tree_path = ContradictionsDetectorWithTree.detect_single_pair(*artifacts)
                self.root.after(0, self._create_result_popup, decision_tree_path)
            except Exception:
                logger.exception("An error occurred. ")
                self.result_text.set("Sorry, an error occurred. Please try again.")

    def show_decision_tree(self, path: Path, text_start_y: int = 15, max_text_width: int = 500,
                           x_padding_between_nodes: float = 40, y_padding_between_nodes: float = 75,
                           x_canvas_padding: float = 200, y_canvas_padding: float = 100) -> None:
        """
        Shows the decision tree for a contradiction result.
        :param path: Contains the nodes that led to the result.
        :param text_start_y: Where the text should start vertically.
        :param max_text_width: The maximum width for a given requirement.
        :param x_padding_between_nodes: Amount of padding between nodes horizontally.
        :param y_padding_between_nodes: Amount of padding between nodes vertically.
        :param x_canvas_padding: Amount of padding on canvas horizontally.
        :param y_canvas_padding: Amount of padding on canvas vertically.
        :return: None
        """
        popup = tk.Toplevel(self.root)
        popup.title("Path to Decision")

        requirements = self._get_requirements_from_input()
        additional_text = f"{RequirementConstituent.EFFECT.name} {RequirementConstituent.CONDITION.name}"
        nodes = path.get_nodes()

        node_text = [node.get_formatted_question(path.args) if isinstance(node, LLMNode) else node.description for node in
                     nodes]
        canvas_width = self._calculate_canvas_width(node_text, requirements, max_text_width, x_padding_between_nodes, x_canvas_padding)

        center_x, root_y0 = canvas_width / 2, text_start_y + (x_padding_between_nodes / 2)
        req_x_coords = [center_x + (-1 if i == 0 else 1) * ((BoundingBox.calculate_width_of_text(r + additional_text,
                                                                                                 max_width=max_text_width)
                                                             + x_padding_between_nodes) / 2) for i, r in enumerate(requirements)]
        node2bounding_box = {
            req: BoundingBox(x_mid=req_x_coords[i], y0=root_y0, text=req + additional_text, max_width=max_text_width)
            for i, req in enumerate(requirements)}

        last_y = DictUtil.get_value_by_index(node2bounding_box, 0).y1 - y_padding_between_nodes / 2
        for i, node in enumerate(nodes):
            x_mid = center_x
            y0 = last_y + y_padding_between_nodes
            bb = BoundingBox(x_mid=x_mid, y0=y0, text=node_text[i])
            node2bounding_box[node_text[i]] = bb
            last_y = bb.y1

        edges = [(i + len(requirements) - 1, i + len(requirements), path.get_choice(i)) for i in range(1, len(nodes))]

        min_height = DictUtil.get_value_by_index(node2bounding_box, - 1).y1
        canvas = tk.Canvas(popup, width=canvas_width, height=min_height + y_canvas_padding)

        key = [("key = ", self.ACCENT_COLOR)] + [(f"{c.name}|", color) for c, color in self.REQUIREMENT_CONSTITUENT_COLORS.items()]
        key_width = BoundingBox.calculate_width_of_text(EMPTY_STRING.join([k[0] for k in key]))
        self._display_text_segments(key, (center_x - (key_width / 2), text_start_y), canvas, make_scrollable=False)
        self._draw_decision_tree(canvas, node2bounding_box, edges, path.args)

    def _create_requirement_entry(self, req_num: int) -> scrolledtext.ScrolledText:
        """
        Creates an entry for the requirement input.
        :param req_num: Which requirement this is an entry for.
        :return: The requirement input entry.
        """
        tk.Label(self.root, text=f"Requirement {req_num + 1}:", font=self.font, bg=self.BACKGROUND_COLOR).pack(pady=(10, 0))
        entry_req = scrolledtext.ScrolledText(self.root, width=40, height=5, font=self.font)
        entry_req.pack(pady=5)
        return entry_req

    def _create_results_label(self) -> tk.StringVar:
        """
        Creates the result label and returns an instance of the text to display.
        :return: The text to display for the result.
        """
        result_text = tk.StringVar()
        result_label = tk.Label(self.root, textvariable=result_text, font=self.font, bg=self.BACKGROUND_COLOR)
        result_label.pack(pady=(10, 0))
        return result_text

    def _create_checker_button(self) -> tk.Button:
        """
        Creates the button used to check requirements for contradictions.
        :return: The button.
        """
        check_button = tk.Button(self.root, text="Check for Contradictions", command=self.start_contradiction_check, font=self.font,
                                 bg=self.ACCENT_COLOR, fg="white", relief=tk.FLAT)
        check_button.pack(pady=10)
        return check_button

    def _create_result_popup(self, path: Path) -> None:
        """
        Creates the popup for displaying the result.
        :param path: The path from the contradiction detection.
        :return: None.
        """
        popup = tk.Toplevel(self.root)
        popup.title("Contradictions Result")

        result = path.get_final_decision()

        result_label = tk.Label(popup, text=f"Result: {result.title()}", font=self.font)
        result_label.pack(pady=10)

        btn_show_tree = tk.Button(popup, text="Show Path to Decision", command=lambda: self.show_decision_tree(path),
                                  bg=self.ACCENT_COLOR, fg="white", relief=tk.FLAT)
        btn_show_tree.pack(pady=20)

        self.result_text.set("")

    @staticmethod
    def _calculate_canvas_width(node_text: List[str], requirements: List[str], max_text_width: int,
                                x_padding_between_nodes: float, canvas_padding: float) -> float:
        """
        Calculates the width of the canvas based on the text being displayed.
        :param node_text: All node text.
        :param requirements: The requirements text.
        :param max_text_width: Maximum width allowed.
        :param x_padding_between_nodes: Distance between horizontal nodes.
        :param canvas_padding: Additional padding for the canvas.
        :return: The width of the canvas based on the text being displayed.
        """
        text_widths = [BoundingBox.calculate_width_of_text(text) for text in node_text]
        text_widths.extend(
            [2 * (BoundingBox.calculate_width_of_text(r, max_width=max_text_width) + x_padding_between_nodes)
             for r in requirements])
        canvas_width = max(text_widths) + canvas_padding + x_padding_between_nodes
        return canvas_width

    def _draw_decision_tree(self, canvas: tk.Canvas, nodes: Dict[str, BoundingBox], edges: List[Tuple],
                            requirements: Tuple[Requirement]) -> None:
        """
        Draws the decision tree for a contradiction result.
        :param canvas: Canvas to draw on.
        :param nodes: The nodes mapped to coordinates to draw for the tree.
        :param edges: The edges connecting the nodes in the form (start node, end node, label) .
        :param requirements: The requirements that were used as input.
        :return: None
        """
        original_requirements = [r.replace(NEW_LINE, EMPTY_STRING) for r in self._get_requirements_from_input()]
        for text, bounding_box in nodes.items():

            original_text = text.replace(NEW_LINE, EMPTY_STRING)
            req_index = original_requirements.index(original_text) if original_text in original_requirements else -1
            color = self.ACCENT_COLOR if req_index < 0 else ""
            canvas.create_rectangle(*bounding_box.get_coordinates(), fill=color, outline=color)
            if req_index >= 0:
                req: Requirement = requirements[req_index]
                segments = self._color_req_segments(req, text)
                self._display_text_segments(segments, (bounding_box.x0 + 7, bounding_box.y0 + 7), canvas,
                                            height_width=bounding_box.get_height_and_width(),
                                            make_scrollable=True)
            else:
                canvas.create_text(bounding_box.x_mid, bounding_box.y_mid, text=text, fill="white")

        bound_boxes = list(nodes.values())
        for start, end, label in edges:
            start_x, end_x = bound_boxes[start].x_mid, bound_boxes[end].x_mid
            start_y, end_y = bound_boxes[start].y1, bound_boxes[end].y0
            canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, fill=self.EDGES_COLOR)
            x_mid, y_mid = BoundingBox.calculate_center_position(start_x, end_x), BoundingBox.calculate_center_position(start_y, end_y)
            canvas.create_oval(*BoundingBox(x_mid=x_mid, y_mid=y_mid, text=label).get_coordinates(), fill=self.EDGES_COLOR,
                               outline=self.EDGES_COLOR)
            canvas.create_text(x_mid, y_mid, text=label, fill="white")

    def _color_req_segments(self, req: Requirement, req_text: str) -> List[Tuple]:
        """
        Assigns each requirement part a color.
        :param req: The requirement.
        :param req_text: Text of the requirement.
        :return: List of segment text, color pairs.
        """
        condition_start, condition_end = self._find_loc_of_constituent(req, req_text, RequirementConstituent.CONDITION)
        effect_start, effect_end = self._find_loc_of_constituent(req, req_text, RequirementConstituent.EFFECT)
        condition_segments = self._get_constituent_segments(req, RequirementConstituent.CONDITION, req_text, condition_start,
                                                            condition_end) if condition_start >= 0 else []
        effect_segments = self._get_constituent_segments(req, RequirementConstituent.EFFECT, req_text, effect_start,
                                                         effect_end) if effect_start >= 0 else []
        segments = [*condition_segments, *effect_segments] \
            if condition_start < effect_start else [*effect_segments, *condition_segments]
        return segments

    @staticmethod
    def _find_loc_of_constituent(req: Requirement, req_text: str, constituent: RequirementConstituent) -> Tuple[int, int]:
        """
        Finds the location of the constituent.
        :param req: The requirement obj.
        :param req_text: The text of the requirement.
        :param constituent: Constituent to find.
        :return: The location of the constituent.
        """
        max_index = len(req_text) + 1
        constituent = req.get_constituent(constituent2get=constituent)
        if not constituent:
            return max_index, max_index
        actual_start_index, actual_end_index = ContradictionsUserDisplay._find_constituent_in_modified_requirement(req_text,
                                                                                                                   constituent)

        return actual_start_index, actual_end_index

    def _get_constituent_segments(self, req: Requirement, constituent: RequirementConstituent,
                                  req_text: str, start: int, end: int) -> List[Tuple]:
        """
        Splits the constituent into colored components.
        :param req: The requirement.
        :param constituent: The constituent to get segments for.
        :param req_text: The full text of the requirements.
        :param start: The starting index of the constituent.
        :param end: The ending index of the constituent.
        :return: The constituent split into colored components.
        """
        if not req.get_constituent(constituent):
            return []
        var_segments = self._color_constituent(req, req_text[start:end + 1], constituent,
                                               RequirementConstituent.VARIABLE)
        all_segments = []
        for seg in var_segments:
            if seg[1] == self.REQUIREMENT_CONSTITUENT_COLORS[constituent]:
                all_segments.extend(self._color_constituent(req, seg[0], constituent,
                                                            RequirementConstituent.ACTION))
            else:
                all_segments.append(seg)
        all_segments = [(f"{constituent.name}: ", self.REQUIREMENT_CONSTITUENT_COLORS[constituent])] + all_segments
        return all_segments

    def _color_constituent(self, req: Requirement, text: str, constituent: RequirementConstituent,
                           constituent_component: RequirementConstituent) -> List[Tuple]:
        """
        Splits the constituent into parts based on the given component and assigns a color.
        :param req: The requirement.
        :param text: The text of this portion of the constituent.
        :param constituent: The constituent being examined.
        :param constituent_component: The component of the constituent being examined.
        :return: List of segment text, segment color pairs.
        """
        component_value = req.get_constituent(constituent_component, constituent=constituent, default=EMPTY_STRING)
        if constituent_component == RequirementConstituent.VARIABLE:
            component_value = StrUtil.remove_stop_words(component_value)
        segments = self._split_modified_requirement_by_constituent(text, component_value) if component_value else [text]
        segments = [
            (segments[int(i / 2)].strip(), self.REQUIREMENT_CONSTITUENT_COLORS[constituent])
            if i % 2 == 0 else (component_value, self.REQUIREMENT_CONSTITUENT_COLORS[constituent_component])
            for i in range(2 * len(segments) - 1)]
        return [s for s in segments if s[0]]

    def _get_requirements_from_input(self) -> List[str]:
        """
        Gets the requirements that were inputted.
        :return: The requirements that were inputted.
        """
        return [r.get("1.0", "end-1c") for r in self.requirements_entries]

    def _display_text_segments(self, text_segments: list[tuple[str, str]], coordinates: tuple[float, float],
                               canvas: tk.Canvas,
                               height_width: tuple[float, float] = None,
                               make_scrollable: bool = True) -> None:
        """
        Displays text segments of different colors, handling newlines correctly.
        :param text_segments: List of text, color pairs for each segment.
        :param coordinates: The starting x, y coordinates.
        :param canvas: The canvas to display on.
        :param height_width: The height and width of the text box.
        :param make_scrollable: If True, adds scrollbar to the canvas.
        :return: None
        """
        original_x, y = coordinates
        x = original_x
        line_height = 20

        if make_scrollable:
            assert height_width, "Must provide height and width for making it scrollable."
            frame = tk.Frame(canvas)
            frame_id = canvas.create_window((original_x, y), window=frame, anchor="nw")
            # Attach the scrollbar to the frame for vertical scrolling (change to horizontal if needed)
            scrollbar = tk.Scrollbar(frame, orient="vertical")
            scrollbar.pack(side=tk.RIGHT, fill="y")

            average_char_width = self.font.measure('0')
            width = int(height_width[1] / average_char_width)
            text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, wrap="word", height=5,
                                  width=width,
                                  background=self.ACCENT_COLOR)  # Set height as needed
            text_widget.pack(side=tk.LEFT, fill="both", expand=True)

            # Configure the scrollbar to scroll the text widget
            scrollbar.config(command=text_widget.yview)

            # Insert text into the text widget
            for text, color in text_segments:
                text_widget.insert(tk.END, text + SPACE, color)
                text_widget.tag_configure(color, foreground=color)

        else:
            # Insert text into the canvas
            for text, color in text_segments:
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if line:  # Check if the line is not empty
                        text_id = canvas.create_text(x, y, text=line, fill=color, anchor="nw")
                        text_width = canvas.bbox(text_id)[2] - canvas.bbox(text_id)[0]  # Calculate text width
                        x += text_width + 20  # Move x to the right for the next text segment; adjust spacing as needed
                    if i < len(lines) - 1:  # If not the last line, move to the start of the next line
                        x = original_x
                        y += line_height

        # Ensure the canvas is packed last so it doesn't shrink to scrollbar size
        canvas.pack(side=tk.LEFT, fill="both", expand=True)

    def _split_requirement(self, req: Requirement, req_text: str) -> str:
        """
        Splits the requirement into lines so that no line exceeds the max text length.
        :param req: The requirement.
        :param req_text: The requirement text.
        :return: The requirement split into lines.
        """
        if req.get_condition():
            condition_start, condition_end = self._find_loc_of_constituent(req, req_text, RequirementConstituent.CONDITION)
            effect_start, effect_end = self._find_loc_of_constituent(req, req_text, RequirementConstituent.EFFECT)
            if condition_start < effect_start:
                req = req[condition_start:condition_end] + NEW_LINE + req[effect_start, effect_end]
        return req

    @staticmethod
    def _find_constituent_in_modified_requirement(req_text: str, constituent: str, start: int = 0) -> Tuple[int, int]:
        """
        Locates the constituent in the requirement when new lines have been added.
        :param req_text: The requirement with additional new lines.
        :param constituent: The original constituent in the requirement.
        :param start: Where to start to look for the string.
        :return: The start and end index of the constituent in the req text.
        """
        cleaned_text = req_text.replace(NEW_LINE, EMPTY_STRING)
        cleaned_constituent = constituent.replace(NEW_LINE, EMPTY_STRING)
        constituent_start_loc = cleaned_text.find(cleaned_constituent, start)
        if constituent_start_loc == -1:
            return constituent_start_loc, constituent_start_loc
        constituent_end_loc = constituent_start_loc + len(cleaned_constituent) - 1

        constituent_start_loc = ContradictionsUserDisplay._find_actual_loc(req_text, constituent_start_loc)
        constituent_end_loc = ContradictionsUserDisplay._find_actual_loc(req_text, constituent_end_loc)

        return constituent_start_loc, constituent_end_loc

    @staticmethod
    def _split_modified_requirement_by_constituent(req_text: str, constituent: str) -> List[str]:
        """
        Splits by the constituent in the requirement when new lines have been added.
        :param req_text: The requirement with additional new lines.
        :param constituent: The original constituent in the requirement.
        :return: The requirement split into parts by the constituent.
        """
        parts = []
        start, last_index = 0, 0
        while True:
            start, end = ContradictionsUserDisplay._find_constituent_in_modified_requirement(req_text, constituent, start=start)
            if start < 0:
                break  # No more occurrences found
            parts.append(req_text[last_index:start])
            start = end
            last_index = end + 1

        # Add the remaining part of the string, if any
        if last_index <= len(req_text):
            parts.append(req_text[last_index:])

        return parts

    @staticmethod
    def _find_actual_loc(req_text: str, cleaned_index: int) -> int:
        """
        Locates the actual index in the req text with new liens added.
        :param req_text: The requirement with additional new lines.
        :param cleaned_index: The index when there are no new lines.
        :return: The index adjusted with the new lines.
        """
        chars_count = 0
        actual_index = 0
        for i, char in enumerate(req_text):
            if char != NEW_LINE:
                if chars_count == cleaned_index:
                    actual_index = i
                    break
                chars_count += 1
        return actual_index


if __name__ == "__main__":
    ContradictionsUserDisplay.create_and_run()
