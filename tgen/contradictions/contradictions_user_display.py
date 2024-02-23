import threading
import tkinter as tk
from tkinter import font, messagebox, scrolledtext

from tgen.common.objects.artifact import Artifact
from tgen.contradictions.contradictions_detector import ContradictionsDetector


class ContradictionsUserDisplay:
    BACKGROUND_COLOR = "#f3f4f6"
    N_REQUIREMENTS = 2

    root = None
    font = None
    requirements_entries = []
    result_text = None

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
        requirements = [r.get("1.0", "end-1c") for r in self.requirements_entries]
        artifacts = [Artifact(id=f"R{i}", content=req, layer_id="Requirement") for i, req in enumerate(requirements)]
        decision_tree_path = ContradictionsDetector.detect_single_pair(*artifacts)
        self.root.after(0, self._create_result_popup, decision_tree_path.get_final_decision())

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
                                 bg="#4e8d7c", fg="white", relief=tk.FLAT)
        check_button.pack(pady=10)
        return check_button

    def _create_result_popup(self, result: str) -> None:
        """
        Creates the popup for displaying the result.
        :param result: The result of the contradiction detection.
        :return: None.
        """
        messagebox.showinfo("Contradictions Result", result)
        self.result_text.set("")  # Clear the text


if __name__ == "__main__":
    ContradictionsUserDisplay.create_and_run()
