from dataclasses import dataclass

from typing import List

from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.pipeline.state import State
from tgen.summarizer.summary import Summary


@dataclass
class SummarizerState(State):
    dataset: PromptDataset = None
    cluster_map: ClusterMapType = None
    project_summaries: List[Summary] = None
    final_project_summary: Summary = None
    re_summarized_artifacts_dataset: PromptDataset = None
    summarized_dataset: PromptDataset = None
