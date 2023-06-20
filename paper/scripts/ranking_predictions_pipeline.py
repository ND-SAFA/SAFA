import os.path

from paper.pipeline.base import DatasetIdentifier, RankingPipeline
from paper.pipeline.io_step import read_positive_predictions
from paper.pipeline.map_step import compute_map, create_map_instructions
from paper.pipeline.ranking_step import complete_ranking_prompts, create_ranking_prompts

if __name__ == "__main__":
    EXPERIMENT_ID = "44966436-07c5-46b3-8562-583bc0aecf06"
    DATASET_NAME = "cm1"

    run_path = f"~/desktop/safa/experiments/paper/results/{DATASET_NAME}/original/experiment_0/step_0/{EXPERIMENT_ID}/output.json"
    run_path = os.path.expanduser(run_path)

    dataset_path = f"~/desktop/safa/datasets/paper/{DATASET_NAME}"
    dataset_path = os.path.expanduser(dataset_path)

    dataset_id = DatasetIdentifier(dataset_path=dataset_path, experiment_id=EXPERIMENT_ID, run_path=run_path,
                                   dataset_name=DATASET_NAME)
    steps = [read_positive_predictions, create_ranking_prompts, complete_ranking_prompts, create_map_instructions, compute_map]
    pipeline = RankingPipeline(dataset_id, steps)
    pipeline.run()
