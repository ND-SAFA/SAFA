import os.path
import uuid

from paper.pipeline.base import DatasetIdentifier, RankingPipeline
from paper.pipeline.classification_step import add_precision
from paper.pipeline.io_step import read_predictions
from paper.pipeline.map_step import compute_map, create_map_instructions
from paper.pipeline.ranking_step import complete_ranking_prompts, create_ranking_prompts

if __name__ == "__main__":
    EXPERIMENT_ID = str(uuid.uuid4())
    DATASET_NAME = "drone-pl"
    dataset_path = f"~/desktop/safa/datasets/paper/{DATASET_NAME}"
    # dataset_path = f"~/desktop/safa/datasets/safa/source"

    dataset_path = os.path.expanduser(dataset_path)

    dataset_id = DatasetIdentifier(dataset_path=dataset_path, experiment_id=EXPERIMENT_ID, dataset_name=DATASET_NAME)

    steps = [read_predictions, create_ranking_prompts, complete_ranking_prompts, create_map_instructions, compute_map, add_precision]
    pipeline = RankingPipeline(dataset_id, steps)
    pipeline.run()
