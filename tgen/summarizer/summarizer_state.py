from dataclasses import dataclass

from typing import List, Dict, Any

from tgen.clustering.base.cluster_type import ClusterMapType
from common_resources.tools.util.override import overrides
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.tools.state_management.state import State
from tgen.summarizer.summary import Summary


@dataclass
class SummarizerState(State):
    dataset: PromptDataset = None
    batch_id_to_artifacts: Dict[Any, List[Any]] = None
    project_summaries: List[Summary] = None
    final_project_summary: Summary = None
    re_summarized_artifacts_dataset: PromptDataset = None
    summarized_dataset: PromptDataset = None
