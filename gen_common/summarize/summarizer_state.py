from dataclasses import dataclass
from typing import Any, Dict, List

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.pipeline.state import State
from gen_common.summarize.summary import Summary


@dataclass
class SummarizerState(State):
    dataset: PromptDataset = None
    batch_id_to_artifacts: Dict[Any, List[Any]] = None
    project_summaries: List[Summary] = None
    final_project_summary: Summary = None
    re_summarized_artifacts_dataset: PromptDataset = None
    summarized_dataset: PromptDataset = None
