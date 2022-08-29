from enum import Enum


class PredictionRequest(Enum):
    MODEL_PATH = "modelPath"
    SOURCES = "sources"
    TARGETS = "targets"
    OUTPUT_PATH = "outputPath"
    BASE_MODEL = "baseModel"
    LINKS = "links"
    JOB_ID = "jobID"
