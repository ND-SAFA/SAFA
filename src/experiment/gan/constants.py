import os

# Path to [dataset](https://www.notion.so/nd-safa/Test-Project-Data-856f9df9092742d097f5984e03069bd2)
from typing import List, Tuple

SOFTWARE_DATA_PATH = "/Users/albertorodriguez/projects/calpoly/LeveragingIntermediateArtifacts/datasets"
LHP_DATA_PATH = "/Users/albertorodriguez/desktop/safa dataset/validation/LHP/answer"

MODEL_EXPORT_NAME = "gan-bert"
DATA_FILE_PATH = "../../gan/se_projects.csv"
SKIP = ["TrainController", "Drone"]
TEST_SIZE = 0.5

# Data Paths
TRAINING_DATA_PATH = "/Users/albertorodriguez/desktop/safa dataset/validation/LHP/experiments"
TRAIN_EXPORT_PATH = os.path.join(TRAINING_DATA_PATH, "train.csv")
TEST_EXPORT_PATH = os.path.join(TRAINING_DATA_PATH, "test.csv")

# Models
BASE_MODEL_NAME = "thearod5/automotive"
MODEL_EXPORT_PATH = os.path.join(LHP_DATA_PATH, MODEL_EXPORT_NAME)
ProjectData = Tuple[List[Tuple[str, str]], List[Tuple[str, str]], List[int]]

# Data
