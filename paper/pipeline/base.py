import json
import os
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from tgen.models.llm.llm_responses import GenerationResponse
from tgen.util.file_util import FileUtil
from tgen.util.json_util import NpEncoder

DEFAULT_RANKING_QUESTION = "Rank the artifacts from most to least relevant to the source. " \
                           "Provide the ranked artifacts as comma delimited list of artifact ids. " \
                           "\n\nSource: "
DEFAULT_RANKING_FORMAT = None
DEFAULT_EXPERIMENT_DIR = os.path.expanduser("~/desktop/safa/experiments/rankings")


def remove_file_extension(file_name):
    file_name_without_extension, _ = os.path.splitext(file_name)
    return file_name_without_extension


def get_trace_id(row):
    source_name = remove_file_extension(row["source"])
    target_name = remove_file_extension(row["target"])
    return f"{source_name}-{target_name}"


def create_artifact_map(a_df):
    a_map = {}
    for i, row in a_df.reset_index().iterrows():
        artifact_id = row["id"]
        a_map[artifact_id] = row["content"]
    return a_map


@dataclass
class RankingStore:
    # Instructions
    project_path: str  # path to original dataset
    experiment_id: str  # The UUID of the run on the dataset.
    sorter: str  # The name of the sorter to use
    prompt_question: str = DEFAULT_RANKING_QUESTION  # The prompt used to rank artifacts.
    prompt_format: str = DEFAULT_RANKING_FORMAT
    prompt_artifacts: List[str] = None
    run_path: str = None  # path to predictions on dataset

    # Project
    artifact_map: Dict = field(default=None, repr=False)  # map of artifact name to body
    source_ids: Optional[List[str]] = field(default=None, repr=False)  # enumerates order of prompts
    traced_ids: Optional[List[str]] = field(default=None, repr=False)  # determines label of model responses
    target_ids: Optional[List[str]] = field(default=None, repr=False)  # helps find missing artifact ids in model responses
    trace_entries: Optional[List[Dict]] = field(default=None, repr=False)  # determines what links get included in source queries

    # Models
    prompts: Optional[List[str]] = field(default=None, repr=False)  # the prompts given to the models
    batch_response: Optional[GenerationResponse] = field(default=None, repr=False)
    ranked_predictions: Optional[List[List[str]]] = field(default=None, repr=False)  # list of ranked artifact ids per source artifact
    processed_response: Optional[List[List[str]]] = field(default=None, repr=False)

    # Metrics
    map_instructions: Optional[List[Dict]] = field(default=None, repr=False)
    metrics: Optional[Dict] = field(default=None, repr=False)


RankingStep = Callable[[RankingStore], None]


@dataclass
class DatasetIdentifier:
    dataset_path: str
    experiment_id: str
    dataset_name: str
    run_path: str = None


class RankingPipeline:
    def __init__(self, dataset_id: DatasetIdentifier, steps: List[RankingStep], sorter: str,
                 base_prompt: str = DEFAULT_RANKING_QUESTION,
                 export_dir: str = DEFAULT_EXPERIMENT_DIR):
        self.steps = steps
        self.store = RankingStore(project_path=dataset_id.dataset_path, run_path=dataset_id.run_path,
                                  experiment_id=dataset_id.experiment_id, prompt_question=base_prompt, sorter=sorter)
        self.dataset_export_dir = os.path.join(export_dir, dataset_id.dataset_name)

    def run(self):
        for step in self.steps:
            step(self.store)
        self.export()

    def export(self):
        print(json.dumps(self.store.metrics, indent=4))
        store_export_path = os.path.join(self.dataset_export_dir, self.store.experiment_id, "store.json")
        metrics_export_path = os.path.join(self.dataset_export_dir, self.store.experiment_id, "metrics.json")

        FileUtil.write(json.dumps(self.store.metrics, indent=4), metrics_export_path)
        FileUtil.write(json.dumps(self.store, indent=4, cls=NpEncoder), store_export_path)
        print(f"Saved to: {store_export_path}")
