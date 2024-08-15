from dataclasses import dataclass

from typing import List, Dict

from common_resources.tools.state_management.state import State
from tgen.summarizer.summary import Summary


@dataclass
class DeltaState(State):
    export_dir: str = None  # The path to save the state to

    # ------- STEP 1 ----------
    diff_summaries: Dict = None  # maps filename to the results of the diff summary

    # ------- STEP 2 ----------
    change_summary_output: Dict = None  # output from model, includes the grouping of changes and summaries
    overview_section: List[str] = None  # list of each part of the overview section
    change_details_section: List[str] = None  # list of each part of the change details section

    # ------- STEP 3 ----------
    impact: str = None  # summary of the impact of the changes on the system
    final_summary: str = None  # Markdown version of the final change summary
