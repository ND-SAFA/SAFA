class PredictionRequest:
    MODEL_PATH = "modelPath"  # The path to the model weights / state.
    SOURCES = "sources"  # List of source artifacts
    TARGETS = "targets"  # List of target artifacts
    OUTPUT_DIR = "outputDir"  # Path to directory of output file.
    BASE_MODEL = "baseModel"  # The base model class to use.
    LINKS = "links"  # List of true links between source and target artifacts
    JOB_ID = "jobID"  # The ID of the job to find results.
    LOAD_FROM_STORAGE = "loadFromStorage"  # Whether model weights should reference cloud storage
