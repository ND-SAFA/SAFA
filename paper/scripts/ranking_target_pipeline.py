import os.path
import uuid

from paper.pipeline.base import DatasetIdentifier, RankingPipeline
from paper.pipeline.classification_step import compute_precision
from paper.pipeline.extract_targets_steps import extract_related_target_artifacts
from paper.pipeline.io_step import read_labels
from paper.pipeline.map_step import compute_map, create_metric_instructions
from paper.pipeline.ranking_step import RankingStep
from paper.pipeline.reasoning_step import ReasoningStep

if __name__ == "__main__":
    EXPERIMENT_ID = str(uuid.uuid4())
    DATASET_NAME = "cm1"
    dataset_path = f"~/desktop/safa/datasets/paper/{DATASET_NAME}"
    dataset_path = os.path.expanduser(dataset_path)

    dataset_id = DatasetIdentifier(dataset_path=dataset_path, experiment_id=EXPERIMENT_ID, dataset_name=DATASET_NAME)

    steps = [read_labels,
             extract_related_target_artifacts,  # reads the targets associated with run
             ReasoningStep(),
             RankingStep(),
             create_metric_instructions,
             compute_map,
             compute_precision]
    pipeline = RankingPipeline(dataset_id, steps, sorter="vsm")
    pipeline.run()
