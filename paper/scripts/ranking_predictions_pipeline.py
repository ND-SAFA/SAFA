import os.path

from paper.pipeline.base import DatasetIdentifier, RankingPipeline
from paper.pipeline.classification_step import compute_precision
from paper.pipeline.extract_targets_steps import extract_related_target_artifacts
from paper.pipeline.io_step import read_positive_predictions
from paper.pipeline.map_step import compute_map, create_metric_instructions
from paper.pipeline.ranking_step import complete_ranking_prompts, create_ranking_prompts
from paper.pipeline.response_process_step import process_ranking_prompts

if __name__ == "__main__":
    EXPERIMENT_ID = "c3442bd7-4d4a-4891-827b-a91b0dc1e799"
    DATASET_NAME = "cm1"

    run_path = f"~/desktop/safa/experiments/rankings/{DATASET_NAME}/{EXPERIMENT_ID}/output.json"
    run_path = os.path.expanduser(run_path)

    dataset_path = f"~/desktop/safa/datasets/paper/{DATASET_NAME}"
    dataset_path = os.path.expanduser(dataset_path)

    dataset_id = DatasetIdentifier(dataset_path=dataset_path, experiment_id=EXPERIMENT_ID, run_path=run_path,
                                   dataset_name=DATASET_NAME)
    steps = [
        read_positive_predictions,  # reads previous run and extracts positive predictions
        extract_related_target_artifacts,  # reads the targets and sorts them
        create_ranking_prompts,  # creates prompts for positively predicted targets
        complete_ranking_prompts,  # completes the ranking prompts
        process_ranking_prompts,
        create_metric_instructions,  # creates necessary information for computing metrics
        compute_map,  # computes average precision for each query and mean AP.
        compute_precision  # computes precision at 1, 2, and 3 predictions.
    ]
    pipeline = RankingPipeline(dataset_id, steps)
    pipeline.run()
