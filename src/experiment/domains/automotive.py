# Import project
import argparse
import os
import sys

SRC_PATH = os.path.normpath(os.path.dirname(os.path.join(__file__, "..", "../..", "..")))
sys.path.append(SRC_PATH)

from experiment.common.experiment_run import ExperimentRun
from experiment.common.pretraining_data import PretrainingData
from experiment.common.run_mode import RunMode

GREADER_PATH = "/Users/albertorodriguez/Projects/SAFA/greader"
SAFA_PATH = os.path.join(GREADER_PATH, "safa")
OUTPUT_DIR = "/Users/albertorodriguez/Desktop/safa data/automotive/models"
REPOSITORIES = ["ApolloAuto/apollo",
                "autorope/donkeycar",
                "Autonomous-Racing-PG/ar-tu-do",
                "pylessard/python-udsoncan"]
VALIDATION_PERCENTAGE_DEFAULT = .1
N_TRAINING_EPOCHS = 10
PRETRAINING_DATA = PretrainingData.AUTOMOTIVE
STATE_PATHS = ["bert-base-uncased",
               "thearod5/sebert-task-cls",
               "/Users/albertorodriguez/Desktop/safa data/automotive/models/thearod5/sebert-task-cls_automotive",
               "/Users/albertorodriguez/Desktop/safa data/automotive/models/thearod5/sebert-task-cls_automotive_lm",
               "/Users/albertorodriguez/Desktop/safa data/automotive/models/thearod5/sebert-task-cls_automotive_lm_automotive",
               "/Users/albertorodriguez/Desktop/safa data/automotive/models/nl_bert_automotive"]
METRICS = ["map_at_k"]
TEST_PROJECT_PATH = "/Users/albertorodriguez/Desktop/safa data/validation/lhp/answer"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",
                        help="The job to perform with the model",
                        choices=[e.value for e in RunMode])
    parser.add_argument("model_state_path_indices",
                        help="The initial mode states.",
                        type=int, nargs='+',
                        choices=[0, 1, 2, 3, 4, 5])
    parser.add_argument("-training_repos", "-t",
                        required=False,
                        type=str, nargs='+',
                        help="The repositories to train on.",
                        choices=REPOSITORIES,
                        default=REPOSITORIES)
    args = parser.parse_args()

    # Run state
    for model_state_path_index in args.model_state_path_indices:
        experiment = ExperimentRun(
            STATE_PATHS[model_state_path_index],
            PRETRAINING_DATA,
            [os.path.join(SAFA_PATH, r) for r in args.training_repos],
            METRICS,
            TEST_PROJECT_PATH,
        )
        if args.mode == "lm":
            file_path = "/Users/albertorodriguez/desktop/safa data/automotive/txt"
            experiment.perform_language_modeling(
                file_path,
                OUTPUT_DIR
            )
        if args.mode == "push":
            experiment.push()
        else:
            experiment.perform_run(
                OUTPUT_DIR,
                args.mode,
                load_best_model_at_end=True,
                metric_for_best_model="eval_map_at_k",
                greater_is_better=True
            )
